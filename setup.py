#!/usr/bin/env python3
"""Seriously - a Python-based golfing language"""

from setuptools import setup, find_packages

need_stats = False

try:
    import statistics
except:
    need_stats = True

setup(
    name='seriously',

    version='2.1.3',

    description='A Python-based golfing language',
    long_description='Seriously is a Python-based golfing language. See the GitHub page for more details.',

    url='https://github.com/Mego/Seriously',

    author='Mego',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    
    install_requires = ['pycryptodome'] + (['stats'] if need_stats else []),
    
    packages = ['seriously', 'lib'],

    keywords='codegolf recreational',
    entry_points={
        'console_scripts': [
            'seriously=seriously:main',
        ],
    },
)