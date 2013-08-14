# -*- coding: utf-8 -*-
import random


def argmax(iterable, function):
    max_value = max([function(x) for x in iterable])
    candidates = [x for x in iterable if function(x) == max_value]
    return random.choice(candidates)