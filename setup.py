#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('README.md') as readme:
    __doc__ = readme.read()

from distutils.core import setup

setup(
    name='simple-ai',
    version='0.1',
    description=u'An implementation of AI algorithms based on aima-python',
    long_description=__doc__,
    author = u'Juan Pedro Fisanotti',
    author_email = 'fisadev@gmail.com',
    url='',
    packages=['simepl_ai'],
    classifiers = [
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
