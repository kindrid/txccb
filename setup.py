#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='txccb',
    version='0.1.3',
    description='Twisted CCB Integration',
    long_description=readme + '\n\n' + history,
    author='Trenton Broughton',
    author_email='trenton@kindrid.com',
    url='https://github.com/trenton42/txccb',
    packages=[
        'txccb',
    ],
    package_dir={'txccb': 'txccb'},
    include_package_data=True,
    install_requires=[
        'treq',
        'pyopenssl'
    ],
    license="BSD",
    zip_safe=False,
    keywords='txccb',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
