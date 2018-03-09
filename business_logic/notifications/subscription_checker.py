import base.singleton as sn
import business_logic.message_routing.message_router as message_router
import business_logic.data_processing.my_data as my_data
import business_logic.data_processing.world_data as world_data
import datetime
import business_logic.data_tags as tags
import config
import time


import threading


class SubscriptionChecker(sn.Singleton):
    def __init__(self):
        self.my_data = my_data.MyData.get_instance()
        self.check_period_seconds = 60 * 1
        self.single_subscription_period_seconds = 60 * 60
        self.message_router: message_router.MessageRouter = message_router.MessageRouter.get_instance()
        self.world_data: world_data.WorldData = world_data.WorldData.get_instance()
        self.last_time_triggered = {ticker: datetime.datetime.now() - datetime.timedelta(hours=1) for ticker in config.companies.keys()}

    def check_all(self):
        subscriptions = self.my_data.get_subscriptions()
        for sub in subscriptions:
            self.check_one(sub)

    def start(self):
        def checker():
            while True:
                self.check_all()
                time.sleep(self.check_period_seconds)

        th = threading.Thread(target=checker)
        th.daemon = True
        th.start()

    def check_one(self, sub):
        if sub["type"] == tags.SubType.industry:
            self.check_industry(sub)
        else:
            self.check_stock(sub)

    def check_stock(self, sub):
        ticker = sub["ticker"]

        time_now = datetime.datetime.now()
        last_time_triggered = self.last_time_triggered[ticker]
        old_price = self.world_data.get_price(ticker, last_time_triggered)
        price = self.world_data.get_price(ticker, time_now)

        if price is None or old_price is None:
            return

        difference = (price - old_price) / old_price

        if abs(difference) < sub["threshold"]:
            return

        self.last_time_triggered[ticker] = time_now

        response = {
            'type': tags.OutgoingMessageType.notification,
            'data': {
                'body': "{} changed by {:2.1f}% since {}".format(ticker, difference * 100, last_time_triggered),
                'mime_type': tags.MimeTypes.text
            },
            'additional_data': {
                'old_price': old_price,
                'current_price': price,
                'ticker': ticker
            }
        }

        self.message_router.send(response)

    def check_industry(self, sub):
        tickers = sub["tickers"]
        industry_name = sub["name"]
        time_now = datetime.datetime.now()
        time_one_hour_ago = time_now - datetime.timedelta(hours=1)

        tolerance = 0.5 * 0.01

        ups = []
        downs = []
        same = []
        differences = {}
        for ticker in tickers:
            old_price = self.world_data.get_price(ticker, time_one_hour_ago)
            price = self.world_data.get_price(ticker, time_now)

            if price is None or old_price is None:
                continue

            difference = (price - old_price) / old_price
            differences[ticker] = difference

            if abs(difference) < tolerance:
                same.append(ticker)
            else:
                if difference < 0:
                    downs.append(ticker)
                else:
                    ups.append(ticker)

        exceptional = None
        if len(ups) == 1 and len(downs) == 0:
            exceptional = ups[0]
        elif len(ups) == 0 and len(downs) == 1 :
            exceptional = downs[0]
        else:
            return

        response = {
            'type': tags.OutgoingMessageType.notification,
            'data': {
                'body': "{} in {} changed by {:2.1f}% since {}, opposite to the current trend".format(exceptional,
                                                                       industry_name,
                                                                       differences[exceptional] * 100,
                                                                       time_one_hour_ago),
                'mime_type': tags.MimeTypes.text
            },
            'additional_data': {
                'exceptional_ticker': exceptional,
                'differences': differences,
                'industry_name': industry_name
            }
        }

        self.message_router.send(response)