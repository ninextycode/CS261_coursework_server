import config
import base.singleton as sn



class ReadableResponser(sn.Singleton):
    def get_readable_response_for_news(self, request, data):
        n = len(data)
        headline = "I found {} recent articles for {}.\n".format(n, request["keywords"])
        articles = ""

        for l in data:
            articles += (l["title"] + ": " + l["link"] + "\n")

        response = {
            "headline": headline,
            "text_body": articles
        }

        return response

    def get_readable_response_for_public_opinion(self, request, data):
        print(request)
        print(data.keys())
        print(data)
        search_terms = str(request["keywords"])

        sentiments = "Very positive:\t{}\n" \
                     "Positive:\t\t{} \n" \
                     "Neutral:\t\t{} \n" \
                     "Negative:\t\t{} \n" \
                     "Very negative:\t{}".format(self.calc_percentage(data["very_positive"], data["total"]),
                                                 self.calc_percentage(data["positive"], data["total"]),
                                                 self.calc_percentage(data["neutral"], data["total"]),
                                                 self.calc_percentage(data["negative"], data["total"]),
                                                 self.calc_percentage(data["very_negative"], data["total"]))

        response = {
            "headline": "Social Media Analysis for " + str(search_terms),
            "sentence": "The overall sentiment of {} social media posts is {} with an average sentiment score of {}.".format(data["total"], data["general_opinion"], round(data["mean"],2)),
            "text_body": sentiments
            }

        # print(response["headline"])
        # print(response["sentence"])
        # print(response["text_body"])

        return response

    def calc_percentage(self, den, nom):
        return "{:2.1f}%".format(den/nom*100)

