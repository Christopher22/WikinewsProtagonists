from pathlib import Path
import logging
import pickle
from typing import Sequence
import multiprocessing

from data import Article, ArticleContent


def get_articles() -> Sequence[Article]:
    CACHE_NAME = "articles.pkl"

    if not Path(CACHE_NAME).exists():
        logging.info("Extracting available articles from WikiNews...")
        articles = Article.load_all()
        with open(CACHE_NAME, "wb") as output:
            pickle.dump(articles, output, pickle.HIGHEST_PROTOCOL)
    else:
        with open(CACHE_NAME, "rb") as input:
            articles = pickle.load(input)

    return Article.filter_articles(articles)


def get_texts():
    CACHE_NAME = "texts.pkl"

    if not Path(CACHE_NAME).exists():
        logging.info("Extracting available articles from WikiNews...")
        with multiprocessing.Pool(8) as pool:
            texts = list(
                pool.imap_unordered(ArticleContent.from_article, get_articles())
            )
        with open(CACHE_NAME, "wb") as output:
            pickle.dump(texts, output, pickle.HIGHEST_PROTOCOL)
    else:
        with open(CACHE_NAME, "rb") as input:
            texts = pickle.load(input)

    return [ArticleContent(text, optimize=True) for text in texts]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    texts = get_texts()
