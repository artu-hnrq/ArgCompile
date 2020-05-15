from argparse import SUPPRESS, _ActionsContainer, _AppendAction, _AppendConstAction, _ArgumentGroup
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

class _DependentGroup(_ArgumentGroup):
	def __init__(self, container, dependence, **kwargs):
		super(_DependentGroup, self).__init__(container, **kwargs)
		self.register('usage_test', str(id(self)), self.test)

		self.dependence = dependence

	@property
	def _option_strings(self):
		option_strings = []
		for action in self._group_actions:
			option_strings += action.option_strings
		return option_strings

	def test(self, parser, args, namespace):
		for option in self._option_strings:
			if option in args:
				for group in self.dependence:
					if not any(arg in args for arg in group):
						parser.error(
							f"argument {option} " \
							f"require one of the arguments {' '.join(group)}"
						)

# ===========================
# Attribute parsing classes
# ===========================

class Attribute(_ActionsContainer):
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

				 title = None,
				 description = None,
				 **kwargs):
		super(Attribute, self).__init__(
			description = description,
            prefix_chars = '-',
            argument_default = SUPPRESS,
            conflict_handler = 'error'
		)

		self.register('action', 'append_over', _AppendOverDefault)
		self.register('action', 'append_const_over', _AppendConstOverDefault)
		self.register('type', None, lambda str: str)
		self.title = title

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
	def arguments(self):
		self._arguments = getattr(self, '_arguments', self.add_group())
		return self._arguments

	def add_group(self, **kwargs):
		return self.add_mutually_exclusive_group(required=self.required) \
		 	   if self.max == 1 else \
			   self.add_required_group(**kwargs) \
			   if self.required else \
			   self.add_argument_group(**kwargs)

	def _add_group(self, group_class, *args, **kwargs):
		group = group_class(*args, **kwargs)
		self._action_groups.append(group)
		return group

	def add_required_group(self, *args, **kwargs):
		return self._add_group(_RequiredGroup, *args, **kwargs)

	def add_dependent_group(self, *args, **kwargs):
		return self._add_group(_DependentGroup, *args, **kwargs)

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
				 dest,
				 nargs = '+',
				 default = ['.*'],
				 type = None,
				 help = "define chosen targets",

                 title = "Target",
				 description = "Function's main target object"):
		super(Target, self).__init__(
			dest = dest,
			nargs = nargs,
			default = default,
			type = type,
			help = help,

			title = title or dest,
			description = description
		)

		target = self.add_mutually_exclusive_group(required=self.required) \
				 if not self.limited else \
			 	 self.add_argument_group()

		if not self.limited:
			target.add_argument('--all',
				action = 'store_true',
				help = 'get all targets'
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

	def popattr(self, namespace):
		attributes = dict([
			(action.dest, getattr(namespace, action.dest, None))
			for action in
			self._actions
		])
		for attr, value in attributes.items():
			if value:
				delattr(namespace, attr)

		return attributes

	def __call__(self, namespace):
		def process(*, all = None, target = None):
			setattr(namespace, self.dest, ['.*'] if all else target)

		process(**self.popattr(namespace))
		return namespace
