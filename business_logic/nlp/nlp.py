import base.singleton as si

import business_logic.nlp.pattern_based_extractor as pbe
import business_logic.nlp.google_command_extractor as gce

class NLP(si.Singleton):
    def __init__(self):
        self.extractor = gce.GoogleCommandExtractor.get_instance()

    def get_meaning(self, string):
        return self.extractor.get_meaning(string)
