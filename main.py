import datetime
import time
import json
import pytz

import okx.MarketData as MarketData

from utils.utils import get_time_points, timeframe_to_seconds

timezone = pytz.timezone("Europe/Moscow")
TICKER = 'ETH-USDC'
PERIOD_IN_DAYS = 9
FLAG = '0'  # live trading: 0, demo trading: 1
SLEEP_PER_REQUEST_IN_SEC = 1
marketDataAPI = MarketData.MarketAPI(flag=FLAG, debug=False)


def main():
    today = datetime.datetime.now()
    till_dt = timezone.localize(today)
    delta = datetime.timedelta(days=PERIOD_IN_DAYS)
    from_dt = (till_dt - delta)

    time_points = get_time_points(start=from_dt, end=till_dt, timeframe='15m', rate_limit=100)
    """
    Нужно сделать 3 запросов
    [1691958486, 1691868486, 1691778486]
    12 августа 2023 г., 22:30:00 GMT+03:00 - 13 августа 2023 г., 23:15:00 GMT+03:00
    11 августа 2023 г., 21:30:00 GMT+03:00 - 12 августа 2023 г., 22:15:00 GMT+03:00
    11 августа 2023 г., 21:15:00 GMT+03:00 - 10 августа 2023 г., 20:30:00 GMT+03:00
    """
    data = collect_data(time_points, timeframe='15m', rate_limit=100)
    json_data = json.dumps(data)
    with open('output.json', 'w') as file:
        file.write(json_data)


def collect_data(time_points: list[int], timeframe='15m', rate_limit: int = 100) -> list[list]:
    data = []
    for p in range(len(time_points)):
        history_candles = get_history_data(
            ticker=TICKER,
            start_from=time_points[p],
            timeframe=timeframe,
            limit=rate_limit
            )
        time.sleep(1)
        if history_candles:
            for d in history_candles['data']:
                data.append(d)
    return data


def get_history_data(ticker: str, start_from: int, timeframe: str = '15m', limit: int = 100) -> dict:
    try:
        history_candles = marketDataAPI.get_history_candlesticks(
            instId=ticker,
            bar=timeframe,
            after=(start_from - timeframe_to_seconds(timeframe))*1000,  # use ONLY AFTER, befor is broken
            # Pagination of data to return records earlier than the requested
            limit=limit
            )
        return history_candles
    except IndexError as err:
        print(f'Ошибка {err}')
    except Exception as ex:
        print(f'Got unexpected error {ex}')


if __name__ == '__main__':
    main()
