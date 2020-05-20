from argparse import ArgumentParser,
from .meta import MetaAttributeCompiler
import sys


# ===========================
# Attribute compilation classes
# ===========================

class ArgumentCompiler(ArgumentParser, metaclass=MetaAttributeCompiler):
	"""ArgumentParser specialization for prosecute parsed command line."""

	def __init__(self, **kwargs):
		super(ArgumentCompiler, self).__init__(**kwargs)
		self.register('compilation', str(id(self)), self.__call__)

	def add_attribute(self, attr):
		self._add_container_actions(attr)

		for group in attr._custom_groups:
			self.register('usage_test', str(id(group)), group.__call__)

		self.set_defaults(**{f"{attr.dest}": attr.get_default(attr.dest)})
		self.register('attribute', str(id(attr)), attr.__call__)

	def parse_args(self, args=None, namespace=None):
		"""Extends argument parsing method to process namespace with
		groups' usage tests, attributes' formation managegment and
		self compilation"""

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
