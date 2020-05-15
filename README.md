# ArgCompile

Command-line parsing library

This module is an [argparse][1]-inspired command-line parsing library that promotes
devices to process parsed arguments in complex objects

The module contains the following public classes:

- ArgumentCompiler -- The main entry point for command-line parsing
	and attribute compilation.

- Attribute -- An \_ActionContainer to manage multiple options to a same
	Namespace attribute
- Target -- An Attribute implementation that represent the parsing main object

- FileSelector -- An ArgumentCompiler to easy process opening multiple files on desired mode
- FileComputer --
- YmlCompuler --

  [1]: https://docs.python.org/3/library/argparse.html
