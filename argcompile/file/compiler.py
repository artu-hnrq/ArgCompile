from argparse import *
from ..compiler import ArgumentCompiler
from .action import *
from .attribute import *

import yaml
import os
import re

# ===========================
# Argument compilation classes
# ===========================

class FileSelector(ArgumentCompiler):
	def __init__(self, mode='r', *, filename={}, path={}, extension={}, **kwargs):
		super(FileSelector, self).__init__(**kwargs)
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

		namespace.file = []
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

class FileComputer(FileSelector):
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
			self.add_attribute(Output(*output.pop('*', []), **output))

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
