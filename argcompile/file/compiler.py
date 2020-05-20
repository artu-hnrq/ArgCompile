from ..main import *
from .attribute import *

import yaml
import os
import re

# ===========================
# Attribute compilation classes
# ===========================

class FileSelector(ArgumentCompiler):
	__config__ = {
		'path': {
			'*': ['-p', '--path'],
			'help': "define path to look up files from"
		},
		'filename': {
			'*': ['filename']
		},
		'extension': {
			'nargs': '*',
			'default': ['.*'],
			'help': 'restrict files extension(s)'
		}
	}
	__action__ = {
		'path': Path
	}

	__attr__ = {
		'filename': Target,
		'extension': Extension
	}

	def __init__(self, mode='r', **kwargs):
		super(FileSelector, self).__init__(**kwargs)
		self.mode = mode

	def __call__(self, namespace):
		title = re.compile(f"^(%s)\.(%s)$"
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
					if title.match(file)
					and os.path.isfile(f"{path}{file}")
				]
			except FileNotFoundError:
				break

		return namespace

class FileComputer(FileSelector):
	__attr__ = {
		'output': Output
	}

	def __init__(self, **kwargs):
		super(FileComputer, self).__init__(**kwargs)

	def __call__(self, namespace):
		return namespace

class YamlComputer(FileComputer):
	__config__ = {
		'extension': {
			'nargs': 2,
			'choices': ('yml', 'yaml')
		}
	}

	def __init__(self, **kwargs):
		super(YamlComputer, self).__init__(**kwargs)

	def __call__(self, namespace):
		namespace.file = [
			yaml.load(file)
			for file in
			namespace.file
		]

		return namespace
