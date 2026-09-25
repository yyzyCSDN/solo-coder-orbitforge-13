from __future__ import annotations
from bisect import bisect_right
from dataclasses import dataclass

@dataclass(frozen=True)
class LeapEntry:
    unix_utc_s: int
    tai_minus_utc: int
LEAPS = [LeapEntry(63072000, 10), LeapEntry(78796800, 11), LeapEntry(94694400, 12), LeapEntry(126230400, 13), LeapEntry(157766400, 14), LeapEntry(189302400, 15), LeapEntry(220924800, 16), LeapEntry(252460800, 17), LeapEntry(283996800, 18), LeapEntry(315532800, 19), LeapEntry(362793600, 20), LeapEntry(394329600, 21), LeapEntry(425865600, 22), LeapEntry(489024000, 23), LeapEntry(567993600, 24), LeapEntry(631152000, 25), LeapEntry(662688000, 26), LeapEntry(709948800, 27), LeapEntry(741484800, 28), LeapEntry(773020800, 29), LeapEntry(820454400, 30), LeapEntry(867715200, 31), LeapEntry(915148800, 32), LeapEntry(1136073600, 33), LeapEntry(1230768000, 34), LeapEntry(1341100800, 35), LeapEntry(1435708800, 36), LeapEntry(1483228800, 37)]

def tai_minus_utc(unix_utc_s: float) -> int:
    points = [e.unix_utc_s for e in LEAPS]
    i = bisect_right(points, unix_utc_s) - 1
    return LEAPS[i].tai_minus_utc if i >= 0 else 10

def utc_unix_to_tai(unix_utc_s: float) -> float:
    return unix_utc_s + tai_minus_utc(unix_utc_s)

def tai_to_utc_unix(tai_s: float) -> float:
    guess = tai_s - 37
    for _ in range(6):
        guess = tai_s - tai_minus_utc(guess)
    return guess
