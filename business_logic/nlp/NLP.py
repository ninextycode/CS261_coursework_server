import PatternBasedeExtractor as pbe

class NLP:
    def __init__(self):
        self.extractor = pbe.PatternBasedeExtractor()

    def get_meaning(self, string):
        return self.extractor.ge_meanong(string)