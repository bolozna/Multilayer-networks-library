#! /usr/bin/env python
# vim: set fileencoding=utf-8

from setuptools import setup


setup(
    name="pymnet",
    version="0.1",
    description="Library for analysing multilayer networks",
    url="https://github.com/bolozna/Multilayer-networks-library",
    author="Mikko Kivelä",
    author_email="mikko.kivela@iki.fi",
    packages=["pymnet", "pymnet.tests","pymnet.visuals","pymnet.visuals.drawbackends","pymnet.isomorphisms","pymnet.graphlets","pymnet.sampling"]
)
