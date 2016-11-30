# -*- coding: utf-8 -*-

"""
Example for language classification from text using the es-en europarl
corpus[0].
This script should be able to tell if some text is english or spanish based
solely in counting the letters that appear.

It's *highly* recomended to make shorter versions of the corpus to experiment,
like this:
    head -n 100000 europarl-v7.es-en.en > short.en
    head -n 100000 europarl-v7.es-en.es > short.es

and then change the input files variable to point them... it'll be faster.


[0] Download link: http://www.statmt.org/europarl/v7/es-en.tgz
    See http://www.statmt.org/europarl/ for more information.
"""

from __future__ import print_function

# CHANGE INPUT FILES HERE:
input_files = [("english", "europarl-v7.es-en.en"),
               ("spanish", "europarl-v7.es-en.es")]


import random
from simpleai.machine_learning import DecisionTreeLearner_LargeData, \
                                      ClassificationProblem, Attribute, \
                                      precision, NaiveBayes
from simpleai.machine_learning.classifiers import tree_to_str


class Sentence(object):
    def __init__(self, language, text):
        self.language = language
        self.text = text


class LetterCount(Attribute):
    def __init__(self, letter):
        self.letter = letter
        self.name = "Counts for letter {!r}".format(letter)

    def __call__(self, sentence):
        return sentence.text.count(self.letter)


class LanguageClassificationProblem(ClassificationProblem):

    def __init__(self):
        super(LanguageClassificationProblem, self).__init__()
        for letter in "abcdefghijklmnopqrstuvwxyz":
            attribute = LetterCount(letter)
            self.attributes.append(attribute)

    def target(self, sentence):
        return sentence.language


class OnlineCorpusReader(object):
    def __init__(self, input_files, accept_criteria):
        self.input_files = input_files
        self.accept_criteria = accept_criteria

    def __iter__(self):
        print("Iterating corpus from the start...")
        i = 0
        for language, filename in self.input_files:
            for text in open(filename):
                if self.accept_criteria(i):
                    yield Sentence(language, text.lower())
                i += 1
                if i % 10000 == 0:
                    print("\tReaded {} examples".format(i))


print("Counting examples")
# line count
N = 0
for _, filename in input_files:
    for _ in open(filename):
        N += 1
print("Corpus has {} examples".format(N))

# Choose test set, either 10% or 10000 examples, whatever is less
M = min(N / 10, 10000)
testindexes = set(random.sample(range(N), M))
print("Keeping {} examples for testing".format(M))

problem = LanguageClassificationProblem()
train = OnlineCorpusReader(input_files, lambda i: i not in testindexes)
test = OnlineCorpusReader(input_files, lambda i: i in testindexes)


print("Training Naive Bayes...")
classifier = NaiveBayes(train, problem)
print("Testing...")
p = precision(classifier, test)
print("Precision Naive Bayes = {}".format(p))


print("Training Decision Tree (large data)...")
classifier = DecisionTreeLearner_LargeData(train, problem, minsample=500)
print("Final tree:")
print(tree_to_str(classifier.root))
print("Testing...")
p = precision(classifier, test)
print("Precision Decision Tree = {}".format(p))
