import config as conf
import base.singleton as sn
import business_logic.nlp.data_tags as tags

import json
import re
import base.log as l


logger = l.Logger("PatternBasedExtractor")

class PatternBasedExtractor(sn.Singleton):

    patterns = {"stock_price": ["price", "much", "industry", "sector"],
                "news": ["news", "information", "headlines"],
                "social_media": ["think", "social media"]
                }
    patterns_for_industry = ["industry", "sector"]
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


    def check_stock_price(self, string):
        words = re.sub(r'[^\w\s]','',string).split()
        pattern = None
        indicator = None
        keyword = None
        pattern_keywords = self.patterns["stock_price"]
        patterns_for_industry = self.patterns_for_industry

        for w in words:
            if w in pattern_keywords: #!!!!!
                pattern = "stock_price" # wrong, need key
                if w in patterns_for_industry:
                    indicator = tags.Indicator.industry_average
                    keyword = self.find_industry_from_string(string)
                else:
                    indicator = tags.Indicator.just_price
                    keyword = self.find_company_name_from_string(string)
                req = {
                    'type': tags.Type.data_request,
                    'subtype': pattern,
                    "indicator" : indicator,
                    'keyword': keyword
                }
                logger.log("Before check: " + str(req))
                req = self.check_for_empty_information(req)
                logger.log("after check: " + str(req))
                return req
        return None

    def check_news(self, string):
        words = re.sub(r'[^\w\s]', '', string).split()
        pattern = None
        indicator = None
        keyword = None
        pattern_keywords = self.patterns["news"]

        for w in words:
            if w in pattern_keywords:
                pattern = w  # wrong, need key
                indicator = tags.Indicator.news
                keyword = self.find_company_name_from_string(string)
                if not keyword:
                    keyword = self.find_industry_from_string(string)
                req = {
                    'type': tags.Type.data_request,
                    'subtype': pattern,
                    "indicator": indicator,
                    'keyword': keyword
                }
                logger.log("Before check: " + str(req))
                req = self.check_for_empty_information(req)
                logger.log("after check: " + str(req))
                return req
        return None

    def check_social_media(self, string):
        words = re.sub(r'[^\w\s]', '', string.lower()).split()
        pattern = None
        indicator = None
        keyword = None
        pattern_keywords = self.patterns["social_media"]

        for w in words:
            if str(w) in pattern_keywords or "social media" in string.lower():
                pattern = "social media"  # wrong, need key
                indicator = tags.Indicator.social_media
                keyword = self.find_company_name_from_string(string)
                if not keyword:
                    keyword = self.find_industry_from_string(string)
                req = {
                    'type': tags.Type.data_request,
                    'subtype': pattern,
                    "indicator": indicator,
                    'keyword': keyword
                }
                logger.log("Before check: " + str(req))
                req = self.check_for_empty_information(req)
                logger.log("after check: " + str(req))
                return req
        return None

    def find_company_name_from_string(self, string):
        input = string.lower()
        company = []
        temp = None

        for c in self.companies:
            temp = [x.lower() for x in self.companies[c]]
            for comp in temp:
                if comp in input:
                    company.append(c)
                    break

        return company

    def find_industry_from_string(self, string):
        input = string.lower()
        industry = []
        temp = None

        for i in self.industries:
            temp = self.industries[i]
            # logger.log(temp)
            for ind in temp:
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
        pattern = None
        nouns = []
        company = self.find_company_name_from_array(nouns)
        keywords = None

        for n in tree["nodes"]:
            if n.data["part_of_speech"] == 6:  # get nouns
                nouns.append(n.data["lemma"])
            for p in self.patterns:
                if n.data["lemma"] in self.patterns[p]:  # find pattern
                    pattern = p
                    if n.data["part_of_speech"] == 6:
                     nouns.remove(n.data["lemma"])

        keywords = nouns
        if company is not None:
            keywords = company

        req1 = {
            'type': tags.Type.data_request,
            'subtype': pattern,
            'keyword': keywords
        }

        s = json.dumps(req1)
        logger.log(s)


    def find_company_name_from_array(self, array):
        logger.log(array)
        arr = [x.lower() for x in array]
        company = None
        temp = None

        for c in self.companies:
            temp = str(self.companies[c]).lower()
            for noun in arr:
                if noun in temp:
                    company = temp
                    break

        return company


    def check_tree_against_patterns(self,tree):
     pass


    def get_all_nouns_from_tree(self, tree):
        nouns = []
        for n in tree["nodes"]:
            print(n.data["lemma"] + ", " + str(n.data["part_of_speech"]))
            if n.data["part_of_speech"] == 6:
                nouns.append(n.data["lemma"])
        return nouns

if __name__ == "__main__":
    pbe = PatternBasedExtractor().get_instance()
    print(pbe.companies)