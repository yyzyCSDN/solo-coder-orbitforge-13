from __future__ import annotations
import struct
from dataclasses import dataclass

@dataclass(frozen=True)
class TelemetryPacket:
    apid: int
    sequence: int
    coarse_time: int
    payload: bytes


def encode(packet: TelemetryPacket):
    if not 0 <= packet.apid < 2048:
        raise ValueError('APID range')
    if not 0 <= packet.sequence < 16384:
        raise ValueError('sequence range')
    first = packet.apid
    second = 0xC000 | packet.sequence
    length = len(packet.payload) + 4 - 1
    header = struct.pack('>HHHI', first, second, length, packet.coarse_time)
    return header + packet.payload


def decode(data: bytes):
    if len(data) < 10:
        raise ValueError('truncated telemetry packet')
    first, second, length, coarse = struct.unpack('>HHHI', data[:10])
    expected = length + 1 - 4
    payload = data[10:]
    if len(payload) != expected:
        raise ValueError('packet length mismatch')
    return TelemetryPacket(first & 0x7FF, second & 0x3FFF, coarse, payload)
