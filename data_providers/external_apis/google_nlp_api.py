import base.singleton as sn
import base.log as l

import google.cloud as gl_cloud
import google.cloud.language as gl_lang


logger = l.Logger("GoogleNlpApi", None)


class GoogleNlpApi(sn.Singleton):
    def query(self, text):
        client = gl_cloud.language.LanguageServiceClient()

        document = gl_lang.types.Document(
            content=text,
            type=gl_lang.enums.Document.Type.PLAIN_TEXT,
            language="en"
        )

        features = {
            "extract_syntax": True,
            "extract_entities": True
        }

        api_response = client.annotate_text(document=document, features=features)

        logger.log(api_response)

        result = {
            "keywords": self.get_keywords(api_response),
            "raw": api_response,
            "tree": None
        }

        logger.log("prepared response {}".format(result))
        return result

    def construct_tree(self, response):
        tokens = []
        for t in response.tokens:


    def get_keywords(self, response):
        keywords = []
        for e in response.entities:
            logger.log(e)
            keywords.append({
                "word": e.name,
                "type": e.type,
                "is_proper": e.mentions[0].type == gl_lang.enums.EntityMention.Type.PROPER,
                "importance": e.salience
            })
        return keywords

    def enum_to_string(self, enum):
        pass #todo

class Node:
    def __init__(self, content):
        self.children = []
        self.parent = None
        self.content = content