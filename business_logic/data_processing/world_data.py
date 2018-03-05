import base.singleton as sn
import business_logic.data_tags as tags
import business_logic.data_processing.social_media_analyser as sm_analyser
import business_logic.data_processing.news_analyser as news_analyser
import data_providers.data_wrappers.sql_database_wrapper as sql_connection
import business_logic.data_processing.indicators as indicators


class WorldData(sn.Singleton):
    def __init__(self):
        self.news_analyser = news_analyser.NewsAnalyser.get_instance()
        self.social_media_analyser = sm_analyser.SocialMediaAnalyser.get_instance()
        self.sql_wrapper: sql_connection.SqlDatabaseWrapper = sql_connection.SqlDatabaseWrapper.get_instance()
        self.indicators = indicators.Indicator.get_instance()

    def get_news(self, json_request):
        return self.news_analyser.get_news(json_request)

    def get_public_opinion(self, json_request):
        return self.social_media_analyser.get_public_opinion(json_request)

    def get_indicator(self, tickers, indicator, time_period=None):
        if time_period is None:
            time_period = tags.TimePeriods.default_time_period(indicator)

        if indicator == tags.Indicator.just_price:
            return self.get_price(tickers, time_period)

        prices = self.sql_wrapper.get_prices(tickers, time_period)
        value = self.indicators.calculate_indicator(prices, indicator)
        return value

    def get_price(self, tickers, time_period):
        self.sql_wrapper.get_first_price_before(tickers, datetime)
