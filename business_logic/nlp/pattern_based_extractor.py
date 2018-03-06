import config as conf
import base.singleton as sn
import business_logic.data_tags as tags

import json
import re
import base.log as l


logger = l.Logger('PatternBasedExtractor')


class PatternBasedExtractor(sn.Singleton):

    patterns_keys = ['news',   'stock_price', 'social_media']
    patterns = {
        'news': ['news', 'information', 'headlines'],
        'social_media': ['think', 'talk', 'social'],
        'stock_price': ['price', 'much', 'stock', 'industry', 'sector', 'variance', 'behaviour', 'volatility']
    }
    patterns_for_stock_prices = {
        'variance': tags.Indicator.stock_variance,
        'behaviour': tags.Indicator.stock_behaviour,
        'change': tags.Indicator.price_change,
        'volatitlity': tags.Indicator.stock_variance
    }

    time_patterns = {
        'hour': tags.TimePeriods.hour,
        'today': tags.TimePeriods.day,
        'day': tags.TimePeriods.day,
        'week': tags.TimePeriods.week,
        'month': tags.TimePeriods.month
    }

    patterns_for_industry = ['industry', 'sector']
    pattern_nodes_opinion_on = ['about', 'for', 'of', 'on']

    companies = conf.companies
    industries = conf.industries

    # basic predefined commands including pattern words and company name or industry name
    def get_meaning_from_using_patterns(self, string):
        words = re.sub(r'[^\w\s]','',string).split()

        result = self.check_news(string)
        if result is None:
            result = self.check_social_media(string)
        if result is None:
            result = self.check_stock_price(string)

        return result

    def check_stock_price(self, string):
        words = re.sub(r'[^\w\s]','',string.lower()).split()
        indicator = None
        keywords = None
        pattern_keywords = self.patterns['stock_price']
        patterns_for_industry = self.patterns_for_industry


        for word in words:
            if word in pattern_keywords:
                industry = False
                indicator = self.check_stock_price_tags(words)
                time = self.check_stock_price_time(words)
                for w in words:
                    if w in patterns_for_industry:
                        industry = True
                        keywords = self.find_industry_from_string(string)
                if not industry:
                    keywords = self.find_company_ticker_from_string(string)
                req = {
                    'type': tags.Type.data_request,
                    'subtype': tags.SubType.stock,
                    'Industry': industry,
                    'indicator' : indicator,
                    'time': time,
                    'ticker': keywords
                }
                print(req)
                req = self.check_for_empty_information(req)
                return req
        return None

    def check_stock_price_tags(self, words):
        indicator = tags.Indicator.price_change
        for w in words:
            if w in self.patterns_for_stock_prices:
                indicator = w
                break
        return indicator

    def check_stock_price_time(self, words):
        time = tags.TimePeriods.day
        for word in words:
            if word in self.time_patterns.keys():
                time = self.time_patterns[word],
                break
        return time


    def check_news(self, string):
        words = re.sub(r'[^\w\s]', '', string).split()
        indicator = None
        keywords = None
        pattern_keywords = self.patterns['news']

        for w in words:
            if w in pattern_keywords:
                keywords = self.find_company_name_from_string(string)
                if not keywords:
                    keywords = self.find_industry_from_string(string)
                req = {
                    'type': tags.Type.data_request,
                    'subtype': tags.SubType.news,
                    'keywords': keywords
                }
                req = self.check_for_empty_information(req)
                return req
        return None

    def check_social_media(self, string):
        words = re.sub(r'[^\w\s]', '', string.lower()).split()
        pattern = None
        indicator = None
        keywords = None
        pattern_keywords = self.patterns['social_media']

        for w in words:
            if str(w) in pattern_keywords or 'social media' in string.lower():
                keywords = self.find_company_name_from_string(string)
                if not keywords:
                    keywords = self.find_industry_from_string(string)
                req = {
                    'type': tags.Type.data_request,
                    'subtype': tags.SubType.social_media,
                    'keywords': keywords
                }
                req = self.check_for_empty_information(req)
                return req
        return None

    def find_company_name_from_string(self, string):
        input = string.lower()
        company = []

        for c in self.companies.keys():
            variations = [x.lower() for x in self.companies[c]]
            for comp in variations:
                if comp in input:
                    company.append(comp)
                    break

        return company

    def find_company_ticker_from_string(self, string):
        input = string.lower()
        company = []

        for c in self.companies.keys():
            alternatives = [x.lower() for x in self.companies[c]]
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
        input = string.lower()
        industry = []

        for i in self.industries.keys():
            alternatives = self.industries[i]
            for ind in alternatives:
                if ind.lower() in input:
                    industry.append(self.industries[i][0])
                    break

        return industry

    def check_for_empty_information(self, req):
        for field in req.keys():
            val = req[field]
            if val is None:
                return None
            if (type(val) is list or type(val) is str) and len(val) == 0:
                return None
        return req


    if __name__ == '__main__':
       print('social' in 'social media')