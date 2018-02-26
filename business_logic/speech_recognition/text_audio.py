import base.singleton as sn
import business_logic.speech_recognition.google_audio_to_text as google_audio
import base64


class TextAudio(sn.Singleton):
    def __init__(self):
        self.api_caller = google_audio.GoogleAudioToText.get_instance()

    def get_alternatives(self, audio_json):
        audio_bytes_dict = {
            "mime_type": audio_json["mime_type"],
            "bytes": self.get_bytes(audio_json)
        }
        return self.api_caller.get_alternatives(audio_bytes_dict)

    def get_bytes(self, audio_json):
        if audio_json["is_base64"]:
            return base64.b64decode(audio_json["content"])
        else:
            raise NotImplementedError("Audio should be encoded in base64")

    def text_to_audio(self, throw):
        raise NotImplementedError("text_to_audio not implemented yet")