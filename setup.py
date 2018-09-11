#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='fusionexport',
    version='1.0.0-rc',
    description='Python language SDK for FusionExport',
    long_description=readme,
    author='FusionCharts',
    author_email='fusionexport@fusioncharts.com',
    url='https://github.com/fusioncharts/fusionexport-python-client',
    license='MIT',
    packages=[
        'fusionexport',
    ],
    install_requires=[
		'ws4py', 'glob2', 'beautifulsoup4', 'boto3'
    ],
    package_dir={
        'fusionexport': 'fusionexport'
    },
    keywords='fusionexport fusioncharts sdk charts export python dashboards language client',
)