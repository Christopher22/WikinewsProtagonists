from abc import ABC, abstractmethod
from typing import Sequence, Mapping

from data import Article


class NamedEntityRecognition(ABC):
    @abstractmethod
    def extract(self, texts: Sequence[Article]) -> Mapping[str, Sequence[Article]]:
        raise NotImplementedError()
