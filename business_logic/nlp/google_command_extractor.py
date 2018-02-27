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

    # logger.log(gce.pattern_based_extractor.find_company_name_from_string("What is the stock price of Barclays?"))

    # test cases for stock price of company with patterns
    print("companies_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("What is the stock price of Barclays Bank?")
    print(2)
    gce.get_meaning_from_single_using_patterns("What is the price of Barclays?")
    print(3)
    gce.get_meaning_from_single_using_patterns("How is Rolls Royce priced?") # doesn't make it into the test at all, priced not in pattern
    print(4)
    gce.get_meaning_from_single_using_patterns("What is the price of Rolls Royce?")
    print(5)
    gce.get_meaning_from_single_using_patterns("How much is the price of RDS A?")
    print(6)
    gce.get_meaning_from_single_using_patterns("What is the price of Royal Dutch Shell?") # should give back two: A and B share give a as default??
    print(7)
    gce.get_meaning_from_single_using_patterns("Tell me the stock price of Smith?") # three companies that include smith

    # test cases for industry request with patterns
    print("industry_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("Tell me about the software industry.")
    print(2)
    gce.get_meaning_from_single_using_patterns("How is the car industry behaving?")
    print(3)
    gce.get_meaning_from_single_using_patterns("Is there any movement in the paper industry?")
    print(4)
    gce.get_meaning_from_single_using_patterns("Any news on the electronics industry?") # will pass news and industry test!!!

    # test cases for news request with patterns
    print("news_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("Give me the latest news on Barclays?")
    print(2)
    gce.get_meaning_from_single_using_patterns("Find news on Sainsbury's?")
    print(3)
    gce.get_meaning_from_single_using_patterns("Display the headlines of the pharmaceutical industry?") #crashes the test --> passes patterns for pharma industry info

    # test cases for social_media request with patterns
    print("social_media_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("What do people think about the construction sector?")
    print(2)
    gce.get_meaning_from_single_using_patterns("Show me social media trends of Legal and General?")



    # gce.get_meaning_from_single_using_patterns("What is happening in pharmaceuticals?")
    # gce.get_meaning_from_single_using_patterns("Any information on real estate market?") #get a company name!!! should be a sector
    # gce.get_meaning_from_single_using_patterns("How much is Facebook?")
    # gce.get_meaning_from_single_using_nlp("How is Rolls Royce priced?")
    # gce.get_meaning_from_single_using_nlp("What is happening in pharmaceuticals?")
    # gce.get_meaning_from_single_using_nlp("Any information on real estate market?")
    # gce.get_meaning_from_single_using_patterns("Are there any deviations in the ship building industry?")
    # gce.get_meaning_from_single_using_nlp("Are there any deviations in the ship building industry?")
    # print("easy jet" in "how much is easy jet?")
    # gce.get_meaning_from_single_using_nlp("What is the news on the computer sector?")
