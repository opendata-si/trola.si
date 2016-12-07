import os

from setuptools import setup, find_packages

setup(name='trolasi',
      version='0.0',
      description='',
      author=u'Domen Kozar',
      author_email='domen@dev.si',
      url='http://www.trola.si/',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'flask',
          'requests',
          'raven',
          'blinker',
          'nose',
          'coverage',
          'mock',
          'setuptools',
          'Sphinx',
          'sphinxcontrib-httpdomain',
          'mimerender',
      ],
      entry_points="""
      """,
      )
