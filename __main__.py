from pathlib import Path
import logging
import pickle
from typing import Sequence

from data import Article


def get_articles() -> Sequence[Article]:
    CACHE_NAME = "articles.pkl"

    if not Path(CACHE_NAME).exists():
        logging.info("Extracting available articles from WikiNews...")
        articles = Article.from_wikinews()
        with open(CACHE_NAME, "wb") as output:
            pickle.dump(articles, output, pickle.HIGHEST_PROTOCOL)
    else:
        with open(CACHE_NAME, "rb") as input:
            articles = pickle.load(input)

    return articles


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    articles = get_articles()
