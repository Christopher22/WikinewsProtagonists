# Project: Extracting the protagonists of WikiNews articles

This repository contains the final project for the course "Basics of Data and Natural Language Processing" taught by Dr. Peter Uhrig at the Universiy of Osnabrück. Utilizing different Named-entity recognition systems it extracts the persons named in the articles and exports them in a HTML overview. As such, it may be seen as a example for querying WikiMedia APIs with Python, preprocessing the raw data and applying state-of-the-art frameworks for NLP.

## Usage
1. Install dependencies with `pip install -r requirements.txt`. The system is smart enough to search for them only if needed during runtime. Therefore, if you do not want to use SpaCy, you do not have to install it.
2. Move to the folder and call `python . --help` for getting an overview about the parameters available.
3. (An example usage may look like this: `python . stanford path/to/core_nlp`)
