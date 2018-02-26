import base.singleton as sn
import business_logic.nlp.pattern_based_extractor as pbe
import data_providers.external_apis.google_nlp_api as google_nlp
import business_logic.nlp.nlp_exceptions as ex
import base.log as l

import config
import google.cloud.language as gl_lang
import multiprocessing.pool as m_pool


logger = l.Logger("GoogleCommandExtractor", None)


class GoogleCommandExtractor(sn.Singleton):

    def __init__(self):
        self.pattern_based_extractor = pbe.PatternBasedExtractor.get_instance()
        self.google_api = google_nlp.GoogleNlpApi.get_instance()
        gl_lang.enums.DependencyEdge.Label

    def get_meaning_from_single_using_nlp(self, text):
        meaning = None
        google_api_output = self.google_api.query(text)

        tree = google_api_output["tree"]
        keywords = google_api_output["keywords"]

        logger.log("tree:\n {}".format(tree["root"]))
        logger.log("keywords {}".format(keywords))

        self.pattern_based_extractor.get_meaning_from_using_nlp(tree, keywords)

        return meaning

    def get_meaning_from_single_using_patterns(self, text):
        return self.pattern_based_extractor.get_meaning_from_using_patterns(text)

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


if __name__ == '__main__':
    gce = GoogleCommandExtractor().get_instance()
    #gce.get_meaning_from_single_using_nlp("What is the news on the computer sector?")
    #gce.get_meaning_from_single_using_patterns("How much is Barclays Bank?")
    #gce.pattern_based_extractor.find_company_name("How much is Easy Jet?")
    #gce.get_meaning_from_single_using_patterns("How is Rolls Royce priced?")

    gce.get_meaning_from_single_using_patterns("What is the price of Apple?")
    gce.get_meaning_from_single_using_patterns("Any news on Microsoft?")
    gce.get_meaning_from_single_using_patterns("Any news in the oil market?")
    gce.get_meaning_from_single_using_patterns("What is happening in pharmaceuticals?")
    gce.get_meaning_from_single_using_patterns("Any information on real estate market?") #get a company name!!! should be a sector
    gce.get_meaning_from_single_using_patterns("How much is Facebook?")
    # gce.get_meaning_from_single_using_nlp("How is Rolls Royce priced?")
    # gce.get_meaning_from_single_using_nlp("What is happening in pharmaceuticals?")
    # gce.get_meaning_from_single_using_nlp("Any information on real estate market?")
    # gce.get_meaning_from_single_using_patterns("Are there any deviations in the ship building industry?")
    # gce.get_meaning_from_single_using_nlp("Are there any deviations in the ship building industry?")
    # print("easy jet" in "how much is easy jet?")