import base.SingletoneInterface as si

import business_logic.nlp.PatternBasedExtractor as pbe


class NLP(si.Singleton):
    def __init__(self):
        self.extractor = pbe.PatternBasedeExtractor()

    def get_meaning(self, string):
        return self.extractor.get_meaning(string)