from __future__ import annotations

from datetime import timezone
from email.utils import format_datetime
import math

_WEEKDAY_ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _is_valid_date(self) -> bool:
    try:
        return getattr(self, '_dt', None) is not None and not math.isnan(self.valueOf())
    except Exception:
        return False


def _invalid_date() -> str:
    return "Invalid Date"


def toDateString(self) -> str:
    if not _is_valid_date(self):
        return _invalid_date()
    dt = self._dt.astimezone()
    return f"{_WEEKDAY_ABBR[dt.weekday()]} {_MONTH_ABBR[dt.month - 1]} {dt.day:02d} {dt.year:04d}"


def toISOString(self) -> str:
    if not _is_valid_date(self):
        raise ValueError("Invalid Date")
    dt_utc = self._dt.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt_utc.microsecond // 1000:03d}Z"


def toJSON(self):
    if not _is_valid_date(self):
        return None
    return toISOString(self)


def toLocaleDateString(self) -> str:
    if not _is_valid_date(self):
        return _invalid_date()
    return self._dt.astimezone().strftime("%x")


def toLocaleString(self) -> str:
    if not _is_valid_date(self):
        return _invalid_date()
    return self._dt.astimezone().strftime("%c")


def toLocaleTimeString(self) -> str:
    if not _is_valid_date(self):
        return _invalid_date()
    return self._dt.astimezone().strftime("%X")


def toTimeString(self) -> str:
    if not _is_valid_date(self):
        return _invalid_date()
    dt = self._dt.astimezone()
    tz_name = dt.tzname() or "Local"
    offset = dt.utcoffset()
    if offset is None:
        offset_text = "+0000"
    else:
        total_minutes = int(offset.total_seconds() // 60)
        sign = "+" if total_minutes >= 0 else "-"
        total_minutes = abs(total_minutes)
        hh, mm = divmod(total_minutes, 60)
        offset_text = f"{sign}{hh:02d}{mm:02d}"
    return f"{dt.strftime('%H:%M:%S')} GMT{offset_text} ({tz_name})"


def toString(self) -> str:
    if not _is_valid_date(self):
        return _invalid_date()
    return f"{toDateString(self)} {toTimeString(self)}"


def toUTCString(self) -> str:
    if not _is_valid_date(self):
        return _invalid_date()
    return format_datetime(self._dt.astimezone(timezone.utc), usegmt=True)


def toGMTString(self) -> str:
    return toUTCString(self)

