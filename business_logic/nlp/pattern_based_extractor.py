import base.singleton as sn
import business_logic.nlp.data_tags as tags
# import business_logic.nlp.google_command_extractor as gce


import json
import re
import base.log as l


logger = l.Logger("PatternBasedExtractor")

class PatternBasedExtractor(sn.Singleton):

    patterns = ["price", "news"]
    companies = ["Apple", "Microsoft", "Facebook"]

    def get_meaning(self, tree, keywords):
        for k in keywords:
            if k["word"] in self.patterns:
                request = {}
                req1 = {
                    'type': tags.Type.data_request,
                    'subtype': k["word"],
                    'keyword': self.find_company_name(tree["nodes"])
                }
                s = json.dumps(req1)
                logger.log(s)
                break
                #print(keywords[0]['word'])

    def find_company_name(self, nodes):
        words = nodes
        company = None
        for w in words:
            if (w.data["text"]) in self.companies:
                company = w.data["text"]
                break
        return company


if __name__ == '__main__':
    gce = gce.get_instance()
    pbe = PatternBasedExtractor.get_instance()
    pbe.get_meaning("What is the price of Apple?")
    pbe.get_meaning("What is the latest news of Microsoft?")
