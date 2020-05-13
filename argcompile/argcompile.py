import argparse
from argparse import *
from argparse import _AppendConstAction, _AppendAction, _StoreAction, _ArgumentGroup
from meta import MetaComposition
import sys

# --------------------------------------------

__version__ = '0.0.1'
__all__ = argparse.__all__ + [
    'Attribute',
	'Target',
	'ArgumentCompiler'
]

# ==============
# Action classes
# ==============

class _AppendOverDefault(_AppendAction):
	def __call__(self, parser, namespace, values, option_string=None):
		items = getattr(namespace, self.dest, [])
		if items == self.default or items == parser.get_default(self.dest):
			setattr(namespace, self.dest, values)
		else:
			items.extend(values)
			setattr(namespace, self.dest, items)

class _AppendConstOverDefault(_AppendConstAction):
	def __call__(self, parser, namespace, values, option_string=None):
		items = getattr(namespace, self.dest, [])
		if items == self.default or items == parser.get_default(self.dest):
			setattr(namespace, self.dest, [self.const])
		else:
			super(self.__class__, self).__call__(parser, namespace, values, option_string)

# ==============
# Group classes
# ==============

class _RequiredGroup(_ArgumentGroup):
	def __init__(self, container, **kwargs):
		super(_RequiredGroup, self).__init__(container, **kwargs)
		self.register('usage_test', str(id(self)), self.test)

	@property
	def _option_strings(self):
		option_strings = []
		for action in self._group_actions:
			option_strings += action.option_strings
		return option_strings

	def test(self, parser, args, namespace):
		for option in self._option_strings:
			if option in args:
				break

		else:  # if no actions were used, report the error
			if self._option_strings:
				parser.error(f"one of the arguments {' '.join(self._option_strings)} is required")

# ===========================
# Optional and Positional Parsing
# ===========================

class Attribute(_ArgumentGroup):
	def __init__(self,
				 *option_strings,
				 dest=None,
				 nargs=None,
				 const=None,
				 default=SUPPRESS,
				 type=None,
				 choices=None,
				 help=None,
				 metavar=None,
				 **kwargs):
		super(Attribute, self).__init__(**kwargs)

		self.option_strings = option_strings
		self.dest = dest
		self.nargs = nargs
		self.const = const
		self.default = default
		self.type = type
		self.choices = choices
		self.help = help
		self.metavar = metavar

	# def optional(self):
	# 	if self.option_strings and self.option_strings[0] in self.prefix_chars:

	@property
	def arguments(self):
		self._arguments = getattr(self, '_arguments', self.add_group())
		return self._arguments

	def add_group(self, **kwargs):
		return self.add_mutually_exclusive_group(required=self.required) \
		 	   if self.max == 1 else \
			   self.add_required_group(**kwargs) \
			   if self.required else \
			   self.add_argument_group(**kwargs)

	def add_required_group(self, *args, **kwargs):
		group = _RequiredGroup(self, *args, **kwargs)
		self._action_groups.append(group)
		return group

	@property
	def required(self):
		return self.min > 0

	@property
	def limited(self):
		return self.max < float('inf')

	@property
	def restricted(self):
		return isinstance(self.choices, tuple)

	@property
	def max(self):
		return {
			'?': 1,
			'*': float('inf'),
			'+': float('inf'),
		}.get(self.nargs, self.nargs)

	@property
	def min(self):
		return {
			'?': 0,
			'*': 0,
			'+': 1,
		}.get(self.nargs, self.nargs)

class Target(Attribute):
	def __init__(self,
				 container,
				 dest,
				 nargs = '+',
                 const = ['.*'],
                 default = ['.*'],
				 help = "Defines chosen targets",

				 title = None,
				 description = "Function's main target object"):
		super(Target, self).__init__(
			dest = dest,
			nargs = nargs,
			const = const,
			default = default,

			container = container,
			title = title or dest,
			description = description,
		)

		target = self.add_mutually_exclusive_group(required=self.required) \
				 if not self.limited else \
			 	 self.add_argument_group()

		if not self.limited:
			target.add_argument('--all',
				action = 'store_const',
				dest = self.dest,
				const = self.const,
				help = 'Get all targets'
			)
		target.add_argument(self.dest,
			nargs = {
				'+': '*'
			}.get(self.nargs, self.nargs),
			default = self.default,
			type = self.type,
			choices = self.choices,
			metavar = self.metavar,
			help = self.help
		)

class MetaArgumentCompiler(MetaComposition):
	def __run__(self, namespace):
		for compiler in self.__class__.__compound__:
			namespace = compiler.__run__(self, namespace)
		return namespace

class ArgumentCompiler(ArgumentParser, metaclass=MetaArgumentCompiler):
	def __init__(self, **kwargs):
		super(ArgumentCompiler, self).__init__(**kwargs)

		self.register('action', 'append_over', _AppendOverDefault)
		self.register('action', 'append_const_over', _AppendConstOverDefault)

		self.register('compilation', str(id(self)), self.__call__)

	def parse_args(self, args=None, namespace=None):
		namespace  = super(ArgumentCompiler, self).parse_args(args, namespace)

		for test in self._registries.get('usage_test', {}).values():
			test(self, args or sys.argv[1:], namespace)

		for compilation in self._registries.get('compilation', {}).values():
			namespace = compilation(namespace)

		return namespace

	def __call__(self, namespace):
		return namespace
