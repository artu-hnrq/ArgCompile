# from argparse import *
from argparse import _StoreAction

# ==============
# Action classes
# ==============

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
