import base.singleton as sn

import json
import re


class PatternBasedExtractor(sn.Singleton):

    patterns = ["price", "news"]

    def get_meaning(self, string):
        for p in PatternBasedExtractor.patterns:
            if p in string:
                request = {}
                req1 = {
                    'type': 'request',
                    'subtype': p,
                    'keyword': re.sub(r'[^\w\s]','',string.rsplit(' ', 1)[1])
                }
                s = json.dumps(req1)
                print(s)


if __name__ == '__main__':
    PatternBasedExtractor.get_meaning("What is the price of Apple?")
    PatternBasedExtractor.get_meaning("What is the latest news of Microsoft?")