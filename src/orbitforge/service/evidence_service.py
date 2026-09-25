from __future__ import annotations
from orbitforge.verification.evidence import evidence_record, chain, verify_chain

class EvidenceService:
    def __init__(self):
        self._records = []

    def append(self, kind, inputs, outputs, configuration):
        record = evidence_record(kind, inputs, outputs, configuration)
        self._records.append(record)
        return record

    def export_chain(self):
        return chain(self._records)

    def verify(self):
        return verify_chain(self.export_chain())

    def count(self):
        return len(self._records)
