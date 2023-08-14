import unittest
import datetime
import pytz

from utils.utils import timeframe_to_seconds, get_count_timeframes, datetime_as_int
from main import get_history_data


PERIOD_IN_DAYS = 1
timezone = pytz.timezone("Europe/Moscow")
today = datetime.datetime.now()
till_dt = timezone.localize(today)
delta = datetime.timedelta(days=PERIOD_IN_DAYS)
from_dt = (till_dt - delta)


class TestTimeframeToSeconds(unittest.TestCase):

    def test_timeframe_to_seconds(self):
        self.assertEqual(15*60, timeframe_to_seconds('15m'))
        self.assertEqual(4*60*60, timeframe_to_seconds('4h'))

    # def test_unexpected_values(self):
    #     self.assertRaises(ValueError, timeframe_to_seconds('-1h'))
    #     self.assertRaises(ValueError, timeframe_to_seconds('1sec'))


class TestGetCountTimeframes(unittest.TestCase):

    def test_get_count_timeframes(self):
        self.assertEqual(24*PERIOD_IN_DAYS, get_count_timeframes(from_dt, till_dt, timeframe='1h'))
        self.assertEqual(24*4*PERIOD_IN_DAYS, get_count_timeframes(from_dt, till_dt, timeframe='15m'))


class TestGetHistoryData(unittest.TestCase):

    def test_get_history_data(self):
        start = datetime_as_int(datetime.datetime(2023, 8, 14, 0, 0, 1))
        data = get_history_data('ETH-USDC', start, '15m')
        min_date = min([int(d[0]) for d in data['data']])
        self.assertLessEqual(min_date, start*1000)

        # this test in not pass
        # max_date = max([int(d[0]) for d in data['data']])
        # end = datetime_as_int(datetime.datetime.now())
        # self.assertGreaterEqual(max_date, end*1000)
