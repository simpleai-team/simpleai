#!/usr/bin/env python
# coding: utf-8

"""
Classifiers implemented:
 * Decision tree:      See http://en.wikipedia.org/wiki/Decision_tree_learning
 * Naive Bayes:        See http://en.wikipedia.org/wiki/Naive_Bayes_classifier
 * K-Nearest Neighbor: See http://en.wikipedia.org/wiki/K-nearest_neighbor
"""

import numpy
from collections import defaultdict
from simpleai.machine_learning.models import Classifier
from simpleai.machine_learning.metrics import Counter, OnlineInformationGain, \
                                              OnlineLogProbability

try:
    import cPickle as pickle
except ImportError:
    import pickle


class DecisionTreeLearner(Classifier):
    """
    This implementation features an algorithm that *strictly* follows the
    pseudocode given in AIMA.

    It's obviously ineficient in too many ways (perhaps incomplete too), but
    it's intended to be used pedagogically.

    See the other implementations in this same file for some discusión and
    issues solved.

    This algorithm is equivalent to ID3.
    """

    def __init__(self, dataset, problem):
        self.dataset = dataset
        self.problem = problem
        self.root = self.learn(dataset, set(self.attributes), dataset)

    def learn(self, examples, attributes, parent_examples):
        """
        A decision tree learner that *strictly* follows the pseudocode given in
        AIMA. In 3rd edition, see Figure 18.5, page 702.
        """
        if not examples:
            return self.plurality_value(parent_examples)
        elif len(set(map(self.target, examples))) == 1:
            return self.plurality_value(examples)
        elif not attributes:
            return self.plurality_value(examples)
        A = max(attributes, key=lambda a: self.importance(a, examples))
        tree = DecisionTreeNode(attribute=A)
        for value in set(map(A, examples)):
            exs = [e for e in examples if A(e) == value]
            subtree = self.learn(exs, attributes - set([A]), examples)
            tree.add_branch(value, subtree)
        return tree

    def plurality_value(self, examples):
        if not examples:
            raise ValueError("Dataset is empty")
        counter = Counter(self.target)
        for example in examples:
            counter.add(example)
        tree = DecisionTreeNode()
        # Note that tie is *not* solved randomly here
        tree.set_results_from_counts(counter)
        return tree

    def importance(self, attribute, examples):
        """
        AIMA implies that importance should be information gain.
        Since AIMA only defines it for binary features this implementation
        was based on the wikipedia article:
        http://en.wikipedia.org/wiki/Information_gain_in_decision_trees
        """
        gain_counter = OnlineInformationGain(attribute, self.target)
        for example in examples:
            gain_counter.add(example)
        return gain_counter.get_gain()

    def classify(self, example):
        node = walk_to_leaf(self.root, example)
        return node.result


class NaiveBayes(Classifier):
    """
    Implements a classifier that uses the Bayes' theorem.
    """

    def learn(self):
        # Frequency count of target classes
        self.C = OnlineLogProbability()
        # Frequency count of P(Fi|C):
        self.Fi = defaultdict(lambda:  # For each class,
                      defaultdict(lambda:  # For each attribute,
                          OnlineLogProbability()))  # For each value, count it

        for example in self.dataset:
            class_ = self.target(example)
            self.C.add(class_)
            for attribute in self.attributes:
                value = attribute(example)
                self.Fi[class_][attribute].add(value)
        if not self.C:
            raise ValueError("Dataset is empty")

        # Cripple defaultdict to a regular dict, so now it can rasie KeyError
        self.Fi.default_factory = None
        for d in self.Fi.itervalues():
            d.default_factory = None

    def classify(self, example):
        values = [(attribute, attribute(example))
                  for attribute in self.attributes]
        hypotheses = []
        for class_ in self.C:
            try:
                ps = [self.Fi[class_][attr][val] for attr, val in values]
            except KeyError:
                continue  # A value not seen in training, so Prob(class) == 0
            ps.append(self.C[class_])
            hypotheses.append((sum(ps), class_))

        if hypotheses:
            logprob, best = max(hypotheses)
            Z = numpy.logaddexp.reduce([p for p, class_ in hypotheses])
            logprob = logprob - Z
        else:  # Something not at all seen in training, return best a priori
            logprob, best = max((p, class_) for class_, p
                                            in self.C.iteritems())
        p = numpy.exp(logprob)
        assert 0.0 <= p and p <= 1.0
        return best, p


