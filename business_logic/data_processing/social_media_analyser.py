import base.singleton as sn
import base.log as l
import data_providers.data_wrappers.social_media_provider as sm_provider
import business_logic.nlp.nlp as nlp

import multiprocessing.pool as m_pool
import numpy as np
logger = l.Logger("SocialMediaAnalyser", 400)


class SocialMediaAnalyser(sn.Singleton):
    def __init__(self):
        self.sm_provider = sm_provider.SocialMediaProvider.get_instance()
        self.nlp = nlp.NLP.get_instance()

    def get_social_media_trends(self, request_dict):
        keywords = request_dict["keywords"]
        posts_likes = self.sm_provider.get_posts_by_keywords(keywords)
        pool = m_pool.ThreadPool(processes=len(posts_likes))

        async_result = pool.map_async(self.nlp.get_emotions_score, [p["text"] for p in posts_likes])
        emotions = async_result.get()

        hist = np.histogram(emotions, bins=np.linspace(-1, 1, 10))
        mean = np.mean(emotions)
        total_posts = len(posts_likes)
        hist_str = "\n".join([
            "{}{:1.3f}: {:2.0f} {}".format(
                "" if l < 0 else " ",  # compensate for minus
                l,
                (n*100) / total_posts,
                "="*(n*100 // total_posts))
            for n, l in zip(hist[0], hist[1])
        ])
        logger.log("got emotion magnitude distribution for keywords {}:\n"
                   " mean: {}\n"
                   "{}".format(
                        keywords, mean, hist_str
                    )
        )

        return None  # todo decide what to return


if __name__ == "__main__":
    sm_analyser = SocialMediaAnalyser.get_instance()

    sm_analyser.get_social_media_trends({"keywords": ["Trump"]})
    sm_analyser.get_social_media_trends({"keywords": ["Tesco"]})
    sm_analyser.get_social_media_trends({"keywords": ["Apple"]})
