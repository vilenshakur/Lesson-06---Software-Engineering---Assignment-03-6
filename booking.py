"""Room availability check for the Smart Campus prototype (AC1-AC5).

Times are integer minutes after midnight. The function is pure: it never
modifies its arguments.
"""

MINUTES_PER_DAY = 1440
MAX_DURATION = 120


def _is_int(value):
    # bool is a subclass of int in Python; True/False are not valid minutes.
    return isinstance(value, int) and not isinstance(value, bool)


def can_book(start, end, now, blocked, existing):
    """Return True only if the candidate interval [start, end) is bookable.

    start, end -- candidate times, integer minutes after midnight
    now        -- current time, assumed valid (0..1439)
    blocked    -- True if the selected room is blocked
    existing   -- iterable of (start, end) tuples for existing bookings
    """
    # AC3: a blocked room rejects every request.
    if blocked:
        return False

    # AC1: integer minutes, 0 <= start < end <= 1440.
    if not (_is_int(start) and _is_int(end)):
        return False
    if not (0 <= start < end <= MINUTES_PER_DAY):
        return False

    # AC1: start must be strictly after now (starting exactly now is invalid).
    if start <= now:
        return False

    # AC2: at most 120 minutes; exactly 120 is permitted.
    if end - start > MAX_DURATION:
        return False

    # AC4: reject overlap. Half-open intervals, so touching endpoints
    # (end == other start, or start == other end) do not overlap.
    for booked_start, booked_end in existing:
        if start < booked_end and booked_start < end:
            return False

    return True
