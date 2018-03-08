import config as conf
import base.singleton as sn
import business_logic.data_tags as tags

import json
import re
import base.log as l


logger = l.Logger('PatternBasedExtractor')


class PatternBasedExtractor(sn.Singleton):

    patterns_keys = [tags.SubType.news, tags.SubType.social_media, tags.SubType.stock, tags.SubType.industry]
    patterns = {
        tags.SubType.news: ['news', 'information', 'headlines'],
        tags.SubType.social_media: ['think', 'talk', 'social'],
        tags.SubType.stock: ['price', 'much', 'stock', 'variance', 'behaviour', 'volatility', 'perform', 'rise', 'fall', 'behave', 'move'],
        tags.SubType.industry: ['industry', 'sector']
    }

    indicators_for_behaviour = [
            tags.Indicator.stock_volatility,
            tags.Indicator.price_change,
            tags.Indicator.just_price
    ]

    patterns_for_indicators = {
        'behaviour': indicators_for_behaviour,
        'behaving': indicators_for_behaviour,
        'behaves': indicators_for_behaviour,
        'change': [tags.Indicator.price_change],
        'volatility': [tags.Indicator.stock_volatility],
        'variance': [tags.Indicator.stock_volatility],
    }

    time_patterns = {
        'hour': tags.TimePeriods.hour,
        'today': tags.TimePeriods.day,
        'day': tags.TimePeriods.day,
        'week': tags.TimePeriods.week,
        'month': tags.TimePeriods.month
    }

    pattern_nodes_opinion_on = ['about', 'for', 'of', 'on']

    # basic predefined commands including pattern words and company name or industry name
    def get_meaning_from_using_patterns(self, string):
        result = self.check_news(string)

        if result is None:
            result = self.check_social_media(string)
        if result is None:
            result = self.check_stock_price(string)

        return result

    def check_stock_price(self, string):
        words = re.sub(r'[^\w\s]','',string.lower()).split()

        if len(set(words).intersection(
                   set(self.patterns[tags.SubType.industry]).union(
                        set(self.patterns[tags.SubType.stock])))) == 0:
            return None

        # is_industry = self.is_about_industry_words_list(words)
        if self.find_industry_from_string(string) is not None:
            is_industry = True
        else:
            is_industry = None
        industry_id = -1
        if is_industry:
            industry_id = self.find_industry_from_string(string)
            ticker = self.get_industry_tickers_by_id(industry_id)
        else:
            ticker = self.find_company_ticker_from_string(string)

        indicators = self.check_stock_price_indicator(words)
        time = self.check_stock_price_time(words)
        if len(indicators) == 0:
            if is_industry:
                indicators = [tags.Indicator.industry_average]
            else:
                indicators = [tags.Indicator.just_price]

        req = {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry if is_industry else tags.SubType.stock,
            'indicators' : indicators,
            'time': time,
            'tickers': ticker,
        }
        if is_industry:
            req["industry"] = industry_id

        req = self.null_on_empty_information(req)
        return req

    def is_about_industry_words_list(self, words):
        if "social" in words and "media" in words:
            words.remove("media") # to break possible media industry pattern

        is_industry = False
        for word in words:
            if word in self.patterns[tags.SubType.industry]:
                is_industry = True
                break
        return is_industry

    def check_stock_price_indicator(self, words):
        indicators = []
        for w in words:
            if w in self.patterns_for_indicators.keys():
                indicators.extend(self.patterns_for_indicators[w])
        return indicators

    def check_stock_price_time(self, words):
        time = tags.TimePeriods.default_time_period
        for word in words:
            if word in self.time_patterns.keys():
                time = self.time_patterns[word]
                break
        return time

    def check_news(self, string):
        words = re.sub(r'[^\w\s]', '', string).split()

        if len(set(words).intersection(set(self.patterns[tags.SubType.news]))) == 0:
            return None

        is_industry = self.is_about_industry_words_list(words)
        if is_industry:
            industry_id = self.find_industry_from_string(string)
            keywords = [word for word in conf.industries[industry_id][0].replace("&", " ").split(" ") if len(word) > 0]
        else:
            tickers = self.find_company_ticker_from_string(string)
            keywords = [conf.companies[t][0] for t in tickers]

        req = {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.news,
            'keywords': keywords
        }

        req = self.null_on_empty_information(req)
        return req

    def check_social_media(self, string):
        words = re.sub(r'[^\w\s]', '', string).split()
        if 'social media' in string:
            words.append('social media')

        if len(set(words).intersection(set(self.patterns[tags.SubType.social_media]))) == 0:
            return None

        is_industry = self.is_about_industry_words_list(words)
        if is_industry:
            industry_id = self.find_industry_from_string(string)
            keywords = [word for word in conf.industries[industry_id][0].replace("&", " ").split(" ") if len(word) > 0]
        else:
            tickers = self.find_company_ticker_from_string(string)
            keywords = [conf.companies[t][0] for t in tickers]

        req = {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.social_media,
            'keywords': keywords
        }
        req = self.null_on_empty_information(req)
        return req

    def find_company_name_from_string(self, string):
        input = string.lower()
        company = []

        for c in conf.companies.keys():
            variations = [x.lower() for x in conf.companies[c]]
            for comp in variations:
                if comp in input:
                    company.append(comp)
                    break

        return company

    def find_company_ticker_from_string(self, string):
        input = string.lower()
        company = []

        for c in conf.companies.keys():
            alternatives = [x.lower() for x in conf.companies[c]]
            for comp in alternatives:
                if comp in input:
                    company.append(c)
                    break

        return company

    def find_industry_from_array(self, data):
        industries = []
        for word in data:
            industries.extend(self.find_industry_from_string(word))
        return industries

    def find_industry_from_string(self, string):
        lower_string = string.lower()
        for id in conf.industries.keys():
            alternatives = conf.industries[id]
            for alt in alternatives:
                if alt.lower() in lower_string:
                    return id
        return None

    def get_industry_tickers_by_id(self, industry_number):
        if industry_number is None:
            return None
        return conf.industry_companies[industry_number]


    def null_on_empty_information(self, req):
        for field in req.keys():
            val = req[field]
            if val is None or ((type(val) is list or type(val) is str) and len(val) == 0):
                logger.log("missing some data in {}".format(req))
                return None
        return req


if __name__ == '__main__':
    print('social' in 'social media')