from typing import Sequence, Mapping, Iterable
from collections import OrderedDict, defaultdict

from stanfordcorenlp import StanfordCoreNLP

from data import Article
from named_entity_recognition import NamedEntityRecognition


class Stanford(NamedEntityRecognition):
    def __init__(self, path: str):
        self.path = path

    def extract(self, articles: Sequence[Article]) -> Mapping[str, Sequence[Article]]:
        entities = defaultdict(list)

        with StanfordCoreNLP(self.path, lang="en") as nlp:
            for article in articles:
                # No completly nice to access the internals directly - but nlp.ner does not provide enough info
                corenlp_output = nlp._request("ner", str(article.content))

                # A set with all the found entities in a single article
                local_entities = set()

                # Iterate through sentences
                for sentence in corenlp_output["sentences"]:
                    tokens = OrderedDict(
                        (token["index"], token["lemma"])
                        for token in sentence["tokens"]
                        if token["ner"] == "PERSON"
                    )

                    # Add entities of the sentence to the local set
                    local_entities.update(
                        "{} {}".format(tokens[name[0]], tokens[name[-1]])
                        for name in Stanford.get_continue_elements(tuple(tokens.keys()))
                        if len(name) > 1
                    )

                for entity in local_entities:
                    entities[entity].append(article)

        return entities

    @staticmethod
    def get_continue_elements(inputs: Sequence[int]) -> Iterable[Sequence[int]]:
        last_input = None
        start = 0

        for index, input in enumerate(inputs):
            if last_input is not None and input - last_input > 1:
                yield inputs[start:index]
                start = index
            last_input = input

        if start != len(inputs):
            yield inputs[start:]
