import base.singleton as sn
import data_providers.data_wrappers.json_database_connection as jdc

import config

import re
import datetime


class MyData(sn.Singleton):
    def __init__(self):
        self.json_connection: jdc.JsonDatabaseConnection = jdc.JsonDatabaseConnection.get_instance()

    def add_request(self, request_data):
        copy = {**request_data}
        self.json_connection.insert_one(copy, collection="requests")

    def get_subscriptions(self):
        return self.json_connection.find({}, "subscriptions")

    def count_request_with_this_keyword(self, keyword):
        ticker = config.get_ticker(keyword)

        if keyword in config.companies.keys():
            ticker = keyword
            keyword = config.companies["ticker"][0]

        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        escape = r"^{}$"
        ticker_pattern = escape.format(ticker)
        keyword_pattern = escape.format(keyword)

        request = {
            "$or": [
                {
                    "tickers": re.compile(ticker_pattern, re.IGNORECASE)
                }, {
                    "keywords": re.compile(keyword_pattern, re.IGNORECASE)
                }
            ],
            "time": {
                "$gte": yesterday
            }
        }
        print(request)
        return self.json_connection.count(request)


if __name__ == "__main__":
    conn = MyData.get_instance()
    print(conn.count_request_with_this_keyword("tesco"))

