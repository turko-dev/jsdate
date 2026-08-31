from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import math
import re


_ISO_DATE_ONLY_RE = re.compile(
    r"^(?P<year>[+-]?\d{4,6})-"
    r"(?P<month>\d{2})-"
    r"(?P<day>\d{2})$"
)

_ISO_LOCAL_OR_OFFSET_RE = re.compile(
    r"^(?P<year>[+-]?\d{4,6})-"
    r"(?P<month>\d{2})-"
    r"(?P<day>\d{2})T"
    r"(?P<hour>\d{2}):"
    r"(?P<minute>\d{2})"
    r"(?::(?P<second>\d{2})(?:\.(?P<fraction>\d{1,6}))?)?"
    r"(?P<tz>Z|[+-]\d{2}:\d{2})?$"
)


def now() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def parse(date_string: str) -> float:
    if not isinstance(date_string, str):
        return math.nan

    m = _ISO_DATE_ONLY_RE.match(date_string)
    if m:
        parts = {k: int(v) for k, v in m.groupdict().items()}
        try:
            dt = datetime(parts["year"], parts["month"], parts["day"], tzinfo=timezone.utc)
            return int(dt.timestamp() * 1000)
        except ValueError:
            return math.nan

    m = _ISO_LOCAL_OR_OFFSET_RE.match(date_string)
    if m:
        gd = m.groupdict()
        try:
            year = int(gd["year"])
            month = int(gd["month"])
            day = int(gd["day"])
            hour = int(gd["hour"])
            minute = int(gd["minute"])
            second = int(gd["second"] or 0)
            fraction = gd["fraction"] or "0"
            microsecond = int(fraction.ljust(6, "0")[:6])
            tz_part = gd["tz"]

            if tz_part == "Z":
                dt = datetime(year, month, day, hour, minute, second, microsecond, tzinfo=timezone.utc)
                return int(dt.timestamp() * 1000)

            if tz_part:
                sign = 1 if tz_part[0] == "+" else -1
                off_h = int(tz_part[1:3])
                off_m = int(tz_part[4:6])
                offset = timezone(sign * timedelta(hours=off_h, minutes=off_m))
                dt = datetime(year, month, day, hour, minute, second, microsecond, tzinfo=offset)
                return int(dt.timestamp() * 1000)

            local_dt = datetime(year, month, day, hour, minute, second, microsecond).astimezone()
            return int(local_dt.timestamp() * 1000)
        except ValueError:
            return math.nan

    try:
        dt = parsedate_to_datetime(date_string)
        if dt is None:
            return math.nan
        if dt.tzinfo is None:
            dt = dt.astimezone()
        return int(dt.timestamp() * 1000)
    except Exception:
        return math.nan


def UTC(year, monthIndex=0, day=1, hours=0, minutes=0, seconds=0, milliseconds=0) -> float:
    try:
        year = int(year)
        monthIndex = int(monthIndex)
        day = int(day)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        milliseconds = int(milliseconds)
    except Exception:
        return math.nan

    if 0 <= year <= 99:
        year += 1900

    year += monthIndex // 12
    monthIndex = monthIndex % 12
    month = monthIndex + 1

    try:
        base = datetime(year, month, 1, tzinfo=timezone.utc)
        dt = base + timedelta(
            days=day - 1,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
        )
        return int(dt.timestamp() * 1000)
    except Exception:
        return math.nan