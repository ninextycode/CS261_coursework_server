import config as conf
import base.singleton as sn
import business_logic.nlp.data_tags as tags

import json
import re
import base.log as l


logger = l.Logger("PatternBasedExtractor")

class PatternBasedExtractor(sn.Singleton):

    patterns = json.loads('{"stock_price": ["price", "much"], "news": ["news", "information", "happen"], "industry": ["movement"]}')

    companies = conf.companies

    # basic predefined commands including pattern words and company name or industry name
    def get_meaning_from_using_patterns(self, string):
        pattern = None
        company = None

        words = re.sub(r'[^\w\s]','',string).split()
        for w in words:
            for p in self.patterns:
                if w in self.patterns[p]:
                    pattern = p
                    break

        req1 = {
            'type': tags.Type.data_request,
            'subtype': pattern,
            'keyword': self.find_company_name_from_string(string)
        }
        s = json.dumps(req1)
        logger.log(s)


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



    def find_company_name_from_string(self, string):
        input = string.lower()
        company = None
        temp = None

        for c in self.companies:
            temp = str(self.companies[c]).lower()
            logger.log(temp)
            if temp in input:
                company = c
                break

        return company

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