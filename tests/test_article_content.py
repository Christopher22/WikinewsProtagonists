import unittest

from data import ArticleContent


class TestArticleContent(unittest.TestCase):
    def test_optimize(self):
        PLACEHOLDER = "This is an example."
        test_object = ArticleContent(
            "Random date\n{}\nFile:Iran strait of hormuz 2004.jpg\nSource:\nWikiNews".format(
                PLACEHOLDER
            ),
            optimize=False,
        )
        test_object.optimize()

        self.assertEqual(PLACEHOLDER, str(test_object))
