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

        # logger.log("tree:\n {}".format(tree["root"]))
        # logger.log("keywords {}".format(keywords))

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
                # logger.log(response)
                return response

        return None

    def get_meaning_from_using_nlp(self, tree, keywords):
        req = None
        pattern = None
        subtype = None
        interesting_words = []
        keywords = []
        req = None
        soc_keywords = []

        interesting_parts_of_speech = [gl_lang.enums.PartOfSpeech.Tag.NOUN,  gl_lang.enums.PartOfSpeech.Tag.ADJ]

        for n in tree["nodes"]:
            if n.data["part_of_speech"] in interesting_parts_of_speech:  # get nouns
                interesting_words.append(n.data["lemma"])

        for p in self.pattern_based_extractor.patterns_keys:
            for n in tree["nodes"]:
                if n.data["lemma"] in self.pattern_based_extractor.patterns[p]:  # find pattern
                    pattern = p
                    logger.log("looking for a {}".format(pattern))
                    break
            if pattern is not None:
                break



        if pattern == "stock_price":
                industry = False
                indicator = tags.Indicator.price_change
                time =  tags.TimePeriods.day

                for n in tree["nodes"]:
                    if n.data["lemma"] in self.pattern_based_extractor.patterns_for_industry:
                        industry = True
                    if n.data["lemma"] in self.pattern_based_extractor.patterns_for_stock_prices:
                        indicator = self.pattern_based_extractor.patterns_for_stock_prices[n.data["text"]]
                    if n.data["lemma"] in self.pattern_based_extractor.time_patterns.keys():
                        time = self.pattern_based_extractor.time_patterns[n.data["text"]]

                if industry:
                    keywords = self.find_industry_from_array(interesting_words)
                else:
                    keywords = self.find_company_name_from_array(interesting_words)

                req = {
                        "type": tags.Type.data_request,
                        "subtype": tags.SubType.stock,
                        "industry": industry,
                        "indicator": indicator,
                        "time": time,
                        "ticker": keywords
                    }
                print(interesting_words)
                print(req)


        if pattern == "news":
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

    def find_industry_from_array(self, data):
           industries = []
           for word in data:
               industries.extend(self.pattern_based_extractor.find_industry_from_string(word))
           if len(industries) > 0:
                return self.pattern_based_extractor.get_industry_ticker(industries[0])
           else:
               return []

    def test(self, test_cases, test_number=0): # test_number: 1 for patterns, 2 for nlp, otherwise for general get_meaning from single
        for test in test_cases:
            input = test
            expected = test_cases[test]
            if test_number == 1:
                result = gce.get_meaning_from_single_using_patterns(test)
            elif test_number == 2:
                result = gce.get_meaning_from_single_using_nlp(test)
            else:
                result = gce.get_meaning_from_single(test)

            if expected == result:
                logger.log("OK")
            else:
                logger.log("Wrong")

            logger.log("Input:\t" + str(input))
            logger.log("Expected:\t" + str(test_cases[test]))
            logger.log("Result:\t" + str(result) + "\n")









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
    # print(gce.get_meaning_from_single_using_nlp("What is the price of Royal Dutch Shell?")) # should give back two: A and B share give a as default??
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
    # print(gce.get_meaning_from_single_using_patterns("Tell me about the software industry."))
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
    # print(gce.get_meaning_from_single_using_nlp("How is Rolls Royce priced?"))
    # print(6)
    # gce.get_meaning_from_single_using_nlp("What is the price of Royal Dutch Shell?")  # should give back two: A and B share give a as default??
    # print(7)
    # print(gce.get_meaning_from_single_using_nlp("Tell me the stock price of Smith?"))  # three companies that include smith
    # print(8)
    # gce.get_meaning_from_single_using_nlp("Tell me the stock price of Microsoft?")  # four companies that include smith
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
    # gce.get_meaning_from_single_using_nlp("What do people think about Donald Trump online?")
    # gce.get_meaning_from_single_using_nlp("Check social media for IPhone 10")    #check "social media" two nodes!!

    # special cases for request with patterns
    # print("special_____________________________________________")

    # general test cases

    # print(gce.get_meaning_from_single("What is the price of Barclays?"))
    # print(gce.get_meaning_from_single("What do people think about Donald Trump online?"))
    # gce.get_meaning_from_single("How is Rolls Royce priced?")
    # gce.get_meaning_from_single("Show me social media trends of Legal and General?")
    # gce.get_meaning_from_single("Find news on Sainsbury's?")
    # gce.get_meaning_from_single_using_nlp("Check social media for IPhone 10")   # wrong!

    # tests = [
        # "What is the price of Barclays?",
        # "What do people think about Donald Trump online?",
        # "How is Rolls Royce priced?",
        # "Show me social media trends of Legal and General?",
        # "Find news on Sainsbury's?",
        # "How much does Microsoft cost",
        # "Give me news about Microsoft",
        # "What are the news\ink about the weather today?"
    # ]
    # for test in tests:
    #     resp = gce.get_meaning_from_single_using_nlp(test)   # wrong!
    #     print(resp)


    # logger.log(gce.get_meaning_from_single_using_patterns("What is the stock price of Barclays Bank today?"))
    # logger.log(gce.get_meaning_from_single("Give me the variance of Barclays Bank?")) #!!! problem solved with ordering
    # logger.log(gce.get_meaning_from_single_using_patterns("What is the variance of Barclays Bank?"))


    # test cases for stock price of company with patterns
    test_stock_price_patterns = {
        # "What is the stock price of Barclays Bank?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['BARC']},
        # "What is the price of Barclays?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['BARC']},
        # "How is Rolls Royce priced?": None, # doesn't make it into the test at all, priced not in pattern
        # "What is the price of Rolls Royce?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['RR.']},
        # "How much is the price of RDS A?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['RDSA']},
        # "What is the price of Royal Dutch Shell?": None, # no exact pattern match
        # "Give me the stock of Royal Shell?": None, # no exact pattern match
        # "Tell me the stock price of Smith?": None, # four companies that include smith, but no exact match
        # "Tell me the stock price of Microsoft?": None, # Microsoft not in FTSE100
        # "Give me the stock of Lloyds Group?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['LLOY']},
        "What is the stock price of Barclays Bank today?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['BARC']},
        "What was the variance of Barclays Bank this month?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['BARC']},

    }

    # test cases for industries with patterns
    test_industry_with_patterns = {
        "Tell me about the software industry.": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'industry_average', 'keywords': ['Software & Computer Services']},
        # "How is the car industry behaving?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'industry_average', 'keywords': ['Automobiles & Parts']},
        # "Is there any movement in the paper industry?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'industry_average', 'keywords': ['Forestry & Paper']},
        # "Any news on the electronics industry?":  {'type': 'data_request', 'subtype': 'stock', 'indicator': 'industry_average', 'keywords': ['Electronic & Electrical Equipment']},
        "Show me the volatility of the electronic sector this week.": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'stock_variance', 'time': 'month', 'keywords': ['Electronic & Electrical Equipment']}
    }
    
    # test cases for news request with patterns
    test_news_with_patterns = {
        "Give me the latest news on Barclays?": {'type': 'data_request', 'subtype': 'news', 'indicator': 'news', 'keywords': ['barclays']},
        "Find news on Sainsbury's?": {'type': 'data_request', 'subtype': 'news', 'indicator': 'news', 'keywords': ['sainsburys']},
        "Display the headlines of the pharmaceutical industry?": {'type': 'data_request', 'subtype': 'news', 'indicator': 'news', 'keywords': ['Pharmaceuticals & Biotechnology']},
        "Find news on the CEO of Barclays?": None, # makes the pattern, but cleary wrong result
        "Find news on Germany?": None
    }

    # test cases for social_media request with patterns
    test_social_media_with_patterns = {
        "What do people think about the construction sector?": {'type': 'data_request', 'subtype': 'social_media', 'indicator': 'social_media', 'keywords': ['Construction & Materials']},
        "Show me social media trends of Legal and General?": {'type': 'data_request', 'subtype': 'social_media', 'indicator': 'social_media', 'keywords': ['legal and general']},
        "What do people think about Donald Trump online?": None
    }

    # test cases for stock price of company with patterns
    test_stock_price_nlp = {
        "How is Rolls Royce priced?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['RR.']},
        "What is the price of Royal Dutch Shell?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['RDSA', 'RDSB']},
        "Tell me the stock price of Smith?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['GSK', 'SN.', 'SMDS', 'SMIN']},
        "Tell me the stock price of Microsoft?": None,
        "Give me the stock of Lloyds Group?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['LLOY']},
        "Give me the stock of Royal Shell?": {'type': 'data_request', 'subtype': 'stock', 'indicator': 'just_price', 'keywords': ['RDSA', 'RDSB']}
    }

    # test cases for industries with nlp

    # test cases for news request with nlp
    test_news_nlp = {
        "Display the headlines of the pharmaceutical industry?": {'type': 'data_request', 'subtype': 'news', 'indicator': 'news', 'keywords': ['Pharmaceuticals & Biotechnology']},
        "Find news on the CEO of Barclays?": {'type': 'data_request', 'subtype': 'news', 'indicator': 'news', 'keywords': ['CEO', 'Barclays']},
        "Find news on Germany?": {'type': 'data_request', 'subtype': 'news', 'indicator': 'news', 'keywords': ['Germany']},
        "Find news about Donald Trump": {'type': 'data_request', 'subtype': 'news', 'indicator': 'news', 'keywords': ['Donald', 'Trump']}
    }

    # test cases for social media requests with nlp
    test_social_media_nlp = {
        "What do people think about Donald Trump online?": {'type': 'data_request', 'subtype': 'social_media', 'indicator': 'social_media', 'keywords': ['Donald', 'Trump']},
        "Check social media for IPhone 10": {'type': 'data_request', 'subtype': 'social_media', 'indicator': 'social_media', 'keywords': ['IPhone', '10']},
        "What do people think of the new IPhone 10?": {'type': 'data_request', 'subtype': 'social_media', 'indicator': 'social_media', 'keywords': ['IPhone', 'new']},   #only interesting words
        "Check social media for Donald Trump": {'type': 'data_request', 'subtype': 'social_media', 'indicator': 'social_media', 'keywords': ['Donald', 'Trump']},

    }


    gce.test(test_industry_with_patterns, 2)