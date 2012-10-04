from setuptools import setup, find_packages
import sys, os

version = '9999'

setup(name='evilshortgen',
      version=version,
      description="Evil tornado.gen shortcuts",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Vladimir Iakovlev',
      author_email='nvbn.rm@gmail.com',
      url='https://github.com/nvbn/evilshortgen/',
      license='Apache',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'tornado', 'byteplay',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
