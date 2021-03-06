import config
import base.singleton as sn



class ReadableResponser(sn.Singleton):
    def get_readable_response_for_news(self, data, request):
        n = len(data)
        headline = 'I found {} recent articles for {}.\n'.format(n, request['keywords'])
        # articles = ''
        articles = []



        for l in data[:10]:
            #articles += (l['title'] + ': ' + l['link'] + '\n')
            articles.append([l['title'], l['link']])
        #articles += 'Find summaries and more news at {}'.format(config.news_summary_address)

        response = {
            'headline': headline,
            'type': "news",
            'text_body': articles
        }

        return response

    def get_readable_response_for_public_opinion(self, data, request):
        print(request)
        print(data.keys())
        print(data)
        search_terms = str(request['keywords'])

        sentiments = 'Very positive:\t{}\n' \
                     'Positive:\t\t{} \n' \
                     'Neutral:\t\t{} \n' \
                     'Negative:\t\t{} \n' \
                     'Very negative:\t{}'.format(self.calc_percentage(data['very_positive'], data['total']),
                                                 self.calc_percentage(data['positive'], data['total']),
                                                 self.calc_percentage(data['neutral'], data['total']),
                                                 self.calc_percentage(data['negative'], data['total']),
                                                 self.calc_percentage(data['very_negative'], data['total']))

        sentiments =  'The overall sentiment of {} social media posts is ' \
                      '{} with an average sentiment ' \
                      'score of {:1.2f}.\n'.format(data['total'], data['general_opinion'],  data['mean']) + sentiments

        response = {
            'headline': 'Social Media Analysis for ' + str(search_terms),
            'type': "social_media",
            'text_body': sentiments
        }

        return response

    def calc_percentage(self, den, nom):
        return '{:2.1f}%'.format(den/nom*100)

    def get_readable_response_for_unknown(self):
        return "Cannot process request"

    def get_readable_response_for_indicator(self, data, request):
        headline = "The value of {}:\n".format(request["indicators"])
        body = ""
        for indicator in data.keys():
            if data[indicator] is not None:
                for ticker in data[indicator].keys():
                    if ticker != "average":
                        body += "{}: {}\n".format(ticker, data[indicator][ticker])

                if "average" in data[indicator].keys():
                    body += "{}: {}\n".format("average", data[indicator]["average"])
                body += "\n"*2
        return {
            'headline': headline,
            'text_body': body
        }

