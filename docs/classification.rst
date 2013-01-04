Statistical Classification
==========================

*AIMA Book chapters recommended: 18.3 (Learning Decision Trees), 18.4 (Evaluating and Choosing The Best Hypothesis)*

.. note::

    To use the classification module of SimpleAI you need to have
    `Numpy <http://www.numpy.org/>`_ installed.

To do statistical classification you will need to define the specifics of
your problem, this is a **dataset**, some **attributes** to be tested and a
**problem** definition.

Defining your dataset
---------------------

A very important part of the classification is the dataset used to train a
classifier. You have to define this for your particular problem.

A dataset can be any iterable python object.
For example, if we want to create a dataset for language classification
we could define a `Sentence` object that stores a phrase and it's language,
and then declare our dataset as a list of this `Sentence` objects.

.. code-block:: python

    class Sentence(object):
        def __init__(self, language, text):
            self.language = language
            self.text = text

With that, we can create a dataset of sentences from a file that has
a sentence of each line such as the `europarl <http://www.statmt.org/europarl/>`_ corpus.

.. code-block:: python

    class OnlineCorpusReader(object):
        def __init__(self, input_files):
            self.input_files = input_files

        def __iter__(self):
            for language, filename in self.input_files:
                for text in open(filename):
                    yield Sentence(language, text.lower())

Defining your attributes
------------------------

In order to do an automatic classification you'll have to define what are
the attributes that are going to be tested in the learning phase.

You do this by subclassing from the `Attribute` class and declaring the
`__call__` method. For instance:

.. code-block:: python

    class LetterCount(Attribute):
        def __init__(self, letter):
            self.letter = letter
            self.name = "Counts for letter {!r}".format(letter)

        def __call__(self, sentence):
            return sentence.text.count(self.letter)

This attribute returns the letter count of a word. The `__call__` method
gets a `Sentence` object (an element from our dataset) and returns how
many appearances of a particular letter.

Defining your problem
---------------------

The classifier needs an specification of your problem among the dataset.
The `ClassificationProblem` it's where the attributes previously
defined live. In your problem it's also defined the `target` of an example.
This is a method that given an example from the dataset, it returns the real
classification for it.

For example:

.. code-block:: python

    class LanguageClassificationProblem(ClassificationProblem):
        def __init__(self):
            super(LanguageClassificationProblem, self).__init__()
            for letter in "abcdefghijklmnopqrstuvwxyz":
                attribute = LetterCount(letter)
                self.attributes.append(attribute)

        def target(self, sentence):
            return sentence.language

Here we define an instance of the `LetterCount` attribute for each letter
in the english alphabet.

Once this defined it must be stored in the **attributes** list of
your `ClassificationProblem`.
In this example, the target just returns the language of a `sentence`.

Using a classifier
------------------

With all this defined, you can use one of the implemented classifiers
like Naive Bayes or Decision Tree.

.. code-block:: python

    input_files = [("english", "europarl-v7.es-en.en"),
                   ("spanish", "europarl-v7.es-en.es")]

    dataset = OnlineCorpusReader(input_files)
    problem = LanguageClassificationProblem()
    classifier = NaiveBayes(dataset, problem)

    test = Sentence(None, "is this an english sentence?")
    print classifier.classify(test)
    test = Sentence(None, "es ésta una oración en español?")
    print classifier.classify(test)

Classifier API
===============

.. autoclass:: simpleai.machine_learning.models.Classifier
    :members:
    :undoc-members:


Avaliable classifiers
=====================

.. automodule:: simpleai.machine_learning.classifiers
   :members: DecisionTreeLearner, DecisionTreeLearner_Queued, DecisionTreeLearner_LargeData, NaiveBayes, KNearestNeighbors
