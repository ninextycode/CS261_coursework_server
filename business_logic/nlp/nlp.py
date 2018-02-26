import base.singleton as si

import business_logic.nlp.pattern_based_extractor as pbe
import business_logic.nlp.google_command_extractor as gce

class NLP(si.Singleton):
    def __init__(self):
        self.extractor = gce.GoogleCommandExtractor.get_instance()

    def get_meaning_from_single(self, string):
        return self.extractor.get_meaning_from_single(string)

    def get_meaning_from_alternatives(self, string):
        return self.extractor.get_meaning_from_alternatives(string)
