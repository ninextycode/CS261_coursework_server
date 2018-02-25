import base.singleton as si

import business_logic.nlp.pattern_based_extractor as pbe
import business_logic.nlp.google_command_extractor as gce
import business_logic.nlp.google_emotion_extractor as gee

import business_logic.nlp.summariser as summariser


class NLP(si.Singleton):
    def __init__(self):
        self.command_extractor = gce.GoogleCommandExtractor.get_instance()
        self.emotions_extractor = gee.GoogleEmotionExtractor.get_instance()
        self.summariser = summariser.Summariser.get_instance()

    def get_meaning_from_single(self, string):
        return self.command_extractor.get_meaning_from_single(string)

    def get_meaning_from_alternatives(self, string):
        return self.command_extractor.get_meaning_from_alternatives(string)

    def summarise_url(self, url):
        return self.summariser.summarise_url(url)

    # “Clearly positive” and “clearly negative” sentiment varies for different
    # use cases and customers. You might find differing results for your specific scenario.
    # We recommend that you define a threshold that works for you, and then adjust the
    # threshold after testing and verifying the results. For example, you may define a threshold of
    # any score over 0.25 as clearly positive, and then modify the score threshold to 0.15 after reviewing your
    # data and results and finding that scores from 0.15-0.25 should be considered positive as well.
    # (https://cloud.google.com/)
    def get_emotions(self, text, by_sentences=False):
        return self.emotions_extractor.get_emotions(text, by_sentences)

    def get_emotions_score(self, text, by_sentences=False):
        return self.emotions_extractor.get_emotions_score(text, by_sentences)

    def get_emotions_magnitude(self, text, by_sentences=False):
        return self.emotions_extractor.get_emotions_magnitude(text, by_sentences)