from typing import Sequence, Mapping, Optional
from collections import defaultdict

import spacy

from named_entity_recognition import NamedEntityRecognition
from data import Article


class Spacy(NamedEntityRecognition):
    def __init__(self, num_worker: int):
        self.num_worker = num_worker

    def extract(self, articles: Sequence[Article]) -> Mapping[str, Sequence[Article]]:
        nlp = spacy.load("en_core_web_sm")

        article_entities = [
            frozenset(Spacy.__get_persons(article))
            for article in nlp.pipe(
                (str(article.content) for article in articles),
                n_threads=self.num_worker,
                batch_size=32,
            )
        ]

        entities = defaultdict(list)
        for article, local_entities in zip(articles, article_entities):
            for entity in local_entities:
                entities[entity].append(article)

        return entities

    @staticmethod
    def __get_persons(document) -> Optional[str]:
        for entity in document.ents:
            # Filter entities not of further interest
            if entity.label_ != "PERSON" or len(entity.lemma_) == 0:
                continue

            # Get multiple parts of the name
            name_parts = entity.lemma_.split()

            # Remove potential "'s" at the end of names
            if len(name_parts[-1]) <= 3:
                name_parts = name_parts[:-1]

            # Still a valid entity, but not of further interest.
            if len(name_parts) < 2:
                continue

            # Remove possible mittle names and return only given name and surname
            yield "{} {}".format(
                name_parts[0].capitalize(), name_parts[-1].capitalize()
            )
