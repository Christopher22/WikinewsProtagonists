import multiprocessing
from typing import Sequence, Optional
import logging

import requests

from data import ArticleContent


def _enrich_article(article: "Article") -> "Article":
    article.content = ArticleContent.from_id(article.id)
    return article


class Article:
    def __init__(self, id: int, title: str, content: Optional[ArticleContent] = None):
        self.id = id
        self.title = title
        self.content = content

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def get_url(self):
        return "https://en.wikinews.org/?curid={}".format(self.id)

    @staticmethod
    def filter_articles(articles: Sequence["Article"]) -> Sequence["Article"]:
        return [
            article
            for article in articles
            if all(
                filter_word not in article.title.lower()
                for filter_word in ("shorts", "interview")
            )
        ]

    @staticmethod
    def from_wikinews(num_worker: int = 8) -> Sequence["Article"]:
        params = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "apfilterredir": "nonredirects",
            "aplimit": "max",
        }

        logging.info("Downloading article meta...")

        # Create all the article stumbs
        articles = []
        while True:
            # Get the response and parse it as JSON
            response = requests.get(
                "https://en.wikinews.org/w/api.php", params=params
            ).json()

            # Add all the articles available to the list
            articles.extend(
                Article(id=page["pageid"], title=page["title"])
                for page in response["query"]["allpages"]
            )

            # If further data is available...
            if "continue" in response:
                # ... set the required parameter to continue
                params.update(response["continue"])
            else:
                # ... or end the loading otherwise.
                break

        # Exclude articles not of further interest
        logging.info("%s articles downloaded. Filtering...", len(articles))
        articles = Article.filter_articles(articles)
        logging.info("%s articles remain after filtering.", len(articles))

        # Download the actual texts
        logging.info("Downloading all the texts...")
        with multiprocessing.Pool(num_worker) as pool:
            articles = pool.map(_enrich_article, articles)

        return articles
