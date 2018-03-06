import base.singleton as sn
import business_logic.data_tags as tags


class Indicator(sn.Singleton):
    def calculate_indicator(self, prices, indicator):
        if indicator == tags.Indicator.industry_average:
            self.get_average(prices)

        if indicator == tags.Indicator.price_change:
            self.get_price_change(prices)

        if indicator == tags.Indicator.stock_volatility:
            self.get_volatility(prices)

        if indicator == tags.Indicator.just_price:
            self.get_just_price(prices)