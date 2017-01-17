from datetime import datetime

FORMAT = "%d %B %Y"

def to_datetime(date_string, date_format=FORMAT):
    return datetime.strptime(date_string, date_format)