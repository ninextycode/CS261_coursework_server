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
        "stock_price": ["price", "much", "stock", "industry", "sector"],
        "social_media": ["think", "talk", "social media"]
    }
    patterns_for_industry = ["industry", "sector"]
    pattern_nodes_opinion_on = ["about", "for", "on"]

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


    def get_meaning_from_using_nlp(self, tree, keywords):
        req = None
        pattern = None
        subtype = None
        nouns = []
        keywords = None
        req = None
        soc_keywords = []

        for n in tree["nodes"]:
            if n.data["part_of_speech"] == 6:  # get nouns
                nouns.append(n.data["lemma"])
            for p in self.patterns:
                if n.data["lemma"] in self.patterns[p]:  # find pattern
                    pattern = p
                    if n.data["lemma"] in self.patterns_for_industry:
                        subtype = tags.Indicator.industry_average
                    if n.data["part_of_speech"] == 6:
                     nouns.remove(n.data["lemma"])

        if pattern == "stock_price":
            indicator = tags.Indicator.just_price
            if subtype is tags.Indicator.industry_average:
                req = {
                    "type": tags.Type.data_request,
                    "subtype": tags.SubType.stock,
                    "indicator": tags.Indicator.industry_average,
                    "keywords": self.find_industry_from_array(nouns)
                }
            else:
                for n in tree["nodes"]:
                    if n.data["text"] in self.patterns_for_stock_prices:
                        indicator = n.data["text"]
                        break
                req =  {
                        "type": tags.Type.data_request,
                        "subtype": tags.SubType.stock,
                        "indicator": indicator,
                        "keywords": self.find_company_name_from_array(nouns)
                    }
        if pattern == "news":
            req = {
                "type": tags.Type.data_request,
                "subtype": tags.SubType.news,
                "indicator": tags.Indicator.news,
                "keywords": nouns
            }

        if pattern == "social_media":
            for n in tree["nodes"]:
                for p in self.pattern_nodes_social_media:
                    if n.data["text"] == p:  # get children of pattern nodes
                        soc_keywords = n.get_predecessors()
                        nouns = []

            for w in soc_keywords:
                if w.data["part_of_speech"] == 6:
                    nouns.append(w.data["text"])

            req = {
                "type": tags.Type.data_request,
                "subtype": tags.SubType.social_media,
                "indicator": tags.Indicator.social_media,
                "keywords": nouns
            }
        if req is not None:
            req = self.check_for_empty_information(req)

        return req


    def find_company_name_from_array(self, array):
        arr = [x.lower() for x in array]
        companies = []
        temp = None

        for c in self.companies:
            temp = str(self.companies[c]).lower()
            for noun in arr:
                if noun in temp:
                    companies.append(c)
                    break

        return companies



    # def get_all_nouns_from_tree(self, tree):
    #     nouns = []
    #     for n in tree["nodes"]:
    #         print(n.data["lemma"] + ", " + str(n.data["part_of_speech"]))
    #         if n.data["part_of_speech"] == 6:
    #             nouns.append(n.data["lemma"])
    #     return nouns
