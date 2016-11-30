#!/usr/bin/env python
# coding: utf-8

"""
Opinion Mining example.
More about opinion mining here: http://en.wikipedia.org/wiki/Sentiment_analysis

Dataset extracted from: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
precisely http://www.cs.uic.edu/~liub/FBS/pros-cons.rar
It should be placed in a folder called corpus in the same location of this file.
"""

from __future__ import print_function

import os
import re
import codecs
import random

from simpleai.machine_learning import precision
from simpleai.machine_learning import Attribute
from simpleai.machine_learning import NaiveBayes
from simpleai.machine_learning import ClassificationProblem

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PRO_CORPUS_PATH = os.path.join(BASE_PATH, "corpus", "IntegratedPros.txt")
CON_CORPUS_PATH = os.path.join(BASE_PATH, "corpus", "IntegratedCons.txt")
STOPWORDS_PATH = os.path.join(BASE_PATH, "corpus", "stopwordsEN.txt")
STOPWORDS = {s.strip() for s in codecs.open(STOPWORDS_PATH, encoding="utf-8")}


class Opinion(object):
    def __init__(self, text, category=None):
        self.text = text
        self.category = category


class WordIsPresent(Attribute):
    def __init__(self, word):
        super(WordIsPresent, self).__init__(name="{} is present".format(word))
        self.word = word

    def __call__(self, opinion):
        words = opinion.text.split()
        return self.word in words


class ProConsCorpus(object):
    def __init__(self, input_files, accept_criteria):
        self.input_files = input_files
        self.accept_criteria = accept_criteria

    def _clean_line(self, line):
        line = re.sub("\<[\/]*Pros\>", "", line)
        line = re.sub("\<[\/]*Cons\>", "", line)
        line = re.sub("[;\":!\.,()]", "", line)
        line = line.strip()
        line = line.lower()
        return line

    def __iter__(self):
        i = 0
        for category, filename in list(self.input_files.items()):
            for line in open(filename):
                line = self._clean_line(line)
                if self.accept_criteria(i):
                    yield Opinion(line, category)
                i += 1
                if i % 1000 == 0:
                    print("\tReaded {} examples".format(i))


class OpinionProblem(ClassificationProblem):
    def __init__(self, corpus):
        super(OpinionProblem, self).__init__()

        words = set()
        for opinion in corpus:
            for word in opinion.text.split():
                if word not in STOPWORDS:
                    words.add(word)

        for word in words:
            self.attributes.append(WordIsPresent(word))

    def target(self, opinion):
        return opinion.category


def main():
    input_files = {
        "pro": PRO_CORPUS_PATH,
        "con": CON_CORPUS_PATH,
    }

    # line count
    N = 0
    for _, filename in list(input_files.items()):
        for _ in open(filename):
            N += 1
    print("Corpus has {} examples".format(N))

    # Choose test set, either 10% or 10000 examples, whatever is less
    M = min(N / 10, 1000)
    testindexes = set(random.sample(range(N), M))

    corpus = ProConsCorpus(input_files, lambda i: i not in testindexes)
    test = ProConsCorpus(input_files, lambda i: i in testindexes)
    print("Corpuses created")

    problem = OpinionProblem(corpus)
    classifier = NaiveBayes(corpus, problem)
    print("Classifier created")

    p = precision(classifier, test)
    print("Precision = {}".format(p))

if __name__ == "__main__":
    main()
