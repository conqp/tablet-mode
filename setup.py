#! /usr/bin/env python

from setuptools import setup

setup(
    name='tabletmode',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    python_requires='>=3.8',
    packages=['tabletmode'],
    entry_points={
        'console_scripts': [
            'setsysmode = tabletmode.cli:main',
            'sysmoded = tabletmode.daemon:main'
        ],
    },
    url='https://github.com/conqp/tablet-mode',
    license='GPLv3',
    description='Tablet mode switch for GNOME 3.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='tablet mode tent convertible switch'
)
