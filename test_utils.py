import unittest
import datetime
import pytz

from utils.utils import timeframe_to_seconds, get_count_timeframes


PERIOD_IN_DAYS = 3
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
        pass