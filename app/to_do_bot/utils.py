from datetime import datetime


def parse_date(date_string):
    possible_formats = ["%d%m%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]
    for date_format in possible_formats:
        try:
            return datetime.strptime(date_string, date_format).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_string}")


def parse_time(time_string):
    try:
        return datetime.strptime(time_string, '%H:%M:%S').time()
    except ValueError:
        try:
            return datetime.strptime(time_string, '%H:%M').time()
        except ValueError:
            try:
                return datetime.strptime(time_string, '%H').time()
            except ValueError:
                try:
                    return datetime.strptime(time_string, '%H-%M-%S').time()
                except ValueError:
                    try:
                        return datetime.strptime(time_string, '%H-%M').time()
                    except ValueError:
                        raise ValueError(f"Invalid time format: {time_string}")
