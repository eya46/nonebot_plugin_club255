from datetime import datetime
from time import time
from pytz import timezone


def get_timestamp():
    return int(time())


def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=timezone("Asia/Shanghai"))


def get_now() -> datetime:
    return datetime.now(tz=timezone("Asia/Shanghai"))
