import base.log as l
import base.singleton as sn
import data_providers.external_apis.twitter_api as twitter_api


logger = l.Logger('SocialMediaProvider')


class SocialMediaProvider(sn.Singleton):
    def __init__(self):
        self.social_media_apis = [
            twitter_api.TwitterApi.get_instance(),
            # potentially add more
        ]

    def get_posts_from_given_media_by_keywords(self, media_provider, keywords):
        return media_provider.get_posts_by_keywords(keywords)

    def get_posts_by_keywords(self, keywords):
        posts = []

        for api in self.social_media_apis:
            from_this_api = self.get_posts_from_given_media_by_keywords(api, keywords)
            logger.log('got {} posts from {} for keywords {}'.format(
                len(from_this_api), str(api.name), keywords)
            )
            posts.extend(from_this_api)
        return posts
