#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('LICENSE') as license_file:
    license = license_file.read()

setup(
    name='fusionexport',
    version='1.0.0-beta',
    description='Language SDK for FusionExport which enables exporting of charts & dashboards through Python.',
    long_description=readme,
    author='FusionCharts',
    author_email='support@fusioncharts.com',
    url='https://github.com/fusioncharts/fusionexport-python-client',
    license=license,
    packages=[
        'fusionexport',
    ],
    package_dir={
        'fusionexport': 'fusionexport'
    },
    keywords='fusionexport fusioncharts sdk charts export python dashboards language',
)
