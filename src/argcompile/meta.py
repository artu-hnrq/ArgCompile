import inspect

class MetaComposition(type):
	"Overwrites a target method to behave calling same-type superclasses' implementation orderly"

	def __new__(meta, name, bases, attr, __func__='__call__'):
		attr['__run__'] = attr[__func__]
		attr[__func__] = meta.__run__

		return super(MetaComposition, meta).__new__(
			meta, name, bases, attr
		)

	def __run__(self, *args, **kwargs):
		for compound in self.__class__.__compound__:
			compound.__run__(self, *args, **kwargs)

	@property
	def __compound__(cls):
		return [
			element
			for element in
			list(cls.__mro__)[::-1]
			if type(element)
			is type(cls)
		]

class MetaArgumentCompiler(MetaComposition):
	"Tracks __init__ keyword arguments to manage Actions and Attributes configuration"

	def __new__(meta, name, bases, attr):
		__config__ = attr.pop('__config__', {})
		__action__ = attr.pop('__action__', {})
		__attr__ = attr.pop('__attr__', {})

		for keys in [__action__.keys(), __attr__.keys()]:
			for key in keys:
				if key not in __config__.keys():
					__config__[key] = {}

		__init__ = attr.pop('__init__', None)

		def init(self, *a, **kw):
			config = {}
			for key, args in __config__.items():
				if key in __action__.keys() or key in __attr__.keys():
					config[key] = args
					config[key].update(kw.pop(key, {}))
				else:
					kw[key] = args
					kw[key].update(kw.get(key, {}))

			if __init__:
				__init__(self, *a, **kw)

			for key, args in config.items():
				if key in __action__:
					self.add_argument(
						*config[key].pop('*', []),
						action = __action__[key],
						**config[key]
					)
				else:
					self.add_attribute(
						__attr__[key](*config[key].pop('*', []), **config[key])
					)

		attr['__init__'] = init

		return super(MetaArgumentCompiler, meta).__new__(meta, name, bases, attr)

	def __run__(self, namespace):
		for compiler in self.__class__.__compound__:
			namespace = compiler.__run__(self, namespace)
		return namespace


class MetaAttribute(type):
	"Overwrites __call__ method to pop temporary arguments from Namespace in order to process them"

	def __new__(meta, name, bases, attr):
		__run__ = attr.get('__call__', None)
		if __run__:
			args = inspect.getargspec(__run__).args[1:]
			def __call__(self, namespace):
				attr = dict()
				for arg in args:
					value = getattr(namespace, arg, None)
					if value:
						attr[arg] = value
						delattr(namespace, arg)

				__run__(self, namespace, **attr)
				return namespace

			attr['__call__'] = __call__

		return super(MetaAttribute, meta).__new__(meta, name, bases, attr)

# class Meta(type):
	# def __new__(meta, name, bases, attr):
	# 	"""Meta description of class definition"""
	# 	return super(Meta, meta).__new__(meta, name, bases, attr)

	# def __init__(cls, name, bases, attr, compound):
	# 	""" Meta intervention on class instantiation """
	# 	return super(Meta, cls).__init__(cls, name, bases, attr)

	# def __call__(cls, *args):
	# 	""" Meta modifications in object instantiation """
	# 	return super(Meta, cls).__call__(cls, *args)
