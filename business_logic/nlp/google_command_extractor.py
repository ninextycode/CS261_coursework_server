import base.singleton as sn
import business_logic.nlp.pattern_based_extractor as pbe
import business_logic.nlp.nlp_exceptions as ex
import data_providers.external_apis.google_nlp_api as google_nlp
import google.cloud.language as gl_lang
import base.log as l


logger = l.Logger("GoogleCommandExtractor", 500)


class GoogleCommandExtractor(sn.Singleton):
    labels = {
        gl_lang.enums.DependencyEdge.Label.UNKNOWN: "Unknown",
        gl_lang.enums.DependencyEdge.Label.ABBREV: "Abbreviation modifier",
        gl_lang.enums.DependencyEdge.Label.ACOMP: "Adjectival complement",
        gl_lang.enums.DependencyEdge.Label.ADVCL: "Adverbial clause modifier",
        gl_lang.enums.DependencyEdge.Label.ADVMOD: "Adverbial modifier",
        gl_lang.enums.DependencyEdge.Label.AMOD: "Adjectival modifier of an NP",
        gl_lang.enums.DependencyEdge.Label.APPOS: "Appositional modifier of an NP",
        gl_lang.enums.DependencyEdge.Label.ATTR: "Attribute dependent of a copular verb",
        gl_lang.enums.DependencyEdge.Label.AUX: "Auxiliary (non-main) verb",
        gl_lang.enums.DependencyEdge.Label.AUXPASS: "Passive auxiliary",
        gl_lang.enums.DependencyEdge.Label.CC: "Coordinating conjunction",
        gl_lang.enums.DependencyEdge.Label.CCOMP: "Clausal complement of a verb or adjective",
        gl_lang.enums.DependencyEdge.Label.CONJ: "Conjunct",
        gl_lang.enums.DependencyEdge.Label.CSUBJ: "Clausal subject",
        gl_lang.enums.DependencyEdge.Label.CSUBJPASS: "Clausal passive subject",
        gl_lang.enums.DependencyEdge.Label.DEP: "Dependency (unable to determine)",
        gl_lang.enums.DependencyEdge.Label.DET: "Determiner",
        gl_lang.enums.DependencyEdge.Label.DISCOURSE: "Discourse",
        gl_lang.enums.DependencyEdge.Label.DOBJ: "Direct object",
        gl_lang.enums.DependencyEdge.Label.EXPL: "Expletive",
        gl_lang.enums.DependencyEdge.Label.GOESWITH: "Goes with (part of a word in a text not well edited)",
        gl_lang.enums.DependencyEdge.Label.IOBJ: "Indirect object",
        gl_lang.enums.DependencyEdge.Label.MARK: "Marker (word introducing a subordinate clause)",
        gl_lang.enums.DependencyEdge.Label.MWE: "Multi-word expression",
        gl_lang.enums.DependencyEdge.Label.MWV: "Multi-word verbal expression",
        gl_lang.enums.DependencyEdge.Label.NEG: "Negation modifier",
        gl_lang.enums.DependencyEdge.Label.NN: "Noun compound modifier",
        gl_lang.enums.DependencyEdge.Label.NPADVMOD: "Noun phrase used as an adverbial modifier",
        gl_lang.enums.DependencyEdge.Label.NSUBJ: "Nominal subject",
        gl_lang.enums.DependencyEdge.Label.NSUBJPASS: "Passive nominal subject",
        gl_lang.enums.DependencyEdge.Label.NUM: "Numeric modifier of a noun",
        gl_lang.enums.DependencyEdge.Label.NUMBER: "Element of compound number",
        gl_lang.enums.DependencyEdge.Label.P: "Punctuation mark",
        gl_lang.enums.DependencyEdge.Label.PARATAXIS: "Parataxis relation",
        gl_lang.enums.DependencyEdge.Label.PARTMOD: "Participial modifier",
        gl_lang.enums.DependencyEdge.Label.PCOMP: "The complement of a preposition is a clause",
        gl_lang.enums.DependencyEdge.Label.POBJ: "Object of a preposition",
        gl_lang.enums.DependencyEdge.Label.POSS: "Possession modifier",
        gl_lang.enums.DependencyEdge.Label.POSTNEG: "Postverbal negative particle",
        gl_lang.enums.DependencyEdge.Label.PRECOMP: "Predicate complement",
        gl_lang.enums.DependencyEdge.Label.PRECONJ: "Preconjunt",
        gl_lang.enums.DependencyEdge.Label.PREDET: "Predeterminer",
        gl_lang.enums.DependencyEdge.Label.PREF: "Prefix",
        gl_lang.enums.DependencyEdge.Label.PREP: "Prepositional modifier",
        gl_lang.enums.DependencyEdge.Label.PRONL: "The relationship between a verb and verbal morpheme",
        gl_lang.enums.DependencyEdge.Label.PRT: "Particle",
        gl_lang.enums.DependencyEdge.Label.PS: "Associative or possessive marker",
        gl_lang.enums.DependencyEdge.Label.QUANTMOD: "Quantifier phrase modifier",
        gl_lang.enums.DependencyEdge.Label.RCMOD: "Relative clause modifier",
        gl_lang.enums.DependencyEdge.Label.RCMODREL: "Complementizer in relative clause",
        gl_lang.enums.DependencyEdge.Label.RDROP: "Ellipsis without a preceding predicate",
        gl_lang.enums.DependencyEdge.Label.REF: "Referent",
        gl_lang.enums.DependencyEdge.Label.REMNANT: "Remnant",
        gl_lang.enums.DependencyEdge.Label.REPARANDUM: "Reparandum",
        gl_lang.enums.DependencyEdge.Label.ROOT: "Root",
        gl_lang.enums.DependencyEdge.Label.SNUM: "Suffix specifying a unit of number",
        gl_lang.enums.DependencyEdge.Label.SUFF: "Suffix",
        gl_lang.enums.DependencyEdge.Label.TMOD: "Temporal modifier",
        gl_lang.enums.DependencyEdge.Label.TOPIC: "Topic marker",
        gl_lang.enums.DependencyEdge.Label.VMOD: "Clause headed by an infinite form of the verb that modifies a noun",
        gl_lang.enums.DependencyEdge.Label.VOCATIVE: "Vocative",
        gl_lang.enums.DependencyEdge.Label.XCOMP: "Open clausal complement",
        gl_lang.enums.DependencyEdge.Label.SUFFIX: "Name suffix",
        gl_lang.enums.DependencyEdge.Label.TITLE: "Name title",
        gl_lang.enums.DependencyEdge.Label.ADVPHMOD: "Adverbial phrase modifier",
        gl_lang.enums.DependencyEdge.Label.AUXCAUS: "Causative auxiliary",
        gl_lang.enums.DependencyEdge.Label.AUXVV: "Helper auxiliary",
        gl_lang.enums.DependencyEdge.Label.DTMOD: "Rentaishi (Prenominal modifier)",
        gl_lang.enums.DependencyEdge.Label.FOREIGN: "Foreign words",
        gl_lang.enums.DependencyEdge.Label.KW: "Keyword",
        gl_lang.enums.DependencyEdge.Label.LIST: "List for chains of comparable items",
        gl_lang.enums.DependencyEdge.Label.NOMC: "Nominalized clause",
        gl_lang.enums.DependencyEdge.Label.NOMCSUBJ: "Nominalized clausal subject",
        gl_lang.enums.DependencyEdge.Label.NOMCSUBJPASS: "Nominalized clausal passive",
        gl_lang.enums.DependencyEdge.Label.NUMC: "Compound of numeric modifier",
        gl_lang.enums.DependencyEdge.Label.COP: "Copula",
        gl_lang.enums.DependencyEdge.Label.DISLOCATED: "Dislocated relation (for fronted/topicalized elements)",
        gl_lang.enums.DependencyEdge.Label.ASP: "Aspect marker",
        gl_lang.enums.DependencyEdge.Label.GMOD: "Genitive modifier",
        gl_lang.enums.DependencyEdge.Label.GOBJ: "Genitive object",
        gl_lang.enums.DependencyEdge.Label.INFMOD: "Infinitival modifier",
        gl_lang.enums.DependencyEdge.Label.MES: "Measure",
        gl_lang.enums.DependencyEdge.Label.NCOMP: "Nominal complement of a noun",
    }

    def __init__(self):
        self.pattern_based_extractor = pbe.PatternBasedExtractor.get_instance()
        self.google_api = google_nlp.GoogleNlpApi.get_instance()

    def get_meaning(self, text):
        meaning = None
        try:
            meaning = self.pattern_based_extractor.get_meaning(text)
        except ex.MeaningUnknown:
            logger.log("Cannot get meaning using patterns")

        google_api_output = self.google_api.query(text)


        tree = google_api_output["tree"]
        keywords = google_api_output["keywords"]

        logger.log("tree:\n {}".format(tree["root"]))
        logger.log("keywords {}".format(keywords))


        return meaning

    def construct_tree(self, text):
        pass
