from pathlib import Path
from typing import Sequence
import logging
import pickle
import argparse

from data import Article


def get_articles(
    cache: str = "articles.pkl", num_threads: int = 8
) -> Sequence[Article]:
    """
    Return a collection of articles by loading them from WikiNews or from the provided cache.
    :param cache: The file for storing and loading the WikiNews articles.
    :param num_threads: The number of used threads.
    :return: The loaded sequence of articles.
    """

    if not Path(cache).exists():
        logging.info("Extracting available articles from WikiNews...")
        articles = Article.from_wikinews(num_threads)
        with open(cache, "wb") as output:
            pickle.dump(articles, output, pickle.HIGHEST_PROTOCOL)
    else:
        with open(cache, "rb") as input:
            articles = pickle.load(input)

    # Optimize the text on runtime. Therefore, these routine may be modified without need to reload the cache.
    for article in articles:
        article.content.optimize()

    return articles


if __name__ == "__main__":
    # Configure the visualization of the logging
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s]\t%(message)s")

    # Prepare the argument parser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-num_worker",
        type=int,
        default=8,
        help="The number of worker used to process the data.",
    )
    parser.add_argument(
        "-cache",
        type=str,
        default="articles.pkl",
        help="The cache file used to save the articles locally.",
    )
    parser.add_argument(
        "-output", type=str, default="persons.html", help="The HTML output file."
    )

    # Add the subparsers for choosing the used extractor with possible different arguments
    subparser = parser.add_subparsers(
        dest="parser", help="The Named-entity recognition used.", required=True
    )
    spacy_parser = subparser.add_parser("spacy")
    spacy_parser.set_defaults(ner_parser="spacy")

    stanford_parser = subparser.add_parser("stanford")
    stanford_parser.add_argument(
        "stanford_folder",
        default=str,
        help="Directory with the Stanford CoreNLP parser.",
    )
    stanford_parser.set_defaults(ner_parser="stanford")

    # Parse the arguments
    args = vars(parser.parse_args())

    # Load the articles from WikiNews or cache
    articles = get_articles(args["cache"], args["num_worker"])

    # Select the used parser. By importing them on demand, only the dependencies required are needed on the system.
    if args["ner_parser"] == "spacy":
        from named_entity_recognition.spacy import Spacy

        extractor = Spacy(args["num_worker"])
    elif args["ner_parser"] == "stanford":
        from named_entity_recognition.stanford import Stanford

        extractor = Stanford(args["stanford_folder"])
    else:
        raise NotImplementedError()

    # Calculate and export the extracted names to HTML.
    extractor.export(args["output"], articles)
