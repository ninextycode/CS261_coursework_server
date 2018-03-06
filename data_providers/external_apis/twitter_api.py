import base.singleton as sn
import TwitterAPI as twitter
import json
from data_providers.external_apis import twitter_key_path


# todo either change key or throw meaningfil exception/give meaningful response when limit reached
class TwitterApi(sn.Singleton):
    class ResultType:
        mixed = 'mixed',
        recent = 'recent',
        popular = 'recent'

    def __init__(self):
        self.name = 'TwitterApi'
        self.keys_dict = json.loads(open(twitter_key_path, 'r').read())
        self.twitter_api = twitter.TwitterAPI(consumer_key=self.keys_dict['consumer_key'],
                                              consumer_secret=self.keys_dict['consumer_secret'],
                                              access_token_key=self.keys_dict['access_token_key'],
                                              access_token_secret=self.keys_dict['access_token_secret'])
        self.querying_types = [
            # TwitterApi.ResultType.popular,
            # TwitterApi.ResultType.recent,
            TwitterApi.ResultType.mixed
        ]

    def get_posts_by_keywords(self, keywords):
        results_dict = {}
        for req_type in self.querying_types:

            query = self.generate_search_query(keywords, req_type)
            results_local = self.twitter_api.request('search/tweets', query)

            # no id duplicates if same post received with different request types
            for t in results_local:
                results_dict[t['id']] = {
                    'text': t['full_text'],
                    'likes': t['favorite_count']
                }
        return list(results_dict.values())

    def generate_search_query(self, keywords, req_type, join_or=False):
        joiner = ' OR ' if join_or else ' AND '
        q = joiner.join(keywords)
        return {
            'count': 100,
            'q': q,
            'result_type': req_type,
            'lang': 'en',
            'tweet_mode': 'extended'
        }

    def __str__(self):
        return self.name


if __name__ == '__main__':
    twitter_api = TwitterApi.get_instance()
    tweets = twitter_api.get_posts_by_keywords(['Trump'])
    print(list(tweets)[0])
    print(len(tweets))
