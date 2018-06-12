#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='htu21',
      version='1.0',
      url='https://github.com/Jeremie-C/python-htu21',
      author='Jeremie-C',
      description='A Python library for accessing HTU21.',
      packages=['htu21'],
      long_description=open('README.md').read(),
      requires=['python (>= 2.7)', 'smbus (>= 0.4.1)'],
      install_requires=['smbus-cffi'],
      classifiers=['Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Embedded Systems'
      ]
)
