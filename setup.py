#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='fusionexport',
    version='1.1.0',
    description='The FusionExport SDK in Python',
    long_description=readme,
    author='FusionCharts',
    author_email='fusionexport@fusioncharts.com',
    url='https://github.com/fusioncharts/fusionexport-python-client',
    license='MIT',
    packages=[
        'fusionexport'
    ],
    package_dir={
        'fusionexport': 'fusionexport'
    },
    install_requires=[
		'requests', 'glob2', 'beautifulsoup4'
    ],
    keywords='fusionexport fusioncharts sdk charts export python dashboards language client cli console',
)