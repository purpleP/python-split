#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = open("README").read()
LICENSE = open("LICENSE").read()

setup(
    name='split',
    version='1.1',
    description='Functions to split or partition sequences.',
    long_description=LONG_DESCRIPTION,
    author='Michael Doronin',
    author_email='warrior2031@mail.ru',
    url='https://github.com/purpleP/python-split.git',
    install_required=('six',),
    license=LICENSE,
    classifiers= ["Development Status :: First Version",
                  "Intended Audience :: Developers",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
                  "Programming Language :: Python :: 2",
                  "Programming Language :: Python :: 3",
                  "Topic :: Software Development :: Libraries" ],
    py_modules = ['split']
)
