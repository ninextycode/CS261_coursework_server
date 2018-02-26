import base.singleton as sn
import business_logic.speech_recognition.flac_converter as fc
import data_providers.external_apis.google_speech_recognition_api as speech_api


class GoogleAudioToText(sn.Singleton):
    def __init__(self):
        self.flac_converter = fc.FlacConverter.get_instance()
        self.speech_api = speech_api.GoogleSpeechRecognitionApi().get_instance()

    def get_alternatives(self, audio_bytes_dict):
        audio_bytes_dict = self.flac_converter.to_flac(audio_bytes_dict)
        response = self.speech_api.query(audio_bytes_dict)
        return response

