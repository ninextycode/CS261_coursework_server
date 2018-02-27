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

    def get_emotions(self, text, by_sentences=False):
        return self.emotions_extractor.get_emotions(text, by_sentences)

    def get_emotions_score(self, text, by_sentences=False):
        return self.emotions_extractor.get_emotions_score(text, by_sentences)

    def get_emotions_magnitude(self, text, by_sentences=False):
        return self.emotions_extractor.get_emotions_magnitude(text, by_sentences)