from typing import Sequence, Mapping, Iterable
from collections import OrderedDict, defaultdict

from stanfordcorenlp import StanfordCoreNLP

from data import Article
from named_entity_recognition import NamedEntityRecognition


class Stanford(NamedEntityRecognition):
    """
    Extracting names from articles using Stanford CoreNLP.
    """

    def __init__(self, path: str):
        """
        Create a new parser.
        :param path: The path to the folder containing CoreNLP.
        """
        self.path = path

    def extract(self, articles: Sequence[Article]) -> Mapping[str, Sequence[Article]]:
        """
        Extract the names of persons from a given sequence of articles.
        :param articles: The input articles.
        :return: A structure mapping entities to the articles containing them.
        """

        entities = defaultdict(list)

        # Start CoreNLP and close it automatically afterward
        with StanfordCoreNLP(self.path, lang="en") as nlp:

            # Iterate through all articles
            for article in articles:

                # No completly nice to access the internals directly - but nlp.ner does not provide enough info.
                corenlp_output = nlp._request("ner", str(article.content))

                # A set with all the found entities in a single article
                local_entities = set()

                # Iterate through sentences
                for sentence in corenlp_output["sentences"]:
                    # Get all persons found in each sentence
                    tokens = OrderedDict(
                        (token["index"], token["lemma"])
                        for token in sentence["tokens"]
                        if token["ner"] == "PERSON"
                    )

                    # Add persons found in the sentence to the local set, if their name has at least two parts.
                    local_entities.update(
                        "{} {}".format(tokens[name[0]], tokens[name[-1]])
                        for name in Stanford.get_continue_elements(tuple(tokens.keys()))
                        if len(name) > 1
                    )

                # Add all names found to the global entity collection.
                for entity in local_entities:
                    entities[entity].append(article)

        return entities

    @staticmethod
    def get_continue_elements(inputs: Sequence[int]) -> Iterable[Sequence[int]]:
        """
        From a given sequence, extract all elements without gaps between them and return them as groups.
        :param inputs: The input sequence.
        :return: A list of groups.
        """

        start = 0

        # Run trough all items and their direct ancestors
        for index, (last_input, input) in enumerate(zip(inputs, inputs[1:]), start=1):
            # Return a group, if the indices are separated
            if input - last_input > 1:
                yield inputs[start:index]
                start = index

        # If not all elements were returned, return the rest.
        if start != len(inputs):
            yield inputs[start:]
