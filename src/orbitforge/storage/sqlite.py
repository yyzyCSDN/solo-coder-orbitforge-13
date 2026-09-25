from __future__ import annotations
import sqlite3, json, hashlib, time

class Store:

    def __init__(self, path=':memory:'):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute('pragma journal_mode=WAL')
        self.conn.executescript('create table if not exists analyses(id text primary key, kind text not null, payload text not null, created real not null); create table if not exists audit(seq integer primary key autoincrement, event text not null, digest text not null, created real not null);')

    def put(self, kind, payload):
        raw = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        ident = hashlib.sha256((kind + '|' + raw).encode()).hexdigest()
        now = time.time()
        self.conn.execute('insert or ignore into analyses values(?,?,?,?)', (ident, kind, raw, now))
        self.conn.execute('insert into audit(event,digest,created) values(?,?,?)', (kind, hashlib.sha256(raw.encode()).hexdigest(), now))
        self.conn.commit()
        return ident

    def get(self, ident):
        row = self.conn.execute('select kind,payload,created from analyses where id=?', (ident,)).fetchone()
        return None if row is None else {'id': ident, 'kind': row[0], 'payload': json.loads(row[1]), 'created': row[2]}

    def list(self, kind=None):
        q = 'select id,kind,payload,created from analyses'
        args = ()
        if kind is not None:
            q += ' where kind=?'
            args = (kind,)
        return [{'id': r[0], 'kind': r[1], 'payload': json.loads(r[2]), 'created': r[3]} for r in self.conn.execute(q + ' order by created desc', args)]

    def audit_chain(self):
        return [{'seq': r[0], 'event': r[1], 'digest': r[2], 'created': r[3]} for r in self.conn.execute('select seq,event,digest,created from audit order by seq')]
