import base.singleton as sn
import data_providers.external_apis.google_nlp_api as gl_nlp


class GoogleEmotionExtractor(sn.Singleton):
    def __init__(self):
        self.nlp_api = gl_nlp.GoogleNlpApi.get_instance()

    def get_emotions(self, text, by_sentences):
        return self.nlp_api.query_emotions(text, by_sentences)

    def get_emotions_score(self, text, by_sentences):
        result = self.get_emotions(text, by_sentences)
        if by_sentences:
            return [r["score"] for r in result]
        else:
            return result["score"]

    def get_emotions_magnitude(self, text, by_sentences):
        result = self.get_emotions(text, by_sentences)
        if by_sentences:
            return [r["magnitude"] for r in result]
        else:
            return result["magnitude"]


if __name__ == "__main__":
    gee = GoogleEmotionExtractor.get_instance()
    sentences = [
        "I really hate this place",
        "I love this place a lot",
    ] * 2
    print([gee.get_emotions_score(s, False) for s in sentences])
    print(gee.get_emotions_score(". ".join(sentences) + ".", True))
