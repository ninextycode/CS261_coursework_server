import base.singleton as sn
import base.log as l
import data_providers.external_apis as e_a


import requests
import json


logger = l.Logger("TextsummarizationNetApi")


class TextsummarizationNetApi(sn.Singleton):
    def __init__(self):
        self.api_url = "https://textanalysis-text-summarization.p.mashape.com/text-summarizer"
        self.sentences_count = 7

    def summarise_url(self, url):
        try:
            return self.unsafe_summarise_url(url)
        except Exception as e:
            logger.log(" exception {}".format(e))
            return None

    def unsafe_summarise_url(self,  url):
        params = {
            "url": url,
            "text": None,
            "sentnum": self.sentences_count
        }
        headers = {
            "X-Mashape-Key": open(e_a.summariser_key_path, "r").read(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(self.api_url, json.dumps(params), headers=headers)
        logger.log(" tried to summarise {}, status code: {}".format(url, response.status_code))

        summary = None
        if response.status_code == 200:
            summary = "\n".join(response.json()["sentences"])
            summary += "\n (Summary created with textsummarization.net)"
        return summary


if __name__ == "__main__":
    sum = TextsummarizationNetApi.get_instance()
    url = "https://www.wsj.com/amp/articles/apple-to-start-putting-sensitive-encryption-keys-in-china-1519497574"
    print(sum.summarise_url(url))