Statistical Classification
==========================

*AIMA Book chapters recommended: 18.3 (Learning Decision Trees), 18.4 (Evaluating and Choosing The Best Hypothesis)*

.. note::

    To use the classification module of SimpleAI you need to have
    `Numpy <http://www.numpy.org/>`_ installed.

To train and use the statistical classification algorithms in this library you
will need to write code that specifies your problem. 
Essentially, this boils down to:

 - Define some **attributes** to be used as the input *feature vector* by the
   algorithms.
 - Define a **target** attribute to be predicted by the algorithms.
 - Give a **dataset** to be used as a *training set* by the algorithms.

This chapter explains how to use the statistical classification facilities of
``simpleai`` with an example that can be found in
``simpleai/samples/machine_learning/language_classification.py``.

Defining your dataset
---------------------

A dataset can be any iterable python object, and the objects being iterated
(the *observations* itself) can be any Python object you want.

For instance, suppose we have a dataset of sentences in some language and
the classification task is to identify the language of each sentence. Then,
it's perfectly valid for our dataset to be a ``list`` of
``(target_language, sentence_text)`` objects.

The example of language classification followed here is fully coded in 
``simpleai/samples/machine_learning/language_classification.py``.

In the code, each observation is represented as a named tuple instead of just a
tuple for clarity:

.. code-block:: python

    class Sentence(object):
        def __init__(self, language, text):
            self.language = language
            self.text = text

Since another goal of this example is to learn a decision tree from a **large**
dataset without putting it in memory all at once, the dataset is read using a
custom iterator that only stores a single observation at a time:

.. code-block:: python

    class OnlineCorpusReader(object):
        def __init__(self):
            self.input_files = [("english", "text.en"),
                                ("spanish", "text.es")]

        def __iter__(self):
            for language, filename in self.input_files:
                for text in open(filename):
                    yield Sentence(language, text.lower())

With that, we can create a dataset of sentences from a file that has
a sentence of each line such as the
`europarl <http://www.statmt.org/europarl/>`_ corpus.



Defining your attributes
------------------------

In order to do an automatic classification you'll have to define what are
the attributes (the *features*) that are going to be used in the learning phase.

The way attributes are represented is slightly different than usual in this
library. Normally,
a classification problem uses a vector of attributes as input, in which each
value in the vector is a value of some attribute.
So if the vector has size `N`, you have `N` attributes.

To do the same thing this library you have to provide N functions, such that
each function takes an observation and returns an attribute value.
So each function is applied to the observation and the resulting N values are
the `classical` feature vector.

Back to the language classification example, let's assume that our
attributes/features are the frequency counts of each letter in the sentence.
Then, we can define the attributes like this:

.. code-block:: python

    class LetterCount(Attribute):
        def __init__(self, letter):
            self.letter = letter
            self.name = "Counts for letter {!r}".format(letter)

        def __call__(self, sentence):
            return sentence.text.count(self.letter)

    # ...
    # somewhere else:
    for letter in "abcdefghijklmnopqrstuvwxyz":
        attribute = LetterCount(letter)
    # ...

Here the attributes inherit from the ``Attribute`` class, which is recommended,
but it's not stricly necessary. The only requirement that an attribute has to
meet is to be a callable object (a function, a method,
a class that defines ``__call__``, etc.).

So, a bare minumum valid attribute that counts the letter ``"a"`` in a
observation could have been like this:

.. code-block:: python

    def attribute_count_a(observation):
        return observation.text.count("a")

And that would have been all that is needed.

If you are wondering "Why, oh, why you did it this way???!!!" it's because not
all datasets exist as a feature vector: there could be text, there could be
images, there could be graphs, etc... so using attribute functions is a way of
explicitly (and neatly too) declaring all preprocessing done to the data
without altering the original data in any way (ie, read-only).


Defining your problem
---------------------

The ``ClassificationProblem`` is where the attributes previously
defined live. In your problem it also has to be defined the ``target``
attribute.
The `target` is the attribute that classifier has to guess, ie, it's a method
that given an example from the dataset returns the correct classification
for it.

Back to the language classification example, the problem definition would be:

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

Here we define an instance of the ``LetterCount`` attribute for each letter
in the english alphabet.

Once this defined, it must be stored in the ``attributes`` list of
your ``ClassificationProblem``.
In this example, the target just returns the language of a ``Sentence``.


Using a classifier
------------------

Once all is defined, you can train one of the implemented classifiers
like Naive Bayes or a Decision Tree.

.. code-block:: python

    input_files = [("english", "europarl-v7.es-en.en"),
                   ("spanish", "europarl-v7.es-en.es")]

    dataset = OnlineCorpusReader()
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
