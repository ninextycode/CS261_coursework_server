import base.log as l
import base.singleton as sn


import sumy.parsers.html as s_html
import sumy.nlp.tokenizers as s_tokenizers

import sumy.nlp.stemmers as s_stemmers
import sumy.utils as s_utils

from sumy.summarizers.luhn import LuhnSummarizer as Summarizer

logger = l.Logger('SummarisationWithSumy')


class SummarisationWithSumy(sn.Singleton):
    def __init__(self):
        self.language = 'english'
        self.sentences_count = 7
        self.stemmer = s_stemmers.Stemmer(self.language)
        self.summarizer = Summarizer(self.stemmer)
        self.summarizer.stop_words = s_utils.get_stop_words(self.language)

    def summarise_url(self, url):
        try:
            return self.unsafe_summarise_url(url)
        except Exception as e:
            logger.log(' exception {}'.format(e))
            return None

    def unsafe_summarise_url(self,  url):
        parser = s_html.HtmlParser.from_url(url, s_tokenizers.Tokenizer(self.language))

        logger.log(' tried to summarise {}'.format(url))

        summary =  '\n'.join([str(s) for s in self.summarizer(parser.document, self.sentences_count)])
        summary += '\n (Summary created with sumy 0.7.0 library)'

        return summary


if __name__ == '__main__':
    sum = SummarisationWithSumy.get_instance()
    url = 'https://www.wsj.com/amp/articles/apple-to-start-putting-sensitive-encryption-keys-in-china-1519497574'
    print(sum.summarise_url(url))

    url = 'https://en.wikipedia.org/wiki/Wikipedia:About'
    print(sum.summarise_url(url))