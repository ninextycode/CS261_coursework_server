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
        google_api_output = self.google_api.query_meaning(text)

        tree = google_api_output["tree"]
        keywords = google_api_output["keywords"]

        logger.log("tree:\n {}".format(tree["root"]))
        logger.log("keywords {}".format(keywords))

        meaning = self.pattern_based_extractor.get_meaning_from_using_nlp(tree, keywords)

        return meaning

    def get_meaning_from_single_using_patterns(self, text):
        return self.pattern_based_extractor.get_meaning_from_using_patterns(text)

    def get_meaning_from_single(self, text):
        meaning = self.get_meaning_from_single_using_patterns(text)
        logger.log("--------------------")
        logger.log("meaning: ")
        logger.log(meaning)
        logger.log("--------------------")
        if meaning is not None:
            logger.log("--------------------")
            logger.log("meaning after pattern: ")
            logger.log(meaning)
            logger.log("--------------------")
            return meaning

        meaning = self.get_meaning_from_single_using_nlp(text)
        if meaning is not None:
            logger.log("--------------------")
            logger.log("meaning after nlp: ")
            logger.log(meaning)
            logger.log("--------------------")
            return meaning

        raise ex.MeaningUnknown("Ambiguous Request")

    def get_meaning_from_alternatives(self, alternatives):
        pool = m_pool.ThreadPool(processes=len(alternatives))

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
    print(8)
    gce.get_meaning_from_single_using_patterns("Tell me the stock price of Microsoft?")
    print(9)
    gce.get_meaning_from_single_using_patterns("Give me the stock of Lloyds Group?")
    print(10)
    gce.get_meaning_from_single_using_patterns("Give me the stock of Royal Shell?")

    # test cases for industry request with patterns
    print("industry_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("Tell me about the software industry.")
    print(2)
    gce.get_meaning_from_single_using_patterns("How is the car industry behaving?")
    print(3)
    gce.get_meaning_from_single_using_patterns("Is there any movement in the paper industry?")
    print(4)
    gce.get_meaning_from_single_using_patterns("Any news on the electronics industry?") # will pass news and industry test!!! /ordering takes care now

    # test cases for news request with patterns
    print("news_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("Give me the latest news on Barclays?")
    print(2)
    gce.get_meaning_from_single_using_patterns("Find news on Sainsbury's?")
    print(3)
    gce.get_meaning_from_single_using_patterns("Display the headlines of the pharmaceutical industry?") #crashes the test --> passes patterns for pharma industry info
    print(4)
    gce.get_meaning_from_single_using_patterns("Find news on the CEO of Barclays?") # makes the pattern, but cleary wrong result
    print(5)
    gce.get_meaning_from_single_using_patterns("Find news on Germany?")

    # test cases for social_media request with patterns
    print("social_media_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("What do people think about the construction sector?")
    print(2)
    gce.get_meaning_from_single_using_patterns("Show me social media trends of Legal and General?")
    print(3)
    gce.get_meaning_from_single_using_patterns("What do people think about Donald Trump online?")

    # special cases for request with patterns
    print("special_____________________________________________")
    print(1)
    gce.get_meaning_from_single_using_patterns("Do you have news on the price of Barclays?") # retruns news but should give stock price history



    #test cases for nlp

    # test cases for stock price of company with patterns
    print("companies_____________________________________________")
    print(3)
    gce.get_meaning_from_single_using_nlp("How is Rolls Royce priced?")
    print(6)
    gce.get_meaning_from_single_using_nlp("What is the price of Royal Dutch Shell?")  # should give back two: A and B share give a as default??
    print(7)
    gce.get_meaning_from_single_using_nlp("Tell me the stock price of Smith?")  # three companies that include smith
    print(8)
    gce.get_meaning_from_single_using_nlp("Tell me the stock price of Microsoft?")  # three companies that include smith
    print(9)
    gce.get_meaning_from_single_using_nlp("Give me the stock of Lloyds Group?")
    print(10)
    gce.get_meaning_from_single_using_nlp("Give me the stock of Royal Shell?")


    # test cases for industry request with patterns
    print("industry_____________________________________________")

    # test cases for news request with patterns
    print("news_____________________________________________")
    print(3)
    gce.get_meaning_from_single_using_nlp("Display the headlines of the pharmaceutical industry?") #crashes the test --> passes patterns for pharma industry info
    print(4)
    gce.get_meaning_from_single_using_nlp("Find news on the CEO of Barclays?")
    print(5)
    gce.get_meaning_from_single_using_nlp("Find news on Germany?")

    print("social_media_____________________________________________")
    print(3)
    gce.get_meaning_from_single_using_nlp("What do people think about Donald Trump online?")
    gce.get_meaning_from_single_using_nlp("Check social media for IPhone 10")    #check "social media" two nodes!!

    # special cases for request with patterns
    print("special_____________________________________________")

    # general test cases
    tests = [
        "What is the price of Barclays?",
        "What do people think about Donald Trump online?",
        "How is Rolls Royce priced?",
        "Show me social media trends of Legal and General?",
        "Find news on Sainsbury's?",
        "How much does Microsoft cost", 
        "What are the news about meat"
    ]
    for test in tests:
        resp = gce.get_meaning_from_single_using_nlp(test)   # wrong!
        print(resp)
    # about, for