import argparse
from argcompile.utils import identity, MustImplementError


class _AttributesContainer(argparse._ActionsContainer):
    """ActionsContainer specialization to manage Attributes addition."""

    def __init__(self, description=None, prefix_chars='-', argument_default=None, conflict_handler='error'):
        super(_AttributesContainer, self).__init__(
            description,
            prefix_chars,
            argument_default,
            conflict_handler
        )

        self.register('type', None, identity)
        self._registries.setdefault('attribute', {})

    @property
    def arguments(self):
        """Retrieve list of related arguments dest."""
        return set(
            dest for dest
            in [a.dest for a in self._actions + self.attributes]
            if dest != argparse.SUPPRESS
        )

    @property
    def attributes(self):
        return list(self._registries.get('attribute', {}).values())

    def add_attribute(self, attr):
        self._add_container_actions(attr)

        self.set_defaults(**{
            attr.dest: attr.get_default(attr.dest)
        })
        self.register('attribute', str(id(attr)), attr)


class ArgumentCompiler(argparse.ArgumentParser, _AttributesContainer):
    """
    Customized ArgumentParser class that treats Attributes post-processing
    after the end of argument parsing.
    """

    def parse_args(self, args=None, namespace=None):
        """Extend argument parsing to handle attributes' namespace post-processing"""
        namespace = super(ArgumentCompiler, self).parse_args(args, namespace)

        for attribute in self._registries.get('attribute', {}).values():
            attribute.process(namespace)

        return namespace


class Attribute(_AttributesContainer):
    """
    ActionsContainer specialization capable of processing multiple input arguments
    into a unique Namespace attribute.

    During Attribute initialization it should be populated through `add_argument` method.
    The defined arguments will be forwarded to the parser that adds the Attribute,
    it will parse them without change and, after that, the Attribute will be called
    to process the parsed values, complementing Namespace manipulation.

    :param dest: namespace field name on which Attribute's result will be stored
    """
    def __init__(self, dest, **kwargs):
        super(Attribute, self).__init__(**kwargs)
        self.dest = dest

    def popargs(self, namespace):
        """Extract arguments from namespace and return found ones in a dict."""
        args = {}
        for argument in self.arguments:
            try:
                args[argument] = getattr(namespace, argument, self.argument_default)
                delattr(namespace, argument)
            except AttributeError:
                # It means namespace didn't have the target argument
                continue
        return args

    def process(self, namespace):
        """
        Execute namespace manipulation according to __call__ function,
        calling added attributes recursively
        """
        for attribute in self.attributes:
            attribute.process(namespace)

        kwargs = self.popargs(namespace)
        for key, value in self.__call__(**kwargs).items():
            setattr(namespace, key, value)

    def __call__(self, **kwargs):
        """
        The actual attribute's post-processing logic.
        Subclasses must implement this method.

        :param kwargs: the parsed values from all related arguments, obtained from `popargs` method
        :return a dict-like object to fulfill namespace
        """
        raise MustImplementError(self, '__call__')
