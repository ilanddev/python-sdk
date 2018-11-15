#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

with open('requirements_dev.txt') as requirements_dev_file:
    test_requirements = requirements_dev_file.read().splitlines()

setup(
    name='iland-sdk',
    version='1.0.1',
    description="iland cloud Python SDK",
    long_description=readme + '\n\n' + history,
    author="iland Internet Solutions, Corp",
    author_email='devops@iland.com',
    url='https://github.com/ilanddev/python-sdk',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='iland cloud sdk',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
