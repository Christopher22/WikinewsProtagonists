 # Project: Extracting the protagonists of WikiNews articles

This repository contains the final project for the course "Basics of Data and Natural Language Processing" taught by Dr. Peter Uhrig at the Universiy of Osnabrück. Utilizing different Named-entity recognition systems it extracts the persons named in the articles and exports them in a HTML overview. As such, it may be seen as a example for querying WikiMedia APIs with Python, preprocessing the raw data and applying state-of-the-art frameworks for NLP.

## Usage
1. Install dependencies with `pip install -r requirements.txt`. The system is smart enough to search for them only if needed during runtime. Therefore, if you do not want to use SpaCy, you do not have to install it.
2. Move to the folder and call `python . --help` for getting an overview about the parameters available.
3. (An example usage may look like this: `python . stanford path/to/core_nlp`)

## About The Program
### 1. Article Class
The Article class _articles.py_ serves as an abstract representation of an article on WikiNews, a WikiMedia-based platform, in accordance to the object-oriented programming paradigm.

#### 1.1 Wikinews
Wikinews is a news source wiki by the Wikimedia Foundation. Wikimedia provides an interface for all their products, namely the MediaWiki API, which is used in this project to retrieve the content of articles. Wikinews articles are regular news articles.

#### 1.2 Article Properties
An Article instance contains the unique ID an article has on Wikinews. Furthermore, an Article instance contains the title of a given article. Finally, any Article instance has content. This content is the entire text of a given news article, prepared for further NLP work, i.e. removing irrelevant lines containing date of publishing, removing location strings from the beginnings of articles (e.g. "Peking, China"), and removing unnecessary whitespaces in the beginning of an article.

### 2. Named Entity Recognition
Given the fact that named entity recognition (NER) is an extremely complex problem in its own right and there are a plethora of NER solutions available for free use. We have limited our choice of NER solutions to two widely used parsers. NER requires preprocessing in the form of part-of-speech (POS) tagging, i.e. identifying the syntactic role a word plays in a given sentence and labelling it thus. Since the necessary preprocessing is handled by the parsers used in this project on their own, it will not be discussed further. For further information regarding this, please refer to the documentation of the respective parser.
In order to provide a selection of NER parsers that do the same task, a wrapper was created for each of the two parsers (_spacy.py_ and _stanford.py_, respectively).

#### 2.1 SpaCy
SpaCy is an open-source Python-based parser developed by the software studio Explosion AI (https://explosion.ai/). For general information on how each aspect of spaCy works, please refer to https://spacy.io/api/.
The processing pipeline that finds application in spaCy as depicted below uses a tokenizer to segment a text into individual tokens, i.e. splitting a text string into a list of strings containing each individual sentence and splitting sentence strings into lists of strings containing each indivdual word. Subsequently, each sentence is POS-tagged and labels annotating syntactic dependencies are applied. Finally, named entities are annotated.
![alt text](https://spacy.io/assets/img/pipeline.svg)
Source: https://spacy.io/usage/processing-pipelines

#### 2.2 Stanford CoreNLP
Stanford CoreNLP is a Java-based natural language processing toolkit provided by Stanford University. It provides tools for POS tagging, NER, coreference resolution, sentiment analysis and more. It uses different annotators for different tasks like tokenization and POS tagging [1].

#### 2.3 Differences in Performance
Different approaches to NER yield different results. The most current model used in spaCy, a multi-task convoluted neural networktrained on OntoNotes, a large text corpus containing instances of different text genres (e.g. news, telephone conversations, weblogs). For more information on OntoNotes, see https://catalog.ldc.upenn.edu/LDC2013T19. SpaCy provides evaluation of this model's NER accuracy, claiming the following values[2].
|   |spaCy NER|
|:-:|:-:|
|F-Score|85.88|
|Precision|85.62|
|Recall|86.13|
The NER parser used in Stanford CoreNLP comes with 3 different models to chose from; one with three classes (Location, Person, Organization), one with 4 classes (Location, Person, Organization, Misc), and one with 7 classes (Location, Person, Organization, Money, Percent, Date, Time). The first model is trained on the MUC 6 and MUC 7 training data sets and additional data, the second one is trained on the CoNLL 2003 corpus, and the last one is trained on the MUC 6 and MUC 7 training data sets without additional data. Unfortunately, these models do not come with explicit evaluation regarding their performance.
Fortunately, a comparison of performance on the same NER task between spaCy and CoreNLP can be found on a blog about data science [see 3]. While a blog on data science is not the most credible source and the sample set size is miniscule, its methodology (which is provided in detail) is sound enough to use the resulting values[3] as an indication. Moreover, the lack of peer-reviewed work discussing this matter (instead of the overall performance differences between spaCy and CoreNLP, for which there is plenty of work to reference) forced our hand to resort to this source instead.
|Recognized Entity|F-Score for spaCy|F-Score for Stanford NER|
|:-:|:-:|:-:|
|College Name|100.0%|100.0%|
|Location|98.97%|98.88%|
|Designation|99.39%|100.0%|
|Email addresss|99.71%|97.87%|
|Name|99.81%|100.0%|
|Skills|100.0%|96.36%|
|**Mean**|**99.64%**|**98.85%**|
It is important to keep in mind that these values are not indicative of which parser will perform better in the task we work on in this project. After all, the sample set consists only of 20 resumes and the task was to extract all kinds of named entities, not just persons, as is the case in our project. It is therefore an interesting question if the performance of the two parsers reflects the tendencies indicated in the values depicted above, namely a slightly better performance from Stanford NER compared to spaCy. This evaluation would have exceeded the scope of this project, unfortunately, and therefore remains as a question to be answered at a later time with the help of the tools provided in this project.

# References
1. Manning, Christopher D., Mihai Surdeanu, John Bauer, Jenny Finkel, Steven J. Bethard, and David McClosky. 2014. The Stanford CoreNLP Natural Language Processing Toolkit In Proceedings of the 52nd Annual Meeting of the Association for Computational Linguistics: System Demonstrations, pp. 55-60.
2. https://spacy.io/models/en#en_core_web_lg
3. https://towardsdatascience.com/a-review-of-named-entity-recognition-ner-using-automatic-summarization-of-resumes-5248a75de175