import base.singleton as sn
import business_logic.nlp.pattern_based_extractor as pbe
import data_providers.external_apis.google_nlp_api as google_nlp
import business_logic.nlp.nlp_exceptions as ex
import base.log as l
import business_logic.data_tags as tags

import config as conf
import google.cloud.language as gl_lang
import multiprocessing.pool as m_pool

import re

logger = l.Logger('GoogleCommandExtractor', None)


class GoogleCommandExtractor(sn.Singleton):
    def __init__(self):
        self.pattern_based_extractor: pbe.PatternBasedExtractor = pbe.PatternBasedExtractor.get_instance()
        self.google_api = google_nlp.GoogleNlpApi.get_instance()
        self.interesting_parts_of_speech = [
            gl_lang.enums.PartOfSpeech.Tag.NOUN,
            gl_lang.enums.PartOfSpeech.Tag.ADJ,
            gl_lang.enums.PartOfSpeech.Tag.NUM
        ]

    def get_meaning_from_alternatives(self, alternatives):
        if len(alternatives) == 0:
            return None

        pool = m_pool.ThreadPool(processes=len(alternatives))

        async_result = pool.map_async(self.get_meaning_from_single_using_patterns, [a['text'] for a in alternatives])
        pattern_based_responses = async_result.get()
        for i, response in enumerate(pattern_based_responses):
            if response is not None:
                logger.log(response)
                response["raw_input"] = alternatives[i]
                return response

        async_result = pool.map_async(self.get_meaning_from_single_using_nlp, [a['text'] for a in alternatives])
        api_responses = async_result.get()
        for i, response in enumerate(api_responses):
            if response is not None:
                response["raw_input"] = alternatives[i]
                return response
        return None

    def get_meaning_from_single(self, text):
        meaning = self.get_meaning_from_single_using_patterns(text)
        if meaning is not None:
            meaning["raw_input"] = text

        if meaning is not None and 'keywords' not in meaning.keys(): # keywords may be extended
            return meaning

        meaning_nlp = self.get_meaning_from_single_using_nlp(text)
        if meaning_nlp is not None:
            meaning_nlp["raw_input"] = text
            return meaning_nlp
        else:
            return meaning  # update meaning, but if failed - return old one

    def get_meaning_from_single_using_patterns(self, text):
        response = self.pattern_based_extractor.get_meaning_from_using_patterns(text)
        return response

    def get_meaning_from_single_using_nlp(self, text):
        google_api_output = self.google_api.query_meaning(text)

        tree = google_api_output['tree']
        keywords = google_api_output['keywords']

        meaning = self.get_meaning_from_using_nlp(tree, keywords, text)

        return meaning

    def get_meaning_from_using_nlp(self, tree, keywords, string):
        pattern = None
        req = None

        for p in self.pattern_based_extractor.patterns_keys:
            for n in tree['nodes']:
                if n.data['lemma'] in self.pattern_based_extractor.patterns[p]:  # find pattern
                    pattern = p
                    logger.log('looking for a {}'.format(pattern))
                    break
            if pattern is not None:
                break

        if pattern in [tags.SubType.stock, tags.SubType.industry]:
            req = self.request_for_stock_price(tree, string)
        if pattern == 'news':
            req = self.request_for_news(tree)
        if pattern == 'social_media':
            req = self.request_for_social_media(tree)
        if req is not None:
            req = self.pattern_based_extractor.null_on_empty_information(req)
        return req

    def request_for_stock_price(self, tree, string):
        words = re.sub(r'[^\w\s]', '', string.lower()).split()
        # is_industry = self.is_about_industry_words_list(words)
        if self.pattern_based_extractor.find_industry_from_string(string) is not None:
            is_industry = True
        else:
            is_industry = None
        industry_id = -1
        if is_industry:
            industry_id = self.pattern_based_extractor.find_industry_from_string(string)
            ticker = self.pattern_based_extractor.get_industry_tickers_by_id(industry_id)
        else:
            ticker = self.pattern_based_extractor.find_company_ticker_from_string(string)

        indicators = self.pattern_based_extractor.check_stock_price_indicator(words)
        time = self.pattern_based_extractor.check_stock_price_time(words)
        if len(indicators) == 0:
            if is_industry:
                indicators = [tags.Indicator.industry_average]
            else:
                indicators = [tags.Indicator.just_price]

        req = {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry if is_industry else tags.SubType.stock,
            'indicators': indicators,
            'time': time,
            'tickers': ticker,
        }
        if is_industry:
            req["industry"] = industry_id

        req = self.pattern_based_extractor.null_on_empty_information(req)
        return req

    def request_for_news(self, tree):
        keywords = []
        key_nodes = self.get_nodes_from_request_branch(tree)
        if len(key_nodes) == 0:
            return None

        for w in key_nodes:
            if w.data['part_of_speech'] in self.interesting_parts_of_speech:
                keywords.append(w.data['text'])

        return {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.news,
            'keywords': keywords
        }

    def request_for_social_media(self, tree):
        keywords = []
        key_nodes = self.get_nodes_from_request_branch(tree)
        if len(key_nodes) == 0:
            return None

        for w in key_nodes:
            if w.data['part_of_speech'] in self.interesting_parts_of_speech:
                keywords.append(w.data['text'])

        return {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.social_media,
            'keywords': keywords
        }

    def get_nodes_from_request_branch(self, tree):
        for n in tree['nodes']:
            if n.data['text'] in self.pattern_based_extractor.pattern_nodes_opinion_on:
                return n.get_predecessors()
        return []

    def find_company_names_from_array(self, array):
        arr = [x.lower() for x in array]
        companies = []

        for c in conf.companies:
            temp = str(conf.companies[c]).lower()
            for noun in arr:
                if noun in temp:
                    companies.append(c)

        return companies

    def find_industry_from_array(self, data):
        industries = []
        for word in data:
            ind = self.pattern_based_extractor.find_industry_from_string(word)
            if ind is not None:
                return ind
        else:
           return []

    def test(self, test_cases, test_number=0): # test_number: 1 for patterns, 2 for nlp, otherwise for general get_meaning from single
        passed = True
        total = 0
        number_passed = 0

        for test_input in test_cases.keys():
            total += 1
            expected = test_cases[test_input]
            if test_number == 1:
                result = gce.get_meaning_from_single_using_patterns(test_input)
            elif test_number == 2:
                result = gce.get_meaning_from_single_using_nlp(test_input)
            else:
                result = gce.get_meaning_from_single(test_input)

            if result is not None and "raw_input" in result.keys():
                del(result["raw_input"])
            if expected == result:
                print('OK' + '=' * 150 + 'OK')
                number_passed += 1
            else:
                print('Wrong' + '=' * 150 + 'Wrong')
                passed=False

            print('Input:\t' + str(test_input))
            print('Expect:\t' + str(test_cases[test_input]))
            print('Result:\t' + str(result) + '\n')

        print("!"*100)
        print("Total: " + str(total))
        print("Passed: " + str(number_passed))
        print("!" * 100)
        return passed


