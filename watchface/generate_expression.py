import datetime
import random
import time
import zoneinfo


def check(available_tzs: list[str], dt_search: datetime.datetime, needed_offset: int, picky: bool):
    for tz_name in available_tzs:
        if not "/" in tz_name:
            continue
        tz = zoneinfo.ZoneInfo(tz_name)
        dt_local = dt_search.astimezone(tz)
        offset = dt_local.utcoffset()

        if offset.seconds % 3600 != 0 or offset.days < 0 and offset.seconds != 0:
            total_seconds = offset.total_seconds()
            if total_seconds % 3600 != 0:
                continue
        
        offset_hours = int(offset.total_seconds() / 3600)
        
        if offset_hours == needed_offset:
            return tz_name
            abbr = dt_local.strftime("%Z")
            # Keep only clean 3-4 letter alphabetic abbreviations
            if not picky or (abbr.isalpha() and 3 <= len(abbr) <= 4):
                return abbr
    return None

def get_timezone_at_11am(hour_offset: int) -> str:
    dt_utc = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=hour_offset)
    needed_offset = 11 - dt_utc.hour

    dt_now = datetime.datetime.now()
    
    while needed_offset < -12:
        needed_offset += 24
    while needed_offset > 12:
        needed_offset -= 24

    dt_search = dt_utc + datetime.timedelta(hours=needed_offset)

    available_tzs = list(zoneinfo.available_timezones())
    random.shuffle(available_tzs)
    available_tzs.sort(key=lambda x: 1 if "Etc/" in x else 0)

    if tz := check(available_tzs, dt_search, needed_offset, True):
        return tz
    if tz := check(available_tzs, dt_search, needed_offset, False):
        return tz

    raise Exception("HELP!")


if __name__ == "__main__":
    start_hours = 490_885 # 1 January 2026
    end_hours = start_hours + (2**17) # 10 years later

    f = open("expression.csv", "w")
    f.write("")
    for i in range(start_hours, end_hours):
        tz = get_timezone_at_11am(i)
        f.write(f"{i}\t{tz}\n")
        # f.write(f"[HOURS_SINCE_EPOCH] == {i} ? &quot;{tz}&quot; : ")
    # f.write("&quot;???&quot;")
    f.close()