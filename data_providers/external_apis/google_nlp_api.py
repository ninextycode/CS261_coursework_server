import base.singleton as sn
import base.log as l

import google.cloud as gl_cloud
import google.cloud.language as gl_lang
import requests

logger = l.Logger("GoogleNlpApi", None)


# todo catch exceptions or pass retry object to retry calls at least 1 time

class GoogleNlpApi(sn.Singleton):
    def __init__(self):
        self.emotions_api = GoogleNlpApiEmotions.get_instance()
        self.meaning_api = GoogleNlpApiMeaning.get_instance()

    def query_emotions(self, *args, **kwargs):
        return self.emotions_api.query_emotions(*args, **kwargs)

    def query_meaning(self, *args, **kwargs):
        return self.meaning_api.query_meaning(*args, **kwargs)


class GoogleNlpApiEmotions(sn.Singleton):
    def __init__(self):
        self.client = gl_cloud.language.LanguageServiceClient()

    def query_emotions(self, text, by_sentence):
        document = gl_lang.types.Document(
            content=text,
            type=gl_lang.enums.Document.Type.PLAIN_TEXT,
            language="en"
        )

        api_response = self.client.analyze_sentiment(document=document)

        if by_sentence:
            return self.emotions_response_by_sentences(api_response)
        else:
            return self.emotions_response_overall(api_response)

    def emotions_response_overall(self, api_response):
        if api_response is None:
            return {
                "score": 0,
                "magnitude": 0
            }

        return {
            "score": api_response.document_sentiment.score,
            "magnitude": api_response.document_sentiment.magnitude,
        }

    def emotions_response_by_sentences(self, api_response):
        if api_response is None:
            return []

        return [{
            "score": s.sentiment.score,
            "magnitude": s.sentiment.magnitude,
        } for s in api_response.sentences]


class GoogleNlpApiMeaning(sn.Singleton):
    def query_meaning(self, text):
        document = gl_lang.types.Document(
            content=text,
            type=gl_lang.enums.Document.Type.PLAIN_TEXT,
            language="en"
        )

        features = {
            "extract_syntax": True,
            "extract_entities": True
        }

        api_response = self.client.annotate_text(document=document, features=features)

        result = {
            "keywords": self.get_keywords(api_response),
            "raw": api_response,
            "tree": self.construct_tree(api_response)
        }

        return result

    def construct_tree(self, response):
        nodes = []
        for token in response.tokens:
            token_node_data = {
                "text":  token.text.content,
                "lemma": token.lemma,
                "dependency_edge": token.dependency_edge.label,
                "part_of_speech": token.part_of_speech.tag
            }
            nodes.append(Node(token_node_data))

        root_index = None
        for i, token in enumerate(response.tokens):
            if token.dependency_edge.label == gl_lang.enums.DependencyEdge.Label.ROOT:
                root_index = i
            else:
                parent_index = token.dependency_edge.head_token_index
                nodes[parent_index].add_child(nodes[i])

        return {"root": nodes[root_index], "nodes": nodes}

    def get_keywords(self, response):
        keywords = []
        for e in response.entities:
            keywords.append({
                "word": e.name,
                "type": e.type,
                "is_proper": e.mentions[0].type == gl_lang.enums.EntityMention.Type.PROPER,
                "importance": e.salience
            })
            return keywords


# used to construct a tree of word relationships
class Node:
    def __init__(self, data, children=()):
        self.children = list(children)
        self.data = data

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def __str__(self, level=0):
        ret = "\t" * 2 * level + "({0})\n".format(repr(self.data))

        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return "<tree>"