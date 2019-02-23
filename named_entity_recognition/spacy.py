from typing import Sequence, Mapping
from collections import defaultdict

import spacy

from named_entity_recognition import NamedEntityRecognition
from data import Article


class Spacy(NamedEntityRecognition):
    def extract(self, articles: Sequence[Article]) -> Mapping[str, Sequence[Article]]:
        nlp = spacy.load("en_core_web_sm")

        article_entities = [
            frozenset(
                entity.lemma_.split()[
                    -1
                ]  # Extract the surname, if multiple name parts are available
                for entity in article.ents
                if entity.label_ == "PERSON" and len(entity.lemma_) > 0
            )
            for article in nlp.pipe(
                (str(article.content) for article in articles), n_threads=8, batch_size=32
            )
        ]

        entities = defaultdict(list)
        for article, local_entities in zip(articles, article_entities):
            for entity in local_entities:
                entities[entity.capitalize()].append(article)

        return entities
