from argparse import _AppendAction, _AppendConstAction, _ArgumentGroup
import sys

# ==============
# Action classes
# ==============

class AppendOverDefault(_AppendAction):
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
