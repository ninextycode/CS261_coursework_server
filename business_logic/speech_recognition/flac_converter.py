import base.singleton as sn

import pydub
import tempfile
import io
import base64
import business_logic.data_tags as tags
import base.log as l


logger = l.Logger("FlacConverter")


class FlacConverter(sn.Singleton):


    def __init__(self):
        pass

    def to_flac(self, audio_bytes_dict):
        given_mime = audio_bytes_dict["mime_type"]
        ext = given_mime.split("/")[1]
        given_bytes = audio_bytes_dict["bytes"]

        with tempfile.NamedTemporaryFile(suffix="."+ext) as temp_file, io.BytesIO() as flac_bytes:
            temp_file.write(given_bytes)
            audio_segment = pydub.AudioSegment.from_file(temp_file.name, ext).set_channels(1)

            should_update = audio_segment.channels != 1 or given_bytes != tags.MimeTypes.flac

            if audio_segment.channels != 1:
                audio_segment = pydub.AudioSegment.from_file(temp_file.name, ext).set_channels(1)

            if should_update:
                audio_segment.export(flac_bytes, format="flac")

            audio_bytes_dict["bytes"] = flac_bytes.getvalue()

        return audio_bytes_dict
