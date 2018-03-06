import datetime


class Type:
    data_request = 'data_request'
    subscription = 'subscription'


class SubType:
    social_media = 'social_media'
    news = 'news'
    stock = 'stock'
    industry = "industry"

class Indicator:
    just_price = "just_price"
    industry_average = 'industry_average'
    price_change = 'price_change'
    stock_volatility = 'stock_variance'

class Mood:
    positive = 'positive'
    neutral = 'neutral'
    negative = 'negative'


class OutgoingMessageType:
    response = 'response'
    on_unknown_request = 'unknown_request'
    on_exception = 'exception'


class MimeTypes:
    text = 'text/plain'
    ogg = 'audio/ogg'
    flac = 'audio/flac'


class TimePeriods:
    class RightNow:
        def to_interval(self, time=datetime.datetime.now()):
            end = time.replace(microsecond=0, second=0)
            start = end

            return [start, end.replace(minute=end.minute + 1)]

        def __str__(self):
            return "right_now"

        def __repr__(self):
            return str(self)

    class Hour:
        def to_interval(self, time=datetime.datetime.now()):
            end = time.replace(microsecond=0, second=0)
            start = end.replace(hour=end.hour-1)

            return [start, end.replace(minute=end.minute + 1)]

        def __str__(self):
            return "hour"

        def __repr__(self):
            return str(self)

    class Day:
        def to_interval(self, time=datetime.datetime.now()):
            end = time.replace(microsecond=0, second=0)
            start = end.replace(day=end.day, hour=0, minute=0)

            return [start, end.replace(minute=end.minute + 1)]

        def __str__(self):
            return "day"

        def __repr__(self):
            return str(self)

    class Week:
        def to_interval(self, time=datetime.datetime.now()):
            end = time.replace(microsecond=0, second=0)
            start = end.replace(day=end.day - end.isoweekday()+1, hour=0, minute=0)

            return [start, end.replace(minute=end.minute + 1)]

        def __str__(self):
            return "week"

        def __repr__(self):
            return str(self)

    class Month:
        def to_interval(self, time=datetime.datetime.now()):
            end = time.replace(microsecond=0, second=0)
            start = end.replace(month=end.month, hour=0, minute=0, day=1)

            return [start, end.replace(minute=end.minute + 1)]

        def __str__(self):
            return "month"

        def __repr__(self):
            return str(self)

    right_now = RightNow()
    hour = Hour()
    day = Day()
    week = Week()
    month = Month()
    default_time_period = day

if __name__=='__main__':
    time = datetime.datetime(2018, 2, 14, 10, 32, 21, 0)
    expected = [
        [datetime.datetime(2018, 2, 14, 10, 32, 0, 0), datetime.datetime(2018, 2, 14, 10, 33, 0, 0)],
        [datetime.datetime(2018, 2, 14, 9, 32, 0, 0), datetime.datetime(2018, 2, 14, 10, 33, 0, 0)],
        [datetime.datetime(2018, 2, 14, 0, 0, 0, 0), datetime.datetime(2018, 2, 14, 10, 33, 0, 0)],
        [datetime.datetime(2018, 2, 12, 0, 0, 0, 0), datetime.datetime(2018, 2, 14, 10, 33, 0, 0)],
        [datetime.datetime(2018, 2, 1, 0, 0, 0, 0), datetime.datetime(2018, 2, 14, 10, 33, 0, 0)],
    ]
    testers = [
        TimePeriods.right_now,
        TimePeriods.hour,
        TimePeriods.day,
        TimePeriods.week,
        TimePeriods.month,
    ]

    for i, tester in enumerate(testers):
        actual = tester.to_interval(time)
        print(expected[i], '\t', actual, '\t', expected[i]==actual)
