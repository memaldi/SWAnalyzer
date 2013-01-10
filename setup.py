from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='SWAnalyzer',
	version=version,
	description="An statistical library for Semantic Web and Linked Data",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Mikel Emaldi',
	author_email='m.emaldi@deusto.es',
	url='http://www.morelab.deusto.es',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	#namespace_packages=['swanalyzer'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'rdflib==3.2.1',
		'rdfextras==0.2',
		'django',
	],
)
