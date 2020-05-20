# ArgCompile

![Python](https://img.shields.io/badge/python-3.6-red)
![GitHub](https://img.shields.io/github/license/artu-hnrq/argcompile)

Command-line parsing library

This module proposes to extend [argparse][1] command-line parsing library objects in order to promote devices to easily process several parsed arguments into complex objects

The package contains three public design classes, some useful implementations of them and other auxiliary classes. The most significant ones described bellow:

### ArgumentCompiler
The main entry point for command-line parsing, extended to process new-design group usage test, attribute formation and `Namespace` compilation. Following its superclass, `ArgumentParser`, it's filled by `Actions` that defines as command line should be parsed. By extension, `add_attribute()` method process the inclusion of complex `ActionsContainer` named accordingly.

- **FileSelector**: A multiple file opener that filters selection based on path, filename(s) and extension(s)
- **FileComputer**: A `FileSelector` specialization that also defines an output target
- **YamlCompuler**: A `FileComputer` based class that restricts _yaml_ and _yml_ file extensions, already loading its content to a dictionary

### Attribute
An `ActionsContainer` specialization to manage parsing of multiple arguments into an unique `Namespace` attribute. Implementations of it can be made in order to define how a `Namespace` attribute should be constructed based on the several target arguments parsed.

- **Target**: Defines a reference collection of the main parsed object
- **Extension**: Designed to accumulate a list of extensions, allowing defining special arguments for desired options
- **Output**: Defines a title and opening-mode of a writing file

### CustomGroup
A group-type class that allows post parsing usage tests to be executed. This design enables the implementation of custom rules in `Action` groups.

- **RequiredGroup**: A simple group that checks the presence of its arguments to require at least one has been provided
- **DependentGroup**: Restricts the use of its arguments based on presence of its dependence list

  [1]: https://docs.python.org/3/library/argparse.html
