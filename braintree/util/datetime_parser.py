import re
from datetime import datetime
from datetime import timedelta


def parse_datetime(timestamp):
    if timestamp[-1] == 'Z':
        timestamp = timestamp.replace('-', '').replace(':', '')
        return datetime.strptime(timestamp, '%Y%m%dT%H%M%SZ')
    else:
        try:
            delta_matches = re.findall(r'(\+|\-)(\d\d):(\d\d)$', timestamp)[0]
            delta_is_negative = delta_matches[0] == '-'
            delta_hours = int(delta_matches[1])
            delta_minutes = int(delta_matches[2])
        except IndexError:
            pass
        parsed = datetime.strptime(timestamp[:-6], '%Y-%m-%dT%H:%M:%S')
        delta = timedelta(hours=delta_hours, minutes=delta_minutes)
        if delta_is_negative:
            return parsed + delta
        else:
            return parsed - delta
