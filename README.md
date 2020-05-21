# ArgCompile

[![Python](https://img.shields.io/badge/python-3.6-red)][Python]
[![License](https://img.shields.io/github/license/artu-hnrq/argcompile)][License]
[![PyPI](https://img.shields.io/pypi/v/argcompile?color=blue)][PyPI]

[`argcompile`][PyPI] is a Python package made to improve native [`argparse`][1] command-line parsing library by include some design classes that allows defining post-processing of supplied arguments. Check [package description](DESCRIPTION.md) for more information and [examples](DESCRIPTION.md#Example).


## Getting started
Make sure you have at least [Python 3.6 installed][2]:
```
$ python3 --version
python 3.6.0
```

Since, from this version, [pip][3] already comes together with Python, you'll be able to download package [latest release][PyPI] available in PyPI:
```
pip3 install argcompile
```

## Acknowledgements

This tool was developed after reach an [`argparse` limitation][4] that is actually an old-dated [reported issue][5] and has already an [huge solution proposed][6] in which `argcompile` was based on.

@hpaulj's proposal modifies the standard library making it more flexible to be extended, considering several usage situations and code improvements. `argcompile` otherwise implements a flavor of this mechanisms without much concern and with a simpler and limited approach.

  [Python]: https://www.python.org/downloads/
  [License]: https://github.com/artu-hnrq/argcompile/blob/master/LICENSE
  [PyPI]: https://pypi.org/project/argcompile
  [1]: https://docs.python.org/3/library/argparse.html
  [2]: https://realpython.com/installing-python/
  [3]: https://pip.pypa.io/en/stable/installing/
  [4]: https://stackoverflow.com/q/61624056/2989289
  [5]: https://bugs.python.org/issue11588
  [6]: https://github.com/hpaulj/argparse_issues
