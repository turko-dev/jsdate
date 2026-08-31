from __future__ import annotations

from datetime import datetime, timedelta, timezone
import math


def _timestamp_ms(dt: datetime) -> int:
    return int(dt.astimezone(timezone.utc).timestamp() * 1000)


def _local_dt(self) -> datetime:
    return self._dt.astimezone()


def _utc_dt(self) -> datetime:
    return self._dt.astimezone(timezone.utc)


def _invalidate(self):
    self._dt = None
    return math.nan


def _set_local_components(self, year=None, month_index=None, day=None, hour=None, minute=None, second=None, millisecond=None):
    try:
        current = _local_dt(self)
        year = current.year if year is None else int(year)
        month_index = (current.month - 1) if month_index is None else int(month_index)
        day = current.day if day is None else int(day)
        hour = current.hour if hour is None else int(hour)
        minute = current.minute if minute is None else int(minute)
        second = current.second if second is None else int(second)
        millisecond = (current.microsecond // 1000) if millisecond is None else int(millisecond)

        if 0 <= year <= 99:
            year += 1900

        year += month_index // 12
        month_index = month_index % 12
        month = month_index + 1

        base = datetime(year, month, 1, tzinfo=current.tzinfo)
        result = base + timedelta(
            days=day - 1,
            hours=hour,
            minutes=minute,
            seconds=second,
            milliseconds=millisecond,
        )
        self._dt = result.astimezone()
        return _timestamp_ms(self._dt)
    except Exception:
        return _invalidate(self)


def _set_utc_components(self, year=None, month_index=None, day=None, hour=None, minute=None, second=None, millisecond=None):
    try:
        current = _utc_dt(self)
        year = current.year if year is None else int(year)
        month_index = (current.month - 1) if month_index is None else int(month_index)
        day = current.day if day is None else int(day)
        hour = current.hour if hour is None else int(hour)
        minute = current.minute if minute is None else int(minute)
        second = current.second if second is None else int(second)
        millisecond = (current.microsecond // 1000) if millisecond is None else int(millisecond)

        if 0 <= year <= 99:
            year += 1900

        year += month_index // 12
        month_index = month_index % 12
        month = month_index + 1

        base = datetime(year, month, 1, tzinfo=timezone.utc)
        result_utc = base + timedelta(
            days=day - 1,
            hours=hour,
            minutes=minute,
            seconds=second,
            milliseconds=millisecond,
        )
        self._dt = result_utc.astimezone()
        return _timestamp_ms(self._dt)
    except Exception:
        return _invalidate(self)


def setDate(self, dateValue):
    return _set_local_components(self, day=dateValue)


def setFullYear(self, yearValue, monthValue=None, dateValue=None):
    return _set_local_components(self, year=yearValue, month_index=monthValue, day=dateValue)


def setHours(self, hoursValue, minutesValue=None, secondsValue=None, msValue=None):
    return _set_local_components(self, hour=hoursValue, minute=minutesValue, second=secondsValue, millisecond=msValue)


def setMilliseconds(self, millisecondsValue):
    return _set_local_components(self, millisecond=millisecondsValue)


def setMinutes(self, minutesValue, secondsValue=None, msValue=None):
    return _set_local_components(self, minute=minutesValue, second=secondsValue, millisecond=msValue)


def setMonth(self, monthValue, dateValue=None):
    return _set_local_components(self, month_index=monthValue, day=dateValue)


def setSeconds(self, secondsValue, msValue=None):
    return _set_local_components(self, second=secondsValue, millisecond=msValue)


def setTime(self, timeValue):
    try:
        ts = float(timeValue)
        self._dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).astimezone()
        return int(ts) if ts.is_integer() else ts
    except Exception:
        return _invalidate(self)


def setUTCDate(self, dateValue):
    return _set_utc_components(self, day=dateValue)


def setUTCFullYear(self, yearValue, monthValue=None, dateValue=None):
    return _set_utc_components(self, year=yearValue, month_index=monthValue, day=dateValue)


def setUTCHours(self, hoursValue, minutesValue=None, secondsValue=None, msValue=None):
    return _set_utc_components(self, hour=hoursValue, minute=minutesValue, second=secondsValue, millisecond=msValue)


def setUTCMilliseconds(self, millisecondsValue):
    return _set_utc_components(self, millisecond=millisecondsValue)


def setUTCMinutes(self, minutesValue, secondsValue=None, msValue=None):
    return _set_utc_components(self, minute=minutesValue, second=secondsValue, millisecond=msValue)


def setUTCMonth(self, monthValue, dateValue=None):
    return _set_utc_components(self, month_index=monthValue, day=dateValue)


def setUTCSeconds(self, secondsValue, msValue=None):
    return _set_utc_components(self, second=secondsValue, millisecond=msValue)


def setYear(self, yearValue):
    try:
        y = int(yearValue)
        if 0 <= y <= 99:
            y += 1900
        return _set_local_components(self, year=y)
    except Exception:
        return _invalidate(self)