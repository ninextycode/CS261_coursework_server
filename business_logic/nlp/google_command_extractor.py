import base.singleton as sn
import business_logic.nlp.pattern_based_extractor as pbe
import business_logic.nlp.nlp_exceptions as ex
import data_providers.external_apis.google_nlp_api as google_nlp

import base.log as l

import config

import multiprocessing.pool as m_pool

logger = l.Logger("GoogleCommandExtractor", 500)


class GoogleCommandExtractor(sn.Singleton):

    def __init__(self):
        self.pattern_based_extractor = pbe.PatternBasedExtractor.get_instance()
        self.google_api = google_nlp.GoogleNlpApi.get_instance()

    def get_meaning_from_single_using_nlp(self, text):
        meaning = None
        google_api_output = self.google_api.query(text)

        tree = google_api_output["tree"]
        keywords = google_api_output["keywords"]

        logger.log("tree:\n {}".format(tree["root"]))
        logger.log("keywords {}".format(keywords))

        return meaning

    def get_meaning_from_single_using_patterns(self, text):
        return self.pattern_based_extractor.get_meaning(text)

    def get_meaning_from_single(self, text):
        meaning = self.get_meaning_from_single_using_patterns(text)
        if meaning is not None:
            return meaning

        meaning = self.get_meaning_from_single_using_nlp(text)
        if meaning is not None:
            return meaning
        raise ex.MeaningUnknown()

    def get_meaning_from_alternatives(self, alternatives):
        pool = m_pool.ThreadPool(processes=config.default_number_of_nlp_threads)

        async_result = pool.map_async(self.get_meaning_from_single_using_patterns, [a["text"] for a in alternatives])
        pattern_based_responses = async_result.get()
        for response in pattern_based_responses:
            if response is not None:
                return response

        async_result = pool.map_async(self.get_meaning_from_single_using_nlp, [a["text"] for a in alternatives])
        api_responses = async_result.get()
        for response in api_responses:
            if response is not None:
                return response

        raise ex.MeaningUnknown()


if __name__ == "__main__":
    gce = GoogleCommandExtractor().get_instance()
    gce.get_meaning_from_single("What is the price of Apple?")