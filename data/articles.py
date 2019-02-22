import requests

from typing import Sequence, Tuple


class Article:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

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
    def load_all() -> Sequence["Article"]:
        params = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "apfilterredir": "nonredirects",
            "aplimit": "max",
        }

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

        return articles
