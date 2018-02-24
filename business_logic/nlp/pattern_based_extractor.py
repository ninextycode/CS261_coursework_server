import base.singleton as sn
import business_logic.nlp.data_tags as tags

import json
import re
import base.log as l


logger = l.Logger("PatternBasedExtractor")

class PatternBasedExtractor(sn.Singleton):

    patterns = json.loads('{"stock_price": ["price", "much"], "news": ["news", "information", "happen"]}')

    companies = ["Apple", "Microsoft", "Facebook"]

    def get_meaning_from_using_patterns(self, string):
        words = re.sub(r'[^\w\s]','',string).split()
        print(words)
        for w in words:
            for p in self.patterns:
                if w in self.patterns[p]:
                    request = {}
                    req1 = {
                        'type': tags.Type.data_request,
                        'subtype': p,
                        'keyword': self.find_company_name(re.sub(r'[^\w\s]','',string).split())
                    }
                    s = json.dumps(req1)
                    logger.log(s)
                    break


    def get_meaning_from_using_nlp(self, tree, keywords):
        pattern = None
        nouns = []

        for n in tree["nodes"]:
            if n.data["part_of_speech"] == 6:  # get nouns
                nouns.append(n.data["lemma"])
            for p in self.patterns:
                if n.data["lemma"] in self.patterns[p]:  # find pattern
                    pattern = p
                    if n.data["part_of_speech"] == 6:
                     nouns.remove(n.data["lemma"])


        req1 = {
            'type': tags.Type.data_request,
            'subtype': pattern,
            'keyword': nouns
        }

        s = json.dumps(req1)
        logger.log(s)



    def find_company_name(self, words):
        company = None
        for w in words:
            if w in self.companies:
                company = w
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

