from typing import Sequence, Mapping, Iterator
from collections import defaultdict

import spacy

from named_entity_recognition import NamedEntityRecognition
from data import Article


class Spacy(NamedEntityRecognition):
    """
    Extracting names from articles using SpaCy.
    """

    def __init__(self, num_worker: int):
        """
        Create a new parser.
        :param num_worker: The number of simultanously used worker.
        """
        self.num_worker = num_worker

    def extract(self, articles: Sequence[Article]) -> Mapping[str, Sequence[Article]]:
        """
        Extract the names of persons from a given sequence of articles.
        :param articles: The input articles.
        :return: A structure mapping entities to the articles containing them.
        """

        nlp = spacy.load("en_core_web_sm")

        # Create for each article a set with the contained names.
        article_entities = [
            frozenset(Spacy.__get_persons(article))
            for article in nlp.pipe(
                (str(article.content) for article in articles),
                n_threads=self.num_worker,
                batch_size=32,
            )
        ]

        # Create the final mapping.
        entities = defaultdict(list)
        for article, local_entities in zip(articles, article_entities):
            for entity in local_entities:
                entities[entity].append(article)

        return entities

    @staticmethod
    def __get_persons(document) -> Iterator[str]:
        """
        A generator for valid person names in a document.
        :param document: A document parsed by SpaCy.
        :return: A Generator yielding formatted person names.
        """

        for entity in document.ents:
            # Filter entities not of further interest
            if entity.label_ != "PERSON" or len(entity.lemma_) == 0:
                continue

            # Get multiple parts of the name
            name_parts = entity.lemma_.split()

            # Remove potential "'s" at the end of names
            if len(name_parts[-1]) <= 3:
                name_parts = name_parts[:-1]

            # Still a valid entity, but not a typical name with at least two parts.
            if len(name_parts) < 2:
                continue

            # Remove possible mittle names and return only given name and surname
            yield "{} {}".format(
                name_parts[0].capitalize(), name_parts[-1].capitalize()
            )