if __name__ == '__main__':
    gce = GoogleCommandExtractor().get_instance()

    # test cases for stock price of company with patterns
    test_stock_price_patterns = {

        'What is the stock price of Barclays Bank?': {
                'type': tags.Type.data_request,
                'subtype': 'stock',
                'indicators': [tags.Indicator.just_price],
                "time": tags.TimePeriods.default_time_period,
                'tickers': ['BARC']
        },

        'What is the price of Barclays?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.just_price],
            'tickers': ['BARC'],
            "time": tags.TimePeriods.default_time_period
        },

        'How is Rolls Royce priced?': None, # doesn't make it into the test at all, priced not in pattern

        'What is the price of Rolls Royce?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.just_price],
            'tickers': ['RR.'],
            "time": tags.TimePeriods.default_time_period
        },

        'How much is the price of RDS A?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.just_price],
            'tickers': ['RDSA'],
            "time": tags.TimePeriods.default_time_period
        },

        'What is the price of Royal Dutch Shell?': None, # no exact pattern match
        'Give me the stock of Royal Shell?': None, # no exact pattern match

        # four companies that include smith, but no exact match
        'Tell me the stock price of Smith?': {
            'type': 'data_request',
            'subtype': 'stock',
            'indicators': [tags.Indicator.just_price],
            'time': [tags.Indicator.just_price],
            'tickers': ['GSK', 'SN.', 'SMDS', 'SMIN']
        },

        'Tell me the stock price of Microsoft?': None, # Microsoft not in FTSE100

        'Give me the stock of Lloyds Group?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.just_price],
            'tickers': ['LLOY'],
            "time": tags.TimePeriods.default_time_period
        },

        'What is the stock price of Barclays Bank today?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.just_price],
            'tickers': ['BARC'],
            "time": tags.TimePeriods.day
        },

        'What was the variance of Barclays Bank this month?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.stock_volatility],
            'tickers': ['BARC'],
            "time": tags.TimePeriods.month
        },
        'What was the price change of Barclays in the last hour?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.price_change],
            'tickers': ['BARC'],
            "time": tags.TimePeriods.hour
        },

        'What was the  behaviour of Barclays stock in the last week?': {
            'type': tags.Type.data_request,
            'subtype': 'stock',
            'indicators': [tags.Indicator.stock_volatility, tags.Indicator.price_change, tags.Indicator.just_price],
            'tickers': ['BARC'],
            "time": tags.TimePeriods.week
        },

        'How is Severn Trent performing?': None,

    }

    # test cases for industries with patterns
    test_industry_with_patterns = {
        'Tell me about the software industry.': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry,
            'indicators': [tags.Indicator.industry_average],
            'tickers': ['MCRO', 'SGE'],
            'time': tags.TimePeriods.default_time_period,
            "industry": 37
        },
        'How is the car industry behaving?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry,
            'indicators': [tags.Indicator.stock_volatility, tags.Indicator.price_change, tags.Indicator.just_price],
            'time': tags.TimePeriods.default_time_period,
            'tickers': ['GKN'],
            'industry': 3
        },
        'Is there any movement in the paper industry?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry,
            'indicators': [tags.Indicator.industry_average],
            'time': tags.TimePeriods.default_time_period,
            'tickers': ['MNDI'],
            'industry': 15
        },

        'Any news on the electronics industry?':  	{
            'type': 'data_request',
            'subtype': 'news',
            'keywords': ['Electronic', 'Electrical', 'Equipment']
        },

        'How does the electronics industry behaves this week?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry,
            'indicators': [tags.Indicator.stock_volatility, tags.Indicator.price_change, tags.Indicator.just_price],
            'tickers': ['HLMA'],
            'time': tags.TimePeriods.week,
            'industry': 9
        },

        'Show me the volatility of the electronic sector this week.': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry,
            'indicators': [tags.Indicator.stock_volatility],
            'tickers': ['HLMA'],
            'time': tags.TimePeriods.week,
            'industry': 9
        },

        'How does Aerospace and Defense perform this week?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.industry,
            'indicators': [tags.Indicator.industry_average],
            'tickers': ['BA.', 'RR.'],
            'time': tags.TimePeriods.week,
            'industry': 1
        },
    }
    
    # test cases for news request with patterns
    test_news_with_patterns = {
        'Give me the latest news on Barclays?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.news,
            'keywords': ['Barclays']
        },

        'Find news on Sainsbury\'s?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.news,
            'keywords': ['Sainsbury\'s']
        },

        'Display the headlines of the pharmaceutical industry?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.news,
            'keywords': ['Pharmaceuticals', 'Biotechnology']
        },

        'Find news on the CEO of Barclays?': None, # makes the pattern, but cleary wrong result

        'Find news about the chancellor of Germany?': None

    }

    # test cases for social_media request with patterns
    test_social_media_with_patterns = {
        'What do people think about the construction sector?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.social_media,
            'keywords': ['Construction', 'Materials']
        },

        'Show me social media trends of Legal and General?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.social_media,
            'keywords': ['Legal and General']
        },


        'What do people think about Donald Trump online?': None

    }

    # test cases for stock price of company with patterns
    test_stock_price_nlp = {
        'How is Rolls Royce priced?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.stock,
            'indicators': [tags.Indicator.just_price],
            'tickers': ['RR.'],
            'time': tags.TimePeriods.default_time_period,
        },

        'What is the price of Royal Dutch Shell?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.stock,
            'indicators': [tags.Indicator.just_price],
            'tickers': ['RDSA', 'RDSB'],
            'time': tags.TimePeriods.default_time_period
        },

        'Tell me the stock price of Smith?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.stock,
            'indicators': [tags.Indicator.just_price],
            'tickers': ['GSK', 'SN.', 'SMDS', 'SMIN'],
            'time': tags.TimePeriods.default_time_period
        },

        'Tell me the stock price of Microsoft?': None,

        'Give me the stock of Lloyds Group?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.stock,
            'indicators': [tags.Indicator.just_price],
            'tickers': ['LLOY'],
            'time': tags.TimePeriods.default_time_period
        },
        'Give me the stock of Royal Shell?': {
            'type': tags.Type.data_request,
            'subtype': tags.SubType.stock,
            'indicators': [tags.Indicator.just_price],
            'tickers': ['RDSA', 'RDSB'],
            'time': tags.TimePeriods.default_time_period
        }
    }

    # test cases for industries with nlp

    # test cases for news request with nlp
    test_news_nlp = {
        'Display the headlines of the pharmaceutical industry?': {
            'type': tags.Type.data_request,
            'subtype': 'news',
            'keywords': ['Pharmaceuticals', 'Biotechnology']
        },
        'Find news on the CEO of Barclays?': {
            'type': tags.Type.data_request,
            'subtype': 'news',
            'keywords': ['CEO', 'Barclays']
        },
        'Find news on Germany?': {
            'type': tags.Type.data_request,
            'subtype': 'news',
            'keywords': ['Germany']
        },
        'Find news about Donald Trump': {
            'type': tags.Type.data_request,
            'subtype': 'news',
            'keywords': ['Trump', 'Donald']
        }
    }

    # test cases for social media requests with nlp
    test_social_media_nlp = {
        'What do people think about Donald Trump online?': {
            'type': tags.Type.data_request,
            'subtype': 'social_media',
            'keywords': ['Trump', 'Donald']
        },
        'Check social media for IPhone 10': {
            'type': tags.Type.data_request,
            'subtype': 'social_media',
            'keywords': ['IPhone', '10']
        },
        'What do people think of the new IPhone 10?': {
            'type': tags.Type.data_request,
            'subtype': 'social_media',
            'keywords': ['IPhone', 'new', '10']  #only interesting words
        },
        'Check social media for Donald Trump': {
            'type': tags.Type.data_request,
            'subtype': 'social_media',
            'keywords': ['Trump', 'Donald']
        },
    }

    test_patterns = [
        test_stock_price_patterns,
        test_industry_with_patterns,
        test_news_with_patterns,
        test_social_media_with_patterns,
    ], [
        test_stock_price_nlp,
        test_news_nlp,
        test_social_media_nlp
    ]


    for pattern in test_patterns[0]:
        print("="*10)
        print("Passed ", gce.test(pattern, 1))



    for pattern in test_patterns[1]:
        print("="*10)
        print("Passed ", gce.test(pattern))

