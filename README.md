# ArgCompile

Command-line parsing library

This module is an [argparse][1]-inspired command-line parsing library that promotes
devices to process parsed arguments in complex objects

The module contains the following public classes:

    - ArgumentCompiler -- The main entry point for command-line parsing
		and atribute compilation.
	- Attribute -- An \_ArgumentGroup to manage multiple options to a same
		Namespace attribute
	- Target -- An Attribute implementation that represent the parsing main object

  [1]: https://docs.python.org/3/library/argparse.html
