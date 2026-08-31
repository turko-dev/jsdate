from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import re

from . import static as _static
from . import setters as _setters
from . import getters as _getters


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
        m = cls._ISO_UTC_RE.match(s)
        if not m:
            raise ValueError("Expected format YYYY-MM-DDTHH:mm:ss.sssZ")

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

    @staticmethod
    def now() -> int:
        return _static.now()

    @staticmethod
    def parse(date_string: str) -> float:
        return _static.parse(date_string)

    @staticmethod
    def UTC(year, monthIndex=0, day=1, hours=0, minutes=0, seconds=0, milliseconds=0) -> float:
        return _static.UTC(year, monthIndex, day, hours, minutes, seconds, milliseconds)



    def getDate(self) -> int | float: return _getters.getDate(self)
    def getDay(self) -> int | float: return _getters.getDay(self)
    def getFullYear(self) -> int | float: return _getters.getFullYear(self)
    def getHours(self) -> int | float: return _getters.getHours(self)
    def getMilliseconds(self) -> int | float: return _getters.getMilliseconds(self)
    def getMinutes(self) -> int | float: return _getters.getMinutes(self)
    def getMonth(self) -> int | float: return _getters.getMonth(self)
    def getSeconds(self) -> int | float: return _getters.getSeconds(self)
    def getTime(self) -> int | float: return _getters.getTime(self)
    def getTimezoneOffset(self) -> int | float: return _getters.getTimezoneOffset(self)
    def getUTCDate(self) -> int | float: return _getters.getUTCDate(self)
    def getUTCDay(self) -> int | float: return _getters.getUTCDay(self)
    def getUTCFullYear(self) -> int | float: return _getters.getUTCFullYear(self)
    def getUTCHours(self) -> int | float: return _getters.getUTCHours(self)
    def getUTCMilliseconds(self) -> int | float: return _getters.getUTCMilliseconds(self)
    def getUTCMinutes(self) -> int | float: return _getters.getUTCMinutes(self)
    def getUTCMonth(self) -> int | float: return _getters.getUTCMonth(self)
    def getUTCSeconds(self) -> int | float: return _getters.getUTCSeconds(self)
    def getYear(self) -> int | float: return _getters.getYear(self)
    def setDate(self, dateValue): return _setters.setDate(self, dateValue)
    def setFullYear(self, yearValue, monthValue=None, dateValue=None): return _setters.setFullYear(self, yearValue, monthValue, dateValue)
    def setHours(self, hoursValue, minutesValue=None, secondsValue=None, msValue=None): return _setters.setHours(self, hoursValue, minutesValue, secondsValue, msValue)
    def setMilliseconds(self, millisecondsValue):return _setters.setMilliseconds(self, millisecondsValue)
    def setMinutes(self, minutesValue, secondsValue=None, msValue=None): return _setters.setMinutes(self, minutesValue, secondsValue, msValue)
    def setMonth(self, monthValue, dateValue=None): return _setters.setMonth(self, monthValue, dateValue)
    def setSeconds(self, secondsValue, msValue=None): return _setters.setSeconds(self, secondsValue, msValue)
    def setTime(self, timeValue): return _setters.setTime(self, timeValue)
    def setUTCDate(self, dateValue): return _setters.setUTCDate(self, dateValue)
    def setUTCFullYear(self, yearValue, monthValue=None, dateValue=None): return _setters.setUTCFullYear(self, yearValue, monthValue, dateValue)
    def setUTCHours(self, hoursValue, minutesValue=None, secondsValue=None, msValue=None): return _setters.setUTCHours(self, hoursValue, minutesValue, secondsValue, msValue)
    def setUTCMilliseconds(self, millisecondsValue): return _setters.setUTCMilliseconds(self, millisecondsValue)
    def setUTCMinutes(self, minutesValue, secondsValue=None, msValue=None): return _setters.setUTCMinutes(self, minutesValue, secondsValue, msValue)
    def setUTCMonth(self, monthValue, dateValue=None): return _setters.setUTCMonth(self, monthValue, dateValue)
    def setUTCSeconds(self, secondsValue, msValue=None): return _setters.setUTCSeconds(self, secondsValue, msValue)
    def setYear(self, yearValue): return _setters.setYear(self, yearValue)