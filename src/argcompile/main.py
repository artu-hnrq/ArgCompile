import argparse
from argparse import SUPPRESS, ArgumentParser, _AppendAction, _AppendConstAction
from .meta import MetaArgumentCompiler, MetaAttribute
import sys

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

# ===========================
# Argument parsing classes
# ===========================

class _ActionsContainer(argparse._ActionsContainer):
	def __init__(self,
				 title=None,
				 description=None,
				 prefix_chars='-',
				 argument_default=SUPPRESS,
				 conflict_handler='error'):
		super(_ActionsContainer, self).__init__(
			description = description,
            prefix_chars = prefix_chars,
            argument_default = argument_default,
            conflict_handler = conflict_handler
		)
		self.title = title

		self.register('action', 'append_over', _AppendOverDefault)
		self.register('action', 'append_const_over', _AppendConstOverDefault)
		self.register('type', None, lambda str: str)

		self._custom_groups = []

	def _add_group(self, group_class, *args, **kwargs):
		group = group_class(*args, **kwargs)
		self._custom_groups.append(group)
		return group

	def add_required_group(self, *args, **kwargs):
		return self._add_group(_RequiredGroup, *args, **kwargs)

	def add_dependent_group(self, *args, **kwargs):
		return self._add_group(_DependentGroup, *args, **kwargs)

# ==============
# Group classes
# ==============

class TestableGroup(_ActionsContainer):
	"New-design group class to allow custom usage tests"

	def __init__(self, **kwargs):
		super(TestableGroup, self).__init__(**kwargs)
		self.register('usage_test', str(id(self)), self.__call__)

		self._group_actions = []

	def __call__(self, parser, args, namespace):
		pass

	@property
	def _option_strings(self):
		option_strings = []
		for action in self._group_actions:
			option_strings += action.option_strings
		return option_strings


class _RequiredGroup(TestableGroup):
	"Requires at least one of its arguments to be present"

	def __call__(self, parser, args, namespace):
		for option in self._option_strings:
			if option in args:
				break

		else:  # if no actions were used, report the error
			if self._option_strings:
				parser.error(f"one of the arguments {' '.join(self._option_strings)} is required")


class _DependentGroup(TestableGroup):
	"Only allows its arguments if some of dependence list is present"

	def __init__(self, dependence, **kwargs):
		super(_DependentGroup, self).__init__(**kwargs)
		self.dependence = dependence

	def __call__(self, parser, args, namespace):
		for option in self._option_strings:
			if option in args:
				for group in self.dependence:
					if not any(arg in args for arg in group):
						parser.error(
							f"argument {option} requires of one of the arguments {' '.join(group)}"
						)

# ===========================
# Attribute compilation classes
# ===========================

class Attribute(_ActionsContainer, metaclass=MetaAttribute):
	"""ActionsContainer specialization to manage multiple input arguments for an unique Namespace attribute.

	Attribute objects are used by an ArgumentCompiler to represent information
    needed to be parsed through multiple arguments from the command line. The keyword arguments
	define its downward Actions instances."""

	def __init__(self,
				 *option_strings,
				 dest = None,
				 nargs = None,
				 const = None,
				 default = SUPPRESS,
				 type = None,
				 choices = None,
				 help = None,
				 metavar = None,

				 **kwargs):
		super(Attribute, self).__init__(
			**kwargs
		)

		self.option_strings = option_strings
		self.dest = dest
		self.nargs = nargs
		self.const = const
		self.default = default
		self.type = type
		self.choices = choices
		self.help = help
		self.metavar = metavar

	def __call__(self, namespace):
		return namespace

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
	"Attribute designed to select compiler main object references"

	def __init__(self,
				 dest,
				 nargs = '+',
				 default = ['.*'],
				 type = None,
				 help = None,

                 title = "Target",
				 description = "Function's main target object"):
		super(Target, self).__init__(
			dest = dest,
			nargs = nargs,
			default = default,
			type = type,
			help = help or f"define chosen {dest}s",

			title = title or dest,
			description = description
		)

		target = self.add_mutually_exclusive_group(required=self.required) \
				 if not self.limited else \
			 	 self.add_argument_group()

		if not self.limited:
			target.add_argument('--all',
				action = 'store_true',
				help = f"select all {self.dest}s"
			)
		target.add_argument('target',
			nargs = {
				'+': '*'
			}.get(self.nargs, self.nargs),
			default = self.default,
			type = self.type,
			help = self.help,
			metavar = self.dest
		)

	def __call__(self, namespace, all=None, target=None):
		setattr(namespace, self.dest, ['.*'] if all else target)


class ArgumentCompiler(ArgumentParser, metaclass=MetaArgumentCompiler):
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
