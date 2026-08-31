from __future__ import annotations

from datetime import timezone
import math


def _is_valid_date(value) -> bool:
    return getattr(value, '_dt', None) is not None and not math.isnan(value.valueOf())


def getDate(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().day


def getDay(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return (self._dt.astimezone().weekday() + 1) % 7


def getFullYear(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().year


def getHours(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().hour


def getMilliseconds(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().microsecond // 1000


def getMinutes(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().minute


def getMonth(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().month - 1


def getSeconds(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().second


def getTime(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self.valueOf()


def getTimezoneOffset(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    offset = self._dt.astimezone().utcoffset()
    if offset is None:
        return math.nan
    return -int(offset.total_seconds() // 60)


def getUTCDate(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone(timezone.utc).day


def getUTCDay(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return (self._dt.astimezone(timezone.utc).weekday() + 1) % 7


def getUTCFullYear(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone(timezone.utc).year


def getUTCHours(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone(timezone.utc).hour


def getUTCMilliseconds(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone(timezone.utc).microsecond // 1000


def getUTCMinutes(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone(timezone.utc).minute


def getUTCMonth(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone(timezone.utc).month - 1


def getUTCSeconds(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone(timezone.utc).second


def getYear(self) -> int | float:
    if not _is_valid_date(self):
        return math.nan
    return self._dt.astimezone().year - 1900