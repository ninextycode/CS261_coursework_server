import datetime


class Logger:
    def __init__(self, prefix, max_len=300):
        self.prefix = prefix
        self.max_len = max_len

    def log(self, *message):
        if self.prefix == "GoogleCommandExtractor" or self.prefix == "GoogleSpeechRecognitionApi":
            output = " ".join([str(s) for s in [datetime.datetime.now(), self.prefix, "\t", *message]])
            if self.max_len is not None and len(output) > self.max_len:
                output = output[0:self.max_len] + "..."
            print(output)

