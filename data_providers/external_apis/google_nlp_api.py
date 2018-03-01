import base.singleton as sn
import base.log as l

import google.cloud as gl_cloud
import google.cloud.language as gl_lang
import data_providers.external_apis.google_nlp_enum_string as maps

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
                "part_of_speech": token.part_of_speech.tag,
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

class Node:
    def __init__(self, data, children=()):
        self.children = list(children)
        self.data = data
        self.int_mappers = {
            "dependency_edge": maps.dependency_edge,
            "part_of_speech": maps.part_of_speech
        }

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def __str__(self, use_int_mappers=True, level=0):
        ret = "\t" * 2 * level
        data_string = ""

        if use_int_mappers and type(self.data) is dict:
            temp_data = self.data.copy()
            for key in temp_data.keys():
                if key in self.int_mappers.keys():
                    temp_data[key] = self.int_mappers[key][temp_data[key]]
            ret += "({})\n".format(temp_data)
        else:
            ret += "({})\n".format(self.data)


        for child in self.children:
            ret += child.__str__(use_int_mappers, level + 1)
        return ret

    def __repr__(self):
        return "<node>"