from datetime import datetime

FORMAT = "%d %B %Y"

def to_datetime(date_string, date_format=FORMAT):
    return datetime.strptime(date_string, date_format)

def french_format_to_datetime(date_string):
    return datetime.strptime(date_string, "%d/%m/%Y")

def datetime_to_string(date, date_format=FORMAT):
    """
    Converts datetime to string
    """
    return date.strftime(date_format)