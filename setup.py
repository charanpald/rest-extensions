#!/usr/bin/env python

from setuptools import setup

setup(name='rest_extensions',
      version='0.1',
      description='A set of filters/serializers/utilities for Django REST framework and MongoEngine',
      author='Charanpal Dhanjal',
      author_email='charanpal@gmail.com',
      url='https://github.com/charanpald/rest_extensions',
      install_requires=['django>=1.8.0', 'mongoengine>=0.10.0',
                        'djangorestframework>=3.3.0', 'geojson>=1.3.0'],
      platforms=["OS Independent"],
     )
