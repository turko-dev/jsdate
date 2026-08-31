from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import math
import re


@dataclass
class Date:
    _dt: datetime

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

    def __init__(self, *args):
        if len(args) == 0:
            self._dt = datetime.now().astimezone()
            return

        if len(args) == 1:
            value = args[0]

            if isinstance(value, Date):
                self._dt = value._dt.replace()
                return

            if isinstance(value, datetime):
                if value.tzinfo is None:
                    self._dt = value.astimezone()
                else:
                    self._dt = value.astimezone().replace()
                return

            if isinstance(value, str):
                timestamp = self.parse(value)
                if math.isnan(timestamp):
                    raise ValueError("Invalid date string")
                self._dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).astimezone()
                return

            if isinstance(value, (int, float)):
                self._dt = datetime.fromtimestamp(value / 1000, tz=timezone.utc).astimezone()
                return

            raise TypeError("Unsupported single-argument constructor form")

        self._dt = self._from_components_local(*args)

    @staticmethod
    def now() -> int:
        return int(datetime.now(timezone.utc).timestamp() * 1000)

    @staticmethod
    def parse(date_string: str) -> float:
        if not isinstance(date_string, str):
            return math.nan

        m = Date._ISO_DATE_ONLY_RE.match(date_string)
        if m:
            parts = {k: int(v) for k, v in m.groupdict().items()}
            try:
                dt = datetime(parts["year"], parts["month"], parts["day"], tzinfo=timezone.utc)
                return int(dt.timestamp() * 1000)
            except ValueError:
                return math.nan

        m = Date._ISO_LOCAL_OR_OFFSET_RE.match(date_string)
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

    @staticmethod
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

    @classmethod
    def _from_components_local(cls, *args) -> datetime:
        if len(args) < 2 or len(args) > 7:
            raise TypeError("Component constructor expects 2 to 7 arguments")

        year = int(args[0])
        monthIndex = int(args[1])
        day = int(args[2]) if len(args) > 2 else 1
        hours = int(args[3]) if len(args) > 3 else 0
        minutes = int(args[4]) if len(args) > 4 else 0
        seconds = int(args[5]) if len(args) > 5 else 0
        milliseconds = int(args[6]) if len(args) > 6 else 0

        if 0 <= year <= 99:
            year += 1900

        year += monthIndex // 12
        monthIndex = monthIndex % 12
        month = monthIndex + 1

        base = datetime(year, month, 1).astimezone()
        return base + timedelta(
            days=day - 1,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
        )

    def valueOf(self) -> int:
        return int(self._dt.astimezone(timezone.utc).timestamp() * 1000)

    def toISOString(self) -> str:
        dt_utc = self._dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt_utc.microsecond // 1000:03d}Z"

    def to_datetime(self) -> datetime:
        return self._dt.replace()

    def __repr__(self) -> str:
        return f"Date({self.toISOString()})"