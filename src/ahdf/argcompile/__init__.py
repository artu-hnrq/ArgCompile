"""Command-line parsing library

This module extends argparse command-line parsing library through:

    - handling post-parsing fields processing

The module contains the following public classes:

    - ArgumentCompiler -- The main entry point for command-line parsing.
        Customize parse_args() method to include Attributes post-processing
        after the end of argparse standard argument parsing.

    - Attribute -- The main addiction from this module.
        An ActionsContainer specialization capable of processing multiple input arguments
        into a unique Namespace attribute.

All other classes in this module are considered implementation details.
"""
from .parse import ArgumentCompiler, Attribute

__version__ = '0.1.0'
__all__ = [
    'ArgumentCompiler',
    'Attribute',
]