class KNearestNeighbors(Classifier):
    """
    Classifies objects based on closest training example.
    Uses the k-nearest examples from the training and
    gets the most common classification among these.

    To use this classifier the problem must define a `distance`
    method to messure the distance between two examples.
    """

    def __init__(self, dataset, problem, k=1):
        self.k = k
        super(KNearestNeighbors, self).__init__(dataset, problem)

    def learn(self):
        try:
            next(iter(self.dataset))
        except StopIteration:
            raise ValueError("Empty dataset")
        try:
            example = next(iter(self.dataset))
            self.problem.distance(example, example)
        except NotImplementedError:
            message = "Classification problem not suitable for KNN. " \
                      "A problem with a distance defined is needed."
            raise ValueError(message)

    def classify(self, example):
        distances = [(self.problem.distance(e, example), e)
                     for e in self.dataset]
        best = sorted(distances)[:self.k]

        counter = Counter(self.problem.target)
        for _, example in best:
            counter.add(example)

        items = [(x[1], x[0]) for x in counter.iteritems()]
        items.sort(reverse=True)
        return (items[0][1], items[0][0] / counter.total)

    def save(self, filepath):
        """
        Saves the classifier to `filepath`.
        Because this classifier needs to save the dataset, it must
        be something that can be pickled and not something like an
        iterator.
        """

        if not filepath or not isinstance(filepath, basestring):
            raise ValueError("Invalid filepath")

        with open(filepath, "w") as filehandler:
            pickle.dump(self, filehandler)


def path_to_leaf(node, example):
    while node is not None:
        yield node
        node = node.take_branch(example)


def walk_to_leaf(node, example):
    for node in path_to_leaf(node, example):
        pass
    return node


def iter_tree(root):
    q = [(None, root, 0)]
    while q:
        value, node, depth = q.pop()
        yield value, node, depth
        for value, child in node.branches.iteritems():
            q.append((value, child, depth + 1))


def tree_to_str(root):
    """
    Returns a string representation of a decision tree with
    root node `root`.
    """

    xs = []
    for value, node, depth in iter_tree(root):
        template = "{indent}"
        if node is not root:
            template += "case={value}\t"
        if node.attribute is None:
            template += "result={result} -- P={prob:.2}"
        else:
            template += "split by {split}:\t" +\
                        "(partial result={result} -- P={prob:.2})"
        line = template.format(indent="    " * depth,
                               value=value,
                               result=node.result[0],
                               prob=node.result[1],
                               split=str(node.attribute))
        xs.append(line)
    return "\n".join(xs)


class DecisionTreeNode(object):
    """
    A node of a decision tree.
    """

    def __init__(self, attribute=None):
        self.branches = {}
        self.attribute = attribute
        self.parent = None
        self.result = None

    def take_branch(self, example):
        """
        Returns a `DecisionTreeNode` instance that can better classify
        `example` based on the selectors value.
        If there are no more branches (ie, this node is a leaf) or the
        attribute gives a value for an unexistent branch then this method
        returns None.
        """
        if self.attribute is None:
            return None
        value = self.attribute(example)
        return self.branches.get(value, None)

    def set_results_from_counts(self, counts):
        self.counts = counts
        total = sum(counts.itervalues())
        majority = max(counts, key=counts.get)  # Max frequency
        self.result = (majority, counts[majority] / float(total))

    def add_branch(self, value, branch=None):
        assert not value in self.branches
        if branch is None:
            branch = self.__class__()
        self.branches[value] = branch
        branch.parent = self
        return branch


