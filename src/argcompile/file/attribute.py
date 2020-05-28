from argparse import SUPPRESS, _StoreAction
from ..main import Attribute

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

# ===========================
# Attribute compilation classes
# ===========================

class Extension(Attribute):
	def __init__(self,
				 *option_strings,
				 dest = 'extension',
				 nargs = '*',
				 default = [],
				 type = None,
				 choices = None,
				 help = 'define target extension(s)',
				 metavar = None,

				 title = 'Extension',
				 description = 'option(s) to define extension(s)'):
		super(Extension, self).__init__(
			*(option_strings or ['-e', '--extension']),
			dest = dest,
			nargs = nargs,
			default = default,
			type = type,
			choices = choices,
			help = help,
			metavar = metavar or dest,

			title = title or dest,
			description = description
		)

		if self.restricted:
			if self.required:
				if len(self.choices) < self.min:
					raise ValueError(
						f"Number of restricted choices {self.choices} need to be " \
						f"equal or greater than minimum extensions required ({self.min})."
					)
				elif len(self.choices) == self.min:
					self.default = self.choices
					self.set_defaults(**{f"{self.dest}": self.choices})
					return

			elif len(self.choices) == 1:
				self.add_options(*self.choices, default=SUPPRESS)
				return

		self.set_defaults(**{f"{self.dest}": self.default})

		self.arguments.add_argument(*self.option_strings,
			action = 'append',
			dest = 'extension',
			nargs = {
				'?': 1,
				'*': '+'
			}.get(self.nargs, self.nargs),
			choices = self.choices if self.restricted else None,
			help = self.help,
			metavar = self.metavar
		)

		if self.choices:
			self.add_options(*self.choices, default=SUPPRESS)

	@property
	def arguments(self):
		self._arguments = getattr(self, '_arguments',
			self.add_mutually_exclusive_group(required=self.required) \
		 		if self.max == 1 else \
			self.add_required_group() \
				if self.required else \
			self.add_argument_group()
		)
		return self._arguments

	def add_options(self, *options, action='append_const', **kwargs):
		for option in options:
			self.arguments.add_argument(f"--{option}",
				action = action,
				dest = 'options',
				const= option,
				**kwargs
			)

	def __call__(self, namespace, extension=None, options=None):
		if options:
			extension += options
		setattr(namespace, self.dest, extension)

class Output(Attribute):
	def __init__(self,
				 *option_strings,
				 dest = 'output',
				 default = SUPPRESS,
				 type = None,
				 choices = None,
				 help = 'define a file to write script output',
				 metavar = None,

				 title = 'Output',
				 description = 'option(s) to define output preferences'):
		super(Output, self).__init__(
			*(option_strings or ['-o', '--output']),
			dest = dest,
			default = default,
			type = type,
			choices = choices,
			help = help,
			metavar = metavar,

			title = title or dest,
			description = description
		)

		self.add_argument(*self.option_strings,
			dest = 'output',
			default = self.default,
			choices = self.choices if self.restricted else None,
			help = self.help,
			metavar = self.metavar
		)

		group = self.add_dependent_group((self.option_strings,))
		group = group.add_mutually_exclusive_group()
		group.add_argument('-a', '--append',
			action = 'store_const',
			dest = 'mode',
			const = 'a',
			help = 'define output file open type'
		)
		group.add_argument('-w', '--write',
			action = 'store_const',
			dest = 'mode',
			const = 'w',
			help = 'define output file open type'
		)

	def __call__(self, namespace, output=None, mode='w'):
		if output != SUPPRESS:
			setattr(namespace, self.dest, open(output, mode))
