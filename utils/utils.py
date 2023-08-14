from datetime import datetime


SECONDS_IN_MINUTES = 60
MINUTES_IN_HOURS = 60
HOURS_IN_DAY = 24


def datetime_as_int(datetime: datetime) -> int:
    return int(round(datetime.timestamp()))


def timeframe_to_seconds(timeframe: str) -> int:
    try:
        timeframe_without_str_part = int(timeframe[:-1:])

        if timeframe_without_str_part <= 0:
            raise ValueError(f'Got unexpected value {timeframe}. Expects values like 5m, 1h, 3d')

        match timeframe[len(timeframe) - 1].lower():
            case 'm':
                return timeframe_without_str_part * SECONDS_IN_MINUTES
            case 'h':
                return timeframe_without_str_part * MINUTES_IN_HOURS * SECONDS_IN_MINUTES
            case 'd':
                return timeframe_without_str_part * HOURS_IN_DAY * MINUTES_IN_HOURS * SECONDS_IN_MINUTES
            case _:
                raise ValueError(f'Got unexpected valuse {timeframe}. Expects values like 5m, 1h, 3d')
    except ValueError:
        print(f'Got unexpected value {timeframe}. Expects values like 5m, 1h, 3d')
    except Exception as ex:
        print(f'Got unexpected error: {ex}')

def get_count_timeframes(start: datetime, end: datetime, timeframe: str = '15m') -> int:
    return int((datetime_as_int(end) - datetime_as_int(start)) / timeframe_to_seconds(timeframe))


# def get_count_requests(start: datetime, end: datetime, timeframe: str = '15m', rate_limit: int = 100) -> int:
#     return int(get_count_timeframes(start, end, timeframe) / rate_limit) + 1 # +1 для нецелых timeframe


def get_time_points(start: datetime, end: datetime, timeframe: str = '15m', rate_limit: int = 100) -> list[int]:
    timeframes = []
    for t in range(get_count_timeframes(start, end, timeframe)):
        value = datetime_as_int(start) + t * timeframe_to_seconds(timeframe)
        timeframes.append(value)
    return [t for n, t in enumerate(timeframes) if n % rate_limit == 0]