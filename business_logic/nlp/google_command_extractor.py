import base.singleton as sn
import business_logic.nlp.pattern_based_extractor as pbe
import business_logic.nlp.nlp_exceptions as ex
import data_providers.external_apis.google_nlp_api as google_nlp

import base.log as l


logger = l.Logger("GoogleCommandExtractor")

class GoogleCommandExtractor(sn.Singleton):
    def __init__(self):
        self.pattern_based_extractor = pbe.PatternBasedExtractor.get_instance()
        self.google_api = google_nlp.GoogleNlpApi.get_instance()

    def get_meaning(self, text):
        meaning = None
        try:
            meaning = self.pattern_based_extractor.get_meaning(text)
        except ex.MeaningUnknown:
            logger.log("Cannot get meaning using patterns")

        google_api_output = self.google_api.query(text)
        tree = google_api_output["tree"]
        keywords = google_api_output["keywords"]
        raw = google_api_output["raw"]

        return meaning

    def construct_tree(self, text):
        pass

