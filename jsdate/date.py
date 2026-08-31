from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import calendar
import re

@dataclass
class Date:
    _dt: datetime

    _ISO_UTC_RE = re.compile(
        r"^(?P<year>[+-]?\d{4,6})-"
        r"(?P<month>\d{2})-"
        r"(?P<day>\d{2})T"
        r"(?P<hour>\d{2}):"
        r"(?P<minute>\d{2}):"
        r"(?P<second>\d{2})\."
        r"(?P<millisecond>\d{3})Z$"
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
                self._dt = value.replace()
                return

            if isinstance(value, str):
                self._dt = self._from_iso_utc_string(value)
                return

            if isinstance(value, (int, float)):
                self._dt = datetime.fromtimestamp(value / 1000, tz=timezone.utc).astimezone()
                return

            raise TypeError("Unsupported single-argument constructor form")

        self._dt = self._from_components(*args)

    @classmethod
    def _from_iso_utc_string(cls, s: str) -> datetime:
        
        match = cls._ISO_UTC_RE.match(s)
        if not match: raise ValueError("Expected format YYYY-MM-DDTHH:mm:ss.sssZ")

        parts = {k: int(v) for k, v in m.groupdict().items()}
        dt = datetime(
            year=parts["year"],
            month=parts["month"],
            day=parts["day"],
            hour=parts["hour"],
            minute=parts["minute"],
            second=parts["second"],
            microsecond=parts["millisecond"] * 1000,
            tzinfo=timezone.utc,
        )
        return dt.astimezone()

    @staticmethod
    def _days_in_month(year: int, month_1_based: int) -> int:
        return calendar.monthrange(year, month_1_based)[1]

    @classmethod
    def _from_components(cls, *args) -> datetime:
        if len(args) < 2 or len(args) > 7:
            raise TypeError("Component constructor expects 2 to 7 arguments")

        year = int(args[0])
        month_index = int(args[1])
        day = int(args[2]) if len(args) > 2 else 1
        hour = int(args[3]) if len(args) > 3 else 0
        minute = int(args[4]) if len(args) > 4 else 0
        second = int(args[5]) if len(args) > 5 else 0
        millisecond = int(args[6]) if len(args) > 6 else 0

        if 0 <= year <= 99:
            year += 1900

        year += month_index // 12
        month_index = month_index % 12
        month = month_index + 1

        base = datetime(year, month, 1)
        delta = timedelta(
            days=day - 1,
            hours=hour,
            minutes=minute,
            seconds=second,
            milliseconds=millisecond,
        )
        return base + delta

    def valueOf(self) -> int:
        return int(self._dt.astimezone(timezone.utc).timestamp() * 1000)

    def toISOString(self) -> str:
        dt_utc = self._dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt_utc.microsecond // 1000:03d}Z"

    def to_datetime(self) -> datetime:
        return self._dt.replace()

    def __repr__(self) -> str:
        return self.toISOString()