import base.singleton as sn
import business_logic.nlp.pattern_based_extractor as pbe
import data_providers.external_apis.google_nlp_api as google_nlp
import business_logic.nlp.nlp_exceptions as ex
import base.log as l
import business_logic.data_tags as tags

import config
import google.cloud.language as gl_lang
import multiprocessing.pool as m_pool


logger = l.Logger("GoogleCommandExtractor", None)


class GoogleCommandExtractor(sn.Singleton):

    def __init__(self):
        self.pattern_based_extractor: pbe.PatternBasedExtractor = pbe.PatternBasedExtractor.get_instance()
        self.google_api = google_nlp.GoogleNlpApi.get_instance()

    def get_meaning_from_single_using_nlp(self, text):
        meaning = None
        google_api_output = self.google_api.query_meaning(text)

        tree = google_api_output["tree"]
        keywords = google_api_output["keywords"]

        logger.log("tree:\n {}".format(tree["root"]))
        logger.log("keywords {}".format(keywords))

        meaning = self.get_meaning_from_using_nlp(tree, keywords)

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

        # raise ex.MeaningUnknown("Ambiguous Request")
        return None

    def get_meaning_from_alternatives(self, alternatives):
        if len(alternatives) == 0:
            return None

        pool = m_pool.ThreadPool(processes=len(alternatives))

        async_result = pool.map_async(self.get_meaning_from_single_using_patterns, [a["text"] for a in alternatives])
        pattern_based_responses = async_result.get()
        for response in pattern_based_responses:
            if response is not None:
                logger.log(response)
                return response

        async_result = pool.map_async(self.get_meaning_from_single_using_nlp, [a["text"] for a in alternatives])
        api_responses = async_result.get()
        for response in api_responses:
            if response is not None:
                logger.log(response)
                return response

        return None

    def get_meaning_from_using_nlp(self, tree, keywords):
        req = None
        pattern = None
        subtype = None
        keywords = []
        req = None
        soc_keywords = []

        interesting_parts_of_speech = [gl_lang.enums.PartOfSpeech.Tag.NOUN,  gl_lang.enums.PartOfSpeech.Tag.ADJ]

        for n in tree["nodes"]:
            if n.data["part_of_speech"] in interesting_parts_of_speech:  # get nouns
                keywords.append(n.data["lemma"])

        for p in self.pattern_based_extractor.patterns_keys:
            for n in tree["nodes"]:
                if n.data["lemma"] in self.pattern_based_extractor.patterns[p]:  # find pattern
                    pattern = p
                    if n.data["lemma"] in self.pattern_based_extractor.patterns_for_industry:
                        subtype = tags.Indicator.industry_average
                    if n.data["part_of_speech"] in interesting_parts_of_speech:
                        keywords.remove(n.data["lemma"])

                        logger.log("looking for a {}".format(pattern))
                        break
            if pattern is not None:
                break

        if pattern == "stock_price":
            if subtype is tags.Indicator.industry_average:
                req = {
                    "type": tags.Type.data_request,
                    "subtype": tags.SubType.stock,
                    "indicator": tags.Indicator.industry_average,
                    "keywords": self.pattern_based_extractor.find_industry_from_array(keywords)
                }
            else:
                req = {
                    "type": tags.Type.data_request,
                    "subtype": tags.SubType.stock,
                    "indicator": tags.Indicator.just_price,
                    "keywords": self.find_company_name_from_array(keywords)
                }

        if pattern == "news":
            print("=" * 200)
            news_key_nodes = []
            for n in tree["nodes"]:
                for p in self.pattern_based_extractor.pattern_nodes_opinion_on:
                    if n.data["text"] == p:  # get children of pattern nodes
                        news_key_nodes = n.get_predecessors()
                        keywords = []

            for w in news_key_nodes:
                if w.data["part_of_speech"] in interesting_parts_of_speech:
                    keywords.append(w.data["text"])

            req = {
                "type": tags.Type.data_request,
                "subtype": tags.SubType.news,
                "indicator": tags.Indicator.news,
                "keywords": keywords
            }

        if pattern == "social_media":
            for n in tree["nodes"]:
                for p in self.pattern_based_extractor.pattern_nodes_opinion_on:
                    if n.data["text"] == p:  # get children of pattern nodes
                        soc_keywords = n.get_predecessors()
                        keywords = []

            for w in soc_keywords:
                if w.data["part_of_speech"] in interesting_parts_of_speech:
                    keywords.append(w.data["text"])

            req = {
                "type": tags.Type.data_request,
                "subtype": tags.SubType.social_media,
                "indicator": tags.Indicator.social_media,
                "keywords": keywords
            }
        if req is not None:
            req = self.pattern_based_extractor.check_for_empty_information(req)

        return req

    def find_company_name_from_array(self, array):
        arr = [x.lower() for x in array]
        companies = []
        temp = None

        for c in self.pattern_based_extractor.companies:
            temp = str(self.pattern_based_extractor.companies[c]).lower()
            for noun in arr:
                if noun in temp:
                    companies.append(c)
                    break

        return companies

