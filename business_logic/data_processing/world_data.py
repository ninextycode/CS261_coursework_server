import base.singleton as sn
import business_logic.data_tags as tags
import business_logic.data_processing.social_media_analyser as sm_analyser
import business_logic.data_processing.news_analyser as news_analyser
import data_providers.data_wrappers.sql_database_wrapper as sql_connection
import business_logic.data_processing.indicators as indicators
import base.log as l


logger = l.Logger("WorldData")


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

    def get_indicator(self, request):
        if "time_period" not in request.keys():
            request["time_period"] = tags.TimePeriods.default_time_period

        start_time, end_time = request["time_period"].to_interval()
        print(start_time, end_time)

        prices = self.sql_wrapper.get_prices(request["tickers"], True, start_time, end_time)
        logger.log("get prices {}".format(prices))
        value = self.indicators.calculate_indicators(prices, request)
        return value

    def get_prices(self, tickers, time):
        return self.sql_wrapper.get_first_price_before(tickers, time)

    def get_price(self, ticker, time):
        data = self.sql_wrapper.get_first_price_before([ticker], time).reset_index(drop=True)
        if len(data) == 0:
            return None
        return data.loc[0, "Price"]
