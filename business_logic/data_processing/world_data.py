import base.singleton as sn

import business_logic.data_processing.social_media_analyser as sm_analyser
import business_logic.data_processing.news_analyser as news_analyser
import data_providers.data_wrappers.sql_database_wrapper as sql_connection
import business_logic.data_processing.indicators as indicator


class WorldData(sn.Singleton):
    def __init__(self):
        self.news_analyser = news_analyser.NewsAnalyser.get_instance()
        self.social_media_analyser = sm_analyser.SocialMediaAnalyser.get_instance()
        self.sql_connection = sql_connection.SqlDatabaseWrapper.get_instance()
        self.indicators = indicator.Indicator.get_instance()

    def get_news(self, json_request):
        return self.news_analyser.get_news(json_request)

    def get_public_opinion(self, json_request):
        return self.social_media_analyser.get_public_opinion(json_request)

    def get_indicator(self, tickers, indicator, time_start, time_end):
        prices = self.sql_connection.get_prices(tickers, time_start, time_end)
        value = self.indicators.calculate_indicator(prices, indicator)

        return value