if __name__ == "__main__":
    gce = GoogleCommandExtractor().get_instance()

    # test cases for stock price of company with patterns
    # print("companies_____________________________________________")
    # print(1)
    # gce.get_meaning_from_single_using_patterns("What is the stock price of Barclays Bank?")
    # print(2)
    # gce.get_meaning_from_single_using_patterns("What is the price of Barclays?")
    # print(3)
    # gce.get_meaning_from_single_using_patterns("How is Rolls Royce priced?") # doesn't make it into the test at all, priced not in pattern
    # print(4)
    # gce.get_meaning_from_single_using_patterns("What is the price of Rolls Royce?")
    # print(5)
    # gce.get_meaning_from_single_using_patterns("How much is the price of RDS A?")
    # print(6)
    # gce.get_meaning_from_single_using_patterns("What is the price of Royal Dutch Shell?") # should give back two: A and B share give a as default??
    # print(7)
    # gce.get_meaning_from_single_using_patterns("Tell me the stock price of Smith?") # three companies that include smith
    # print(8)
    # gce.get_meaning_from_single_using_patterns("Tell me the stock price of Microsoft?")
    # print(9)
    # gce.get_meaning_from_single_using_patterns("Give me the stock of Lloyds Group?")
    # print(10)
    # gce.get_meaning_from_single_using_patterns("Give me the stock of Royal Shell?")

    # test cases for industry request with patterns
    # print("industry_____________________________________________")
    # print(1)
    # gce.get_meaning_from_single_using_patterns("Tell me about the software industry.")
    # print(2)
    # gce.get_meaning_from_single_using_patterns("How is the car industry behaving?")
    # print(3)
    # gce.get_meaning_from_single_using_patterns("Is there any movement in the paper industry?")
    # print(4)
    # gce.get_meaning_from_single_using_patterns("Any news on the electronics industry?") # will pass news and industry test!!! /ordering takes care now

    # test cases for news request with patterns
    # print("news_____________________________________________")
    # print(1)
    # gce.get_meaning_from_single_using_patterns("Give me the latest news on Barclays?")
    # print(2)
    # gce.get_meaning_from_single_using_patterns("Find news on Sainsbury's?")
    # print(3)
    # gce.get_meaning_from_single_using_patterns("Display the headlines of the pharmaceutical industry?") #crashes the test --> passes patterns for pharma industry info
    # print(4)
    # gce.get_meaning_from_single_using_patterns("Find news on the CEO of Barclays?") # makes the pattern, but cleary wrong result
    # print(5)
    # gce.get_meaning_from_single_using_patterns("Find news on Germany?")

    # test cases for social_media request with patterns
    # print("social_media_____________________________________________")
    # print(1)
    # gce.get_meaning_from_single_using_patterns("What do people think about the construction sector?")
    # print(2)
    # gce.get_meaning_from_single_using_patterns("Show me social media trends of Legal and General?")
    # print(3)
    # gce.get_meaning_from_single_using_patterns("What do people think about Donald Trump online?")

    # special cases for request with patterns
    # print("special_____________________________________________")
    # print(1)
    # gce.get_meaning_from_single_using_patterns("Do you have news on the price of Barclays?") # retruns news but should give stock price history



    #test cases for nlp

    # test cases for stock price of company with patterns
    # print("companies_____________________________________________")
    # print(3)
    # gce.get_meaning_from_single_using_nlp("How is Rolls Royce priced?")
    # print(6)
    # gce.get_meaning_from_single_using_nlp("What is the price of Royal Dutch Shell?")  # should give back two: A and B share give a as default??
    # print(7)
    # gce.get_meaning_from_single_using_nlp("Tell me the stock price of Smith?")  # three companies that include smith
    # print(8)
    # gce.get_meaning_from_single_using_nlp("Tell me the stock price of Microsoft?")  # three companies that include smith
    # print(9)
    # gce.get_meaning_from_single_using_nlp("Give me the stock of Lloyds Group?")
    # print(10)
    # gce.get_meaning_from_single_using_nlp("Give me the stock of Royal Shell?")


    # test cases for industry request with patterns
    # print("industry_____________________________________________")

    # test cases for news request with patterns
    # print("news_____________________________________________")
    # print(3)
    # gce.get_meaning_from_single_using_nlp("Display the headlines of the pharmaceutical industry?") #crashes the test --> passes patterns for pharma industry info
    # print(4)
    # gce.get_meaning_from_single_using_nlp("Find news on the CEO of Barclays?")
    # print(5)
    # gce.get_meaning_from_single_using_nlp("Find news on Germany?")

    # print("social_media_____________________________________________")
    # print(3)
    gce.get_meaning_from_single_using_nlp("What do people think about Donald Trump online?")
    gce.get_meaning_from_single_using_nlp("Check social media for IPhone 10")    #check "social media" two nodes!!

    # special cases for request with patterns
    # print("special_____________________________________________")

    # general test cases

    # gce.get_meaning_from_single("What is the price of Barclays?")
    # gce.get_meaning_from_single("What do people think about Donald Trump online?")
    # gce.get_meaning_from_single("How is Rolls Royce priced?")
    # gce.get_meaning_from_single("Show me social media trends of Legal and General?")
    # gce.get_meaning_from_single("Find news on Sainsbury's?")
    # gce.get_meaning_from_single_using_nlp("Check social media for IPhone 10")   # wrong!

    tests = [
        # "What is the price of Barclays?",
        # "What do people think about Donald Trump online?",
        # "How is Rolls Royce priced?",
        # "Show me social media trends of Legal and General?",
        # "Find news on Sainsbury's?",
        # "How much does Microsoft cost",
        # "Give me news about Microsoft",
        "What are the news about meat",
        "What do people think about the weather today?"
    ]
    for test in tests:
        resp = gce.get_meaning_from_single_using_nlp(test)   # wrong!
        print(resp)
