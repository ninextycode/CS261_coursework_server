import base.singleton as sn
import business_logic.nlp.data_tags as tags

import json
import re
import base.log as l


logger = l.Logger("PatternBasedExtractor")

class PatternBasedExtractor(sn.Singleton):

    patterns = json.loads('{"stock_price": ["price", "much"], "news": ["news", "information"]}')

    companies = ["Apple", "Microsoft", "Facebook"]

    def get_meaning_from_single(self, string, keywords):
        print(self.patterns["stock_price"])
        for k in keywords:
            for p in self.patterns:
                print(p)
                if k["word"] in self.patterns[p]:
                    request = {}
                    req1 = {
                        'type': tags.Type.data_request,
                        'subtype': p,
                        'keyword': self.find_company_name(re.sub(r'[^\w\s]','',string).split())
                    }
                    s = json.dumps(req1)
                    logger.log(s)
                    break

    def find_company_name(self, words):
        company = None
        for w in words:
            if w in self.companies:
                company = w
                break
        return company


if __name__ == '__main__':
    gce = gce.get_instance()
    pbe = PatternBasedExtractor.get_instance()
    pbe.get_meaning("What is the price of Apple?")
    pbe.get_meaning("What is the latest news of Microsoft?")
