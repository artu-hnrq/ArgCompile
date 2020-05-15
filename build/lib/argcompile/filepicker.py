from argparse import *
from argparse import _StoreAction
from .compiler import ArgumentCompiler
from .attribute import *

import yaml
import os
import re

# --------------------------------------------

class Path(_StoreAction):
	def __init__(self,
                 option_strings,
                 dest,
                 nargs = None,
                 const = None,
                 default = ['./'],
                 choices = None,
                 required = False,
				 help = 'define target path(s)',
				 metavar = None):
		super(Path, self).__init__(
			option_strings = option_strings,
			dest = dest,
			nargs = nargs,
			const = const,
			default = default,
			type = self.type,
			choices = choices,
			required = required,
			help = help,
			metavar = metavar
		)

	def type(self, str):
		if not str:
			return './'
		if not str.endswith('/'):
			str += '/'
		return str

class Output(_StoreAction):
	def __init__(self,
                 option_strings,
                 dest,
                 const = './output',
                 default = SUPPRESS,
				 type = FileType('w'),
                 choices = None,
                 required = False,
				 help = 'define a file to write out script output',
				 metavar = None):
		super(Output, self).__init__(
			option_strings = option_strings,
			dest = dest,
			nargs = '?',
			const = const,
			default = default,
			type = type,
			choices = choices,
			required = required,
			help = help,
			metavar = metavar
		)

class FilePicker(ArgumentCompiler):
	def __init__(self, mode='r', *, filename={}, path={}, extension={}, **kwargs):
		super(FilePicker, self).__init__(**kwargs)
		self.mode = mode

		assert any([isinstance(attr, dict) for attr in [filename, path, extension]]), \
		"one of the attribute filename, path, extension is required"

		if isinstance(path, dict):
			path = self.update(path, {
				'*': ['-p', '--path'],
				'help': "define path to look up files from"
			})
			self.add_argument(*path.pop('*', []), action = Path, **path)

		if isinstance(filename, dict):
			filename = self.update(filename, {
				'*': ['filename']
			})
			self.add_attribute(Target('filename')) #*filename.pop('*', []), **filename))

		if isinstance(extension, dict):
			extension = self.update(extension, {
				'nargs': '*',
				'default': ['.*'],
				'help': 'restrict files extension(s)'
			})
			self.add_attribute(Extension(*extension.pop('*', []), **extension))

	def update(self, reference, default):
		default.update(reference)
		return default

	def __call__(self, namespace):
		pick = re.compile(f"^(%s)\.(%s)$"
			% (
				"|".join(namespace.filename),
				"|".join(namespace.extension)
			)
		)

		if isinstance(namespace.path, str):
			namespace.path = [namespace.path]

		for path in namespace.path:
			try:
				namespace.file = [
					open(f"{path}{file}", self.mode)
					for file
					in os.listdir(path)
					if pick.match(file)
					and os.path.isfile(f"{path}{file}")
				]
			except FileNotFoundError:
				break

		return namespace

class FileComputer(FilePicker):
	def __init__(self, *,
	 			 filename = {},
				 path = {},
				 extension = {},
				 output = {},
				 **kwargs):
		super(FileComputer, self).__init__(
			filename = filename,
			path = path,
			extension = extension,
			**kwargs
		)

		if isinstance(output, dict):
			output = self.update(output, {
				'*': ['-o', '--output'],
			})
			self.add_argument(*output.pop('*', []),
				action = Output,
				**output
			)

	def __call__(self, namespace):
		return namespace

class YmlComputer(FileComputer):
	def __init__(self, *,
	 			 filename = {},
				 path = {},
				 extension = {},
				 output = {},
				 **kwargs):

		if isinstance(extension, dict):
			extension = self.update(extension, {
				'nargs': 1,
				'choices': ('yml',)
			})

		super(YmlComputer, self).__init__(
			filename = filename,
			path = path,
			extension = extension,
			output = output,
			**kwargs
		)

	def __call__(self, namespace):
		namespace.file = [
			yaml.load(file)
			for file in
			namespace.file
		]

		return namespace

class Extension(Attribute):
	def __init__(self,
				 *option_strings,
				 dest = 'extension',
				 nargs = '*',
				 default = None,
				 type = None,
				 choices = None,
				 help = 'define target extension(s)',
				 metavar = 'extension',

				 title = 'Extension',
				 description = 'option(s) to define extension(s)'):
		super(Extension, self).__init__(
			option_strings = option_strings,
			dest = dest,
			nargs = nargs,
			default = default,
			type = type,
			choices = choices,
			help = help,
			metavar = metavar,

			title = title or dest,
			description = description
		)

		if self.restricted:
			if self.required:
				if len(self.choices) < self.min:
					raise ValueError(
						"Number of restricted choices need to be equal or greater than minimum extensions required. \n" \
						f"Restricted choices: {self.choices}, Minimum extensions required: {self.min}"
					)
				elif len(self.choices) == self.min:
					self.default = self.choices
					self.set_defaults(**{f"{self.dest}": self.choices})
					return

			elif len(self.choices) == 1:
				self.add_options(*self.choices, action='store_const')
				return

		self.set_defaults(**{f"{self.dest}": self.default})

		self.arguments.add_argument(*self.option_strings,
			action = 'append_over',
			dest = self.dest,
			nargs = {
				'?': 1,
				'*': '+'
			}.get(self.nargs, self.nargs),
			default = self.default,
			choices = self.choices if self.restricted else None,
			metavar = self.metavar,
			help = self.help
		)

		if self.choices:
			self.add_options(*self.choices, default=SUPPRESS)


	def add_options(self, *options, action='append_const_over', **kwargs):
		for option in options:
			self.arguments.add_argument(f"--{option}",
				action = action,
				dest = self.dest,
				const=f"{option}",
				**kwargs
			)

	def __call__(self, namespace):
		return namespace
