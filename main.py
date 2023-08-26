import datetime
import time
import json
import pytz

import okx.MarketData as MarketData

from utils.utils import get_time_points, timeframe_to_seconds

timezone = pytz.timezone("Europe/Moscow")
TICKER = 'ETH-USDC'
PERIOD_IN_DAYS = 5
FLAG = '0'  # live trading: 0, demo trading: 1
SLEEP_PER_REQUEST_IN_SEC = 1
marketDataAPI = MarketData.MarketAPI(flag=FLAG, debug=False)

# todo: крайние 2+ дня отсутствую в выборке
# todo: save data to DB
# todo: get data from DB
# todo: convert script as FastApi app
# todo: get diff between DB and request from OKX (with saveving to DB)
# todo: add request get tickers
# todo: если модальная цена измелась сильно - пора выходить из позиций


def main():
    today = datetime.datetime.now()
    till_dt = timezone.localize(today)
    delta = datetime.timedelta(days=PERIOD_IN_DAYS)
    from_dt = (till_dt - delta)

    time_points = get_time_points(start=from_dt, end=till_dt, timeframe='15m', rate_limit=100)
    data = collect_data(time_points, timeframe='15m', rate_limit=100)
    json_data = json.dumps(data)
    with open(f'output_{PERIOD_IN_DAYS}.json', 'w') as file:
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
        time.sleep(SLEEP_PER_REQUEST_IN_SEC)
        print(f'Load batch #{p+1} from {len(time_points)}')
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
        print(f'Got error: {err}. Could be an empty answer from API?')
    except Exception as ex:
        print(f'Got unexpected error {ex}')


if __name__ == '__main__':
    main()
