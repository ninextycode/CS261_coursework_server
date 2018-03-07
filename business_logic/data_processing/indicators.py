import base.singleton as sn
import business_logic.data_tags as tags
import numpy as np


class Indicator(sn.Singleton):
    def calculate_indicators(self, prices, request):
        indicators = request["indicators"]
        data = {}
        for indicator in indicators:
            data[indicator] = self.calculate_indicator(prices, indicator, request["tickers"])
        return data

    def calculate_indicator(self, prices, indicator, tickers):
        if len(prices) == 0:
            return None

        if indicator == tags.Indicator.industry_average:
            return self.get_average(prices, tickers)

        if indicator == tags.Indicator.price_change:
            return self.get_price_changes(prices, tickers)

        if indicator == tags.Indicator.just_price:
            return self.get_just_price(prices, tickers)

        else:
            return None


    def get_average(self, prices, tickers):
        av = 0
        number = 0
        for ticker in tickers:
            subdf = prices.loc[prices["Company_code"] == ticker, "Price"].reset_index(drop=True)
            if len(subdf) == 0:
                continue
            av += subdf[0]
            number += 1
        av /= number
        return {"average": av}

    def get_price_changes(self, prices, tickers):
        diff = {}
        av = 0
        number = 0
        for ticker in tickers:
            subdf = prices.loc[prices["Company_code"] == ticker, "Price"].reset_index(drop=True)
            if len(subdf) == 0:
                continue
            n = len(subdf)
            diff[ticker] = subdf[0] - subdf[n-1]
            av += diff[ticker]
            number += 1
        av /= number
        diff["average"] = av
        return diff

    def get_just_price(self, prices, tickers):
        av = 0
        number = 0
        diff = {}
        for ticker in tickers:
            subdf = prices.loc[prices["Company_code"]==ticker, "Price"].reset_index(drop=True)
            if len(subdf) == 0:
                continue
            diff[ticker] = subdf[0]
            av += diff[ticker]
            number += 1
        av /= number
        diff["average"] = av
        return diff
