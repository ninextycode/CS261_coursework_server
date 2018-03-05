import config as conf
import base.singleton as sn
import business_logic.data_tags as tags

import json
import re
import base.log as l


logger = l.Logger("PatternBasedExtractor")


class PatternBasedExtractor(sn.Singleton):

    patterns_keys = ["news",   "stock_price", "social_media"]
    patterns = {
        "news": ["news", "information", "headlines"],
        "social_media": ["think", "talk", "social"],
        "stock_price": ["price", "much", "stock", "industry", "sector"]
    }
    patterns_for_stock_prices = ["variance", "behaviour", "today", "yesterday"]
    patterns_for_industry = ["industry", "sector"]
    pattern_nodes_opinion_on = ["about", "for", "of", "on"]

    companies = conf.companies
    industries = conf.industries

    # basic predefined commands including pattern words and company name or industry name
    def get_meaning_from_using_patterns(self, string):
        words = re.sub(r"[^\w\s]","",string).split()

        result = self.check_news(string)
        if result is None:
            result = self.check_social_media(string)
        if result is None:
            result = self.check_stock_price(string)

        return result

    def check_stock_price(self, string):
        words = re.sub(r"[^\w\s]","",string.lower()).split()
        indicator = None
        keywords = None
        pattern_keywords = self.patterns["stock_price"]
        patterns_for_industry = self.patterns_for_industry


        for w in words:
            if w in pattern_keywords:

                if w in patterns_for_industry:
                    indicator = tags.Indicator.industry_average
                    keywords = self.find_industry_from_string(string)
                else:
                    indicator = self.check_stock_price_tags(words)
                    keywords = self.find_company_ticker_from_string(string)
                req = {
                    "type": tags.Type.data_request,
                    "subtype": tags.SubType.stock,
                    "indicator" : indicator,
                    "keywords": keywords
                }
                req = self.check_for_empty_information(req)
                return req
        return None

    def check_stock_price_tags(self, words):
        indicator = tags.Indicator.just_price
        for w in words:
            if w in self.patterns_for_stock_prices:
                indicator = w
                break
        return indicator

    def check_news(self, string):
        words = re.sub(r"[^\w\s]", "", string).split()
        indicator = None
        keywords = None
        pattern_keywords = self.patterns["news"]

        for w in words:
            if w in pattern_keywords:
                keywords = self.find_company_name_from_string(string)
                if not keywords:
                    keywords = self.find_industry_from_string(string)
                req = {
                    "type": tags.Type.data_request,
                    "subtype": tags.SubType.news,
                    "indicator": tags.Indicator.news,
                    "keywords": keywords
                }
                req = self.check_for_empty_information(req)
                return req
        return None

    def check_social_media(self, string):
        words = re.sub(r"[^\w\s]", "", string.lower()).split()
        pattern = None
        indicator = None
        keywords = None
        pattern_keywords = self.patterns["social_media"]

        for w in words:
            if str(w) in pattern_keywords or "social media" in string.lower():
                keywords = self.find_company_name_from_string(string)
                if not keywords:
                    keywords = self.find_industry_from_string(string)
                req = {
                    "type": tags.Type.data_request,
                    "subtype": tags.SubType.social_media,
                    "indicator": tags.Indicator.social_media,
                    "keywords": keywords
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

    def check_for_empty_information(self, temp_req):
        temp = None
        for field in temp_req:
            temp = temp_req[field]
            if isinstance(temp, str):
                if temp is None:
                    return None
            if isinstance(temp, list):
                if not temp:
                    return None
        return temp_req

    if __name__ == "__main__":
       print("social" in "social media")