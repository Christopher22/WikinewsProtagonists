import requests
import re

class ArticleContent:
    def __init__(self, content: str, optimize: bool):
        self.content = content
        if optimize:
            self.optimize()

    def __str__(self):
        return self.content

    def optimize(self):
        # Remove the first line with the date
        self.content = self.content[self.content.find("\n") :]

        # Replace a simple meta on beginning like "Peking, China - ..."
        intro_match = re.search(r"^[^\.!\?:]+-\s+", self.content)
        if intro_match is not None and intro_match.start() == 0:
            self.content = self.content[intro_match.end() :]

        # Remove any embedded images
        self.content = re.sub(r"[Ff]ile:.+\n", "", self.content)

        # Search the last occurrence of lines with a single word like 'Reference' or 'Source
        additional_data_match = re.search(
            r"(Related news)|(Sources?):?\n", self.content, re.IGNORECASE
        )
        if additional_data_match is not None:
            self.content = self.content[: additional_data_match.start()]

        # Remove unecessary whitespace at the beginning
        self.content = self.content.strip()

    @staticmethod
    def from_id(article_id: int) -> "ArticleContent":
        response = requests.get(
            "https://en.wikinews.org/w/api.php",
            params={
                "action": "query",
                "prop": "extracts",
                "format": "json",
                "explaintext": True,
                "exsectionformat": "plain",
                "exlimit": 1,
                "pageids": article_id,
            },
        ).json()

        return ArticleContent(response["query"]["pages"][str(article_id)]["extract"], optimize=False)