class DecisionTreeLearner_Queued(Classifier):
    """
    This implementations has a few improvements over the one based on the book:
        -It uses a queue instead of recursion, so the python stack limit is
         never reached.
        -In case an attribute has a value not seen in training the intermediate
         nodes can give a "best so far" classification.
        -Abusive re-iteration of the train examples is avoided by calculating
         at the same time all information gains of a single node split.

         This algorithm is equivalent to ID3.
    """

    def learn(self):
        if not self.attributes:
            self.root = self._single_node_tree()
            return
        self.root = DecisionTreeNode()
        q = [(self.root, self.dataset)]
        while q:
            node, examples = q.pop()
            A = self._max_gain_split(examples)
            counts = A.get_target_class_counts()
            branches = A.get_branches()

            # Base case exception
            if node is self.root:
                node.set_results_from_counts(counts)

            if len(counts) == 1:
                continue  # Avoid splitting when there's a single target class
            if len(branches) == 1:
                continue  # Avoid splitting when there's a single child branch

            # Finally, go ahead and split
            node.attribute = A.attribute
            for value, counts in A.get_branches():
                branch = node.add_branch(value)
                branch.set_results_from_counts(counts)
                bdataset = [e for e in examples if node.attribute(e) == value]
                q.append((branch, bdataset))

    def _max_gain_split(self, examples):
        """
        Returns an OnlineInformationGain of the attribute with
        max gain based on `examples`.
        """
        gains = self._new_set_of_gain_counters()
        for example in examples:
            for gain in gains:
                gain.add(example)
        winner = max(gains, key=lambda gain: gain.get_gain())
        if not winner.get_target_class_counts():
            raise ValueError("Dataset is empty")
        return winner

    def _new_set_of_gain_counters(self):
        """
        Creates a new set of OnlineInformationGain objects
        for each attribute.
        """
        return [OnlineInformationGain(attribute, self.target)
                for attribute in self.attributes]

    def _single_node_tree(self):
        c = Counter(self.target)
        for example in self.dataset:
            c.add(example)
        node = DecisionTreeNode()
        node.set_results_from_counts(c)
        return node

    def classify(self, example):
        node = walk_to_leaf(self.root, example)
        return node.result


class DecisionTreeLearner_LargeData(DecisionTreeLearner_Queued):
    """
    This implementations is specifically designed to handle large dataset that
    don't fit into memory and has more improvements over the queued one:

        -Data is processed one-at-a-time, so the training data doesn't need to
         fit in memory.
        -The amount of times the train data is read is aproximately log(N) full
         iterations (from first to last) for a dataset with N examples.
         This is because the gain from all splits from all leaf nodes are
         estimated simultaneuosly, so every time the train data is read
         completely a full new level of the tree (ie, nodes with equal depth,
         leaves) is expanded simultaneously.

         This algorithm is equivalent to ID3.

    Is very important to note that in order to have a small memory footprint
    the `minsample` argument has to be set to a reasonable size, otherwhise
    there will be one tree leaf for every example in the training set and this
    totally defeats the pourpose of having a large data version of the
    algorithm.
    """
    def __init__(self, dataset, problem, minsample=1):
        self.minsample = minsample
        super(DecisionTreeLearner_Queued, self).__init__(dataset, problem)

    def learn(self):
        if not self.attributes:
            self.root = self._single_node_tree()
            return
        self.root = DecisionTreeNode()
        leaves = {self.root: self._new_set_of_gain_counters()}
        while leaves:
            leaf = None
            for example in self.dataset:
                leaf = walk_to_leaf(self.root, example)
                if leaf not in leaves:
                    continue  # Don't split leaves that where ignored
                for gain_counter in leaves[leaf]:
                    gain_counter.add(example)
            if leaf is None:
                raise ValueError("Dataset is empty")

            old_leaves = leaves
            leaves = {}
            for leaf, gains in old_leaves.iteritems():
                winner = max(gains, key=lambda gain: gain.get_gain())
                counts = winner.get_target_class_counts()
                branches = [(v, c) for v, c in winner.get_branches()
                            if c.total > self.minsample]

                # Base case exception
                if leaf is self.root:
                    leaf.set_results_from_counts(counts)

                if len(counts) == 1:
                    continue  # No split when there's a single target class
                if len(branches) <= 1:
                    continue  # No split when there's a single child branch
                              # Or all branches are too small

                # Finally, go ahead and split
                leaf.attribute = winner.attribute
                for value, counts in branches:
                    branch = leaf.add_branch(value)
                    branch.set_results_from_counts(counts)
                    leaves[branch] = self._new_set_of_gain_counters()
