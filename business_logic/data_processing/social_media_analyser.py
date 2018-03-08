import base.singleton as sn
import base.log as l
import data_providers.data_wrappers.social_media_provider as sm_provider
import business_logic.nlp.nlp as nlp
import business_logic.data_tags as tags


import multiprocessing.pool as m_pool
import numpy as np
logger = l.Logger('SocialMediaAnalyser', None)


class SocialMediaAnalyser(sn.Singleton):
    def __init__(self):
        self.sm_provider = sm_provider.SocialMediaProvider.get_instance()
        self.nlp = nlp.NLP.get_instance()
        self.threshold_0 = 0.15
        self.threshold_1 = 0.45

    def get_public_opinion(self, request_dict):
        keywords = request_dict['keywords']
        posts_likes = self.sm_provider.get_posts_by_keywords(keywords)
        pool = m_pool.ThreadPool(processes=len(posts_likes))

        async_result = pool.map_async(self.nlp.get_emotions_score, [p['text'] for p in posts_likes])
        emotions = np.array(async_result.get())

        return self.analytics(emotions, keywords)

    def analytics(self, emotions, keywords):
        hist = np.histogram(emotions, bins=np.linspace(-1, 1, 10))
        hist_str = self.hist_string(hist)
        logger.log('got emotion magnitude distribution for keywords {}:\n'
                   '{}'.format(keywords, hist_str))

        mean = np.mean(emotions)
        logger.log('mean: {}'.format(mean))

        total_posts = len(emotions)

        very_positive = np.sum(self.threshold_1 <= emotions)
        positive = np.sum((self.threshold_0 <= emotions) & (emotions < self.threshold_1))
        neutral = np.sum((-self.threshold_0 < emotions) & (emotions < self.threshold_0))
        negative = np.sum((-self.threshold_1 < emotions) & (emotions <= -self.threshold_0))
        very_negative = np.sum(emotions <= -self.threshold_1)

        response = {
            'very_positive': very_positive,
            'positive':      positive,
            'neutral':       neutral,
            'negative':      negative,
            'very_negative': very_negative,
            'total':         total_posts,
            'mean':          mean,
            'histrogram_string': hist_str,
            'general_opinion':    self.get_general_opinion(mean)
        }
        return response

    def get_general_opinion(self, mean):
        if mean >= self.threshold_0:
            return tags.Mood.positive
        if mean > -self.threshold_0:
            return tags.Mood.neutral
        return tags.Mood.negative

    def hist_string(self, hist):
        step = hist[1][1] - hist[1][0]

        total_posts = np.sum(hist[0])
        return '\n'.join([
            '{}{:1.3f}: {:2.0f} {}'.format(
                '' if l < 0 else ' ',   # compensate for minus
                l + step / 2,           # so labels are senters of the bins, not their corner
                (n * 100) / total_posts,
                '=' * (n * 100 // total_posts))
            for n, l in zip(hist[0], hist[1])
        ])


if __name__ == '__main__':
    sm_analyser = SocialMediaAnalyser.get_instance()

    print(sm_analyser.get_public_opinion({'keywords': ['fun']}))
    print(sm_analyser.get_public_opinion({'keywords': ['hate']}))
    print(sm_analyser.get_public_opinion({'keywords': ['Intel']}))
