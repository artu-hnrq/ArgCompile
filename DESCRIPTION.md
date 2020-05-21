# ArgCompile

[![Python](https://img.shields.io/badge/python-3.6-red)][Python]
[![License](https://img.shields.io/github/license/artu-hnrq/argcompile)][License]
[![PyPI](https://img.shields.io/pypi/v/argcompile?color=blue)][PyPI]

Command-line parsing library

This module proposes to extend [`argparse`][4] command-line parsing library objects in order to promote devices to easily apply post-parsing processing into supplied arguments.

The package contains three public design classes, some useful implementations of them and other auxiliary classes. The most significant ones are described bellow:


#### ArgumentCompiler
The main entry point for command-line parsing, extended to process new-design group usage test, attribute formation and `Namespace` compilation. Following its superclass, `ArgumentParser`, it's filled by `Actions` that defines as command line should be parsed. By extension, `add_attribute()` method process the inclusion of complex `ActionsContainer` named accordingly.

- **FileSelector**: A multiple file opener that filters selection based on path, filename(s) and extension(s)
- **FileComputer**: A `FileSelector` specialization that also defines an output target
- **YamlCompuler**: A `FileComputer` based class that restricts _yaml_ and _yml_ file extensions, already loading its content to a dictionary


#### Attribute
An `ActionsContainer` specialization to manage parsing of multiple arguments into an unique `Namespace` attribute. Implementations of it can be made in order to define how a `Namespace` attribute should be constructed based on the several target arguments parsed.

- **Target**: Defines a reference collection of the main parsed object
- **Extension**: Designed to accumulate a list of extensions, allowing defining special arguments for desired options
- **Output**: Defines title and opening-mode of a writing file


#### CustomGroup
A group-type class that allows post parsing usage tests to be executed. This design enables the implementation of custom rules in `Action` groups.

- **RequiredGroup**: A simple group that checks the presence of its arguments to require at least one has been provided
- **DependentGroup**: Restricts the use of its arguments based on presence of its dependence list


## Example

The following code is a Python program that prints out the file list of a target path
```python
# ls.py
from argcompile import FileSelector

class Ls(FileSelector):
	def __call__(self, namespace):
		for file in namespace.file:
			print(file.name)

compiler = Ls(
	path={
		'*': ['path'],
		'nargs': 1
	}
)
compiler.parse_args()
```

It can be run at the command line and provides useful help messages:
```
$ python3 ls.py -h
usage: ls.py [-h] [--all] [-e ext [ext ...]]
           path [filename [filename ...]]

positional arguments:
  path                  define path to look up files from
  filename              define chosen filenames

optional arguments:
  -h, --help            show this help message and exit
  --all                 select all filenames
  -e ext [ext ...],     restrict files extension(s)
```

When run with the appropriate arguments, it does the job:
```
$ python3 ls.py . --all
./DESCRIPTION.md
./LICENSE
./makefile
./README.md
./setup.py
```

  [Python]: https://www.python.org/downloads/
  [License]: https://github.com/artu-hnrq/argcompile/blob/master/LICENSE
  [PyPI]: https://pypi.org/project/argcompile
  [4]: https://docs.python.org/3/library/argparse.html
