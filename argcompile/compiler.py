from argparse import ArgumentParser
from .meta import MetaComposition
import sys

__all__ = [
	'ArgumentCompiler'
]

# ===========================
# Argument compilation classes
# ===========================

class MetaArgumentCompiler(MetaComposition):
	def __run__(self, namespace):
		for compiler in self.__class__.__compound__:
			namespace = compiler.__run__(self, namespace)
		return namespace

class ArgumentCompiler(ArgumentParser, metaclass=MetaArgumentCompiler):
	def __init__(self, **kwargs):
		super(ArgumentCompiler, self).__init__(**kwargs)
		self.register('compilation', str(id(self)), self.__call__)

	def add_attribute(self, attr):
		self._add_container_actions(attr)

		for group in attr._action_groups:
			if getattr(group, 'test', None):
				self.register('usage_test', str(id(group)), group.test)

		self.set_defaults(**{f"{attr.dest}": attr.get_default(attr.dest)})
		self.register('attribute', str(id(attr)), attr.__call__)

	def parse_args(self, args=None, namespace=None):
		namespace  = super(ArgumentCompiler, self).parse_args(args, namespace)

		for test in self._registries.get('usage_test', {}).values():
			test(self, args or sys.argv[1:], namespace)

		for attribute in self._registries.get('attribute', {}).values():
			namespace = attribute(namespace)

		for compilation in self._registries.get('compilation', {}).values():
			namespace = compilation(namespace)

		return namespace

	def __call__(self, namespace):
		return namespace
