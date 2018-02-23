import base.singleton as sn
import base.log as l

import google.cloud as gl_cloud
import google.cloud.speech as gl_speech


logger = l.Logger("GoogleSpeechRecognitionApi")


class GoogleSpeechRecognitionApi(sn.Singleton):
    def __init__(self):
        self.client = gl_cloud.speech.SpeechClient()

    def query(self, audio_bytes_dict, n_alternatives=30):
        config = gl_speech.types.RecognitionConfig(
            encoding=gl_speech.enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code='en-GB',
            max_alternatives=n_alternatives
        )

        content = audio_bytes_dict["bytes"]
        audio = gl_speech.types.RecognitionAudio(content=content)

        response = self.client.recognize(config, audio)
        if len(response.results) == 0:
            return []

        alternatives_list = [{"transcript": a.transcript, "confidence": a.confidence}
                             for a in response.results[0].alternatives]
        logger.log('Transcript: {}'.format(alternatives_list))

        return alternatives_list