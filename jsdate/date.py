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
        '''Enables basic storage and retrieval of dates and times.'''

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

    #Basic class methods for internal use
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



    '''The following methods are for external use only and these are the in-house methods that point to other modules.
    These include:
    - getters.py
    - setters.py
    - static.py
    etcetera.
    '''
    
    #A map of static methods such as now(), parse(), and UTC() for external use
    @staticmethod
    def now() -> int:
        """Returns the number of milliseconds elapsed since the epoch."""
        return _static.now()

    @staticmethod
    def parse(date_string: str) -> float:
        '''A date string
        Parses a string containing a date, and returns the number of milliseconds between that date and the epoch.'''
        return _static.parse(date_string)

    @staticmethod
    def UTC(year, monthIndex=0, day=1, hours=0, minutes=0, seconds=0, milliseconds=0) -> float: 
        '''If a year is between 0 and 99, then year is assumed to be 1900 + year.
        Returns the number of milliseconds between the epoch and the specified date.'''
        return _static.UTC(year, monthIndex, day, hours, minutes, seconds, milliseconds)


    # A map of getter functions (maps from getters.py as _getters) for external use

    def getDate(self) -> int | float:
        """Return the day of the month in local time."""
        return _getters.getDate(self)

    def getDay(self) -> int | float:
        """Return the weekday in local time, where Sunday is 0 and Saturday is 6."""
        return _getters.getDay(self)

    def getFullYear(self) -> int | float:
        """Return the full local year as a four-digit value when applicable."""
        return _getters.getFullYear(self)

    def getHours(self) -> int | float:
        """Return the hour in local time using a 24-hour clock."""
        return _getters.getHours(self)

    def getMilliseconds(self) -> int | float:
        """Return the millisecond component in local time."""
        return _getters.getMilliseconds(self)

    def getMinutes(self) -> int | float:
        """Return the minute component in local time."""
        return _getters.getMinutes(self)

    def getMonth(self) -> int | float:
        """Return the local month using JavaScript's zero-based month numbering."""
        return _getters.getMonth(self)

    def getSeconds(self) -> int | float:
        """Return the second component in local time."""
        return _getters.getSeconds(self)

    def getTime(self) -> int | float:
        """Return the Unix timestamp in milliseconds."""
        return _getters.getTime(self)

    def getTimezoneOffset(self) -> int | float:
        """Return the difference, in minutes, between local time and UTC for this date."""
        return _getters.getTimezoneOffset(self)

    def getUTCDate(self) -> int | float:
        """Return the day of the month in UTC."""
        return _getters.getUTCDate(self)

    def getUTCDay(self) -> int | float:
        """Return the UTC weekday, where Sunday is 0 and Saturday is 6."""
        return _getters.getUTCDay(self)

    def getUTCFullYear(self) -> int | float:
        """Return the full year in UTC."""
        return _getters.getUTCFullYear(self)

    def getUTCHours(self) -> int | float:
        """Return the hour component in UTC using a 24-hour clock."""
        return _getters.getUTCHours(self)

    def getUTCMilliseconds(self) -> int | float:
        """Return the millisecond component in UTC."""
        return _getters.getUTCMilliseconds(self)

    def getUTCMinutes(self) -> int | float:
        """Return the minute component in UTC."""
        return _getters.getUTCMinutes(self)

    def getUTCMonth(self) -> int | float:
        """Return the month in UTC using JavaScript's zero-based month numbering."""
        return _getters.getUTCMonth(self)

    def getUTCSeconds(self) -> int | float:
        """Return the second component in UTC."""
        return _getters.getUTCSeconds(self)

    def getYear(self) -> int | float:
        """Return the legacy local year offset from 1900. Deprecated; prefer getFullYear()."""
        return _getters.getYear(self)

    # A map of setter functions (maps from setters.py as _setters) for external use

    def setDate(self, dateValue):
        """Set the day of the month in local time and return the updated timestamp."""
        return _setters.setDate(self, dateValue)

    def setFullYear(self, yearValue, monthValue=None, dateValue=None):
        """Set the local year, and optionally the month and day, then return the updated timestamp."""
        return _setters.setFullYear(self, yearValue, monthValue, dateValue)

    def setHours(self, hoursValue, minutesValue=None, secondsValue=None, msValue=None):
        """Set the local hour and optionally minutes, seconds, and milliseconds."""
        return _setters.setHours(self, hoursValue, minutesValue, secondsValue, msValue)

    def setMilliseconds(self, millisecondsValue):
        """Set the local millisecond component and return the updated timestamp."""
        return _setters.setMilliseconds(self, millisecondsValue)

    def setMinutes(self, minutesValue, secondsValue=None, msValue=None):
        """Set the local minute component and optionally seconds and milliseconds."""
        return _setters.setMinutes(self, minutesValue, secondsValue, msValue)

    def setMonth(self, monthValue, dateValue=None):
        """Set the local month with zero-based numbering and optionally the day of the month."""
        return _setters.setMonth(self, monthValue, dateValue)

    def setSeconds(self, secondsValue, msValue=None):
        """Set the local second component and optionally milliseconds."""
        return _setters.setSeconds(self, secondsValue, msValue)

    def setTime(self, timeValue):
        """Set the date from a Unix timestamp expressed in milliseconds."""
        return _setters.setTime(self, timeValue)

    def setUTCDate(self, dateValue):
        """Set the day of the month in UTC and return the updated timestamp."""
        return _setters.setUTCDate(self, dateValue)

    def setUTCFullYear(self, yearValue, monthValue=None, dateValue=None):
        """Set the UTC year, and optionally the UTC month and day, then return the updated timestamp."""
        return _setters.setUTCFullYear(self, yearValue, monthValue, dateValue)

    def setUTCHours(self, hoursValue, minutesValue=None, secondsValue=None, msValue=None):
        """Set the UTC hour and optionally minutes, seconds, and milliseconds."""
        return _setters.setUTCHours(self, hoursValue, minutesValue, secondsValue, msValue)

    def setUTCMilliseconds(self, millisecondsValue):
        """Set the UTC millisecond component and return the updated timestamp."""
        return _setters.setUTCMilliseconds(self, millisecondsValue)

    def setUTCMinutes(self, minutesValue, secondsValue=None, msValue=None):
        """Set the UTC minute component and optionally seconds and milliseconds."""
        return _setters.setUTCMinutes(self, minutesValue, secondsValue, msValue)

    def setUTCMonth(self, monthValue, dateValue=None):
        """Set the UTC month with zero-based numbering and optionally the day of the month."""
        return _setters.setUTCMonth(self, monthValue, dateValue)

    def setUTCSeconds(self, secondsValue, msValue=None):
        """Set the UTC second component and optionally milliseconds."""
        return _setters.setUTCSeconds(self, secondsValue, msValue)

    def setYear(self, yearValue):
        """Set the legacy local year value. Deprecated; prefer setFullYear()."""
        return _setters.setYear(self, yearValue)