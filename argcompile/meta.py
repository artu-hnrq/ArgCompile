class MetaComposition(type):
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
