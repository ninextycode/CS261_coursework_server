import base.singleton as sn
import business_logic.nlp.data_tags as tags


import json
import re
import base.log as l


logger = l.Logger("PatternBasedExtractor")

class PatternBasedExtractor(sn.Singleton):

    patterns = ["price", "news"]

    def get_meaning(self, string):
        for p in PatternBasedExtractor.patterns:
            if p in string:
                request = {}
                req1 = {
                    'type': tags.Type.data_request,
                    'subtype': p,
                    'keyword': re.sub(r'[^\w\s]','',string.rsplit(' ', 1)[1])
                }
                s = json.dumps(req1)
                logger.log(s)


if __name__ == '__main__':
    pbe = PatternBasedExtractor.get_instance()
    pbe.get_meaning("What is the price of Apple?")
    pbe.get_meaning("What is the latest news of Microsoft?")
