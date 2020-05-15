from ..attribute import *

# ===========================
# Attribute parsing classes
# ===========================

class Extension(Attribute):
	def __init__(self,
				 *option_strings,
				 dest = 'extension',
				 nargs = '*',
				 default = None,
				 type = None,
				 choices = None,
				 help = 'define target extension(s)',
				 metavar = 'extension',

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
			metavar = metavar,

			title = title or dest,
			description = description
		)

		if self.restricted:
			if self.required:
				if len(self.choices) < self.min:
					raise ValueError(
						"Number of restricted choices need to be equal or greater than minimum extensions required. \n" \
						f"Restricted choices: {self.choices}, Minimum extensions required: {self.min}"
					)
				elif len(self.choices) == self.min:
					self.default = self.choices
					self.set_defaults(**{f"{self.dest}": self.choices})
					return

			elif len(self.choices) == 1:
				self.add_options(*self.choices, action='store_const')
				return

		self.set_defaults(**{f"{self.dest}": self.default})

		self.arguments.add_argument(*self.option_strings,
			action = 'append_over',
			dest = self.dest,
			nargs = {
				'?': 1,
				'*': '+'
			}.get(self.nargs, self.nargs),
			default = self.default,
			choices = self.choices if self.restricted else None,
			help = self.help,
			metavar = self.metavar
		)

		if self.choices:
			self.add_options(*self.choices, default=SUPPRESS)


	def add_options(self, *options, action='append_const_over', **kwargs):
		for option in options:
			self.arguments.add_argument(f"--{option}",
				action = action,
				dest = self.dest,
				const=f"{option}",
				**kwargs
			)

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

		group = self.add_dependent_group(self, (self.option_strings,))
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
		def process(*, output = None, mode = None):
			mode = mode or 'w'
			if output != SUPPRESS:
				setattr(namespace, self.dest, open(output, mode))

		process(**self.popattr(namespace))
		return namespace
