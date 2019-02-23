from abc import ABC, abstractmethod
from typing import Sequence, Mapping, Iterator
from pathlib import Path

from data import Article

TEMPLATE_HEAD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Extracted persons</title>
</head>
<body>
    <h1>Persons in WikiNews</h1>
"""

TEMPLATE_END = """
</body>
</html>
"""


class NamedEntityRecognition(ABC):
    @abstractmethod
    def extract(self, articles: Sequence[Article]) -> Mapping[str, Sequence[Article]]:
        raise NotImplementedError()

    def export(self, path: str, articles: Sequence[Article]):
        entities = self.extract(articles)
        with open(path, "w", encoding="utf8") as file:
            file.write(TEMPLATE_HEAD)
            file.writelines(NamedEntityRecognition.__list_generator(entities))
            file.writelines(TEMPLATE_END)

    @staticmethod
    def __list_generator(entities: Mapping[str, Sequence[Article]]) -> Iterator[str]:
        yield "<dl>"
        for entity, articles in entities.items():
            yield "<dt>{}</dt><dd><ul>".format(entity)
            for article in articles:
                yield '<li><a href="{}">{}</a></li>'.format(
                    article.get_url(), article.title
                )
            yield "</ul></dd>"
        yield "</dl>"
