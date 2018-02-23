import base.singleton as sn
import base.log as l

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


logger = l.Logger("GoogleSpeechRecognitionApi")


class GoogleSpeechRecognitionApi(sn.Singleton):
    def __init__(self):
        self.client = speech.SpeechClient()

    def query(self, audio_bytes_dict, n_alternatives=30):
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code='en-GB',
            max_alternatives=n_alternatives
        )

        content = audio_bytes_dict["bytes"]
        audio = types.RecognitionAudio(content=content)

        response = self.client.recognize(config, audio)
        if len(response.results) == 0:
            return []

        alternatives_list = [{"transcript": a.transcript, "confidence": a.confidence}
                             for a in response.results[0].alternatives]
        logger.log('Transcript: {}'.format(alternatives_list))

        return alternatives_list