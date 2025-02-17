import re
from pandas import isnull, isna


def validate_id(value, nan=True):
    if isnull(value) or isna(value) or value is None:
        return nan

    return bool(re.match(r"^[1-9]\d*$", str(value)))


def validate_str(value, nan=True):
    if isnull(value) or isna(value) or value is None:
        return nan

    return bool(re.match(r"^[a-zA-Z\s]+$", str(value)))


def validate_ts(value, nan=True):
    if isnull(value) or isna(value) or value is None:
        return nan

    return bool(re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', str(value)))


def check_data(data: dict):
    check = True

    for key, value in data.items():

        if key in [
            "department_name", "first_name", "last_name",
        ]:
            if not validate_str(value):
                check = False

        elif key in [
            "department_id", "enrollment_id", "worker_id", "job_id",
        ]:
            if not validate_id(value):
                check = False

        elif key in [
            "enrollment_ts", "enrolled_ts"
        ]:
            if not validate_ts(value):
                check = False

    return check
