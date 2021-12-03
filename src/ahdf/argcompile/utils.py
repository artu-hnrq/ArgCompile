def identity(x, *args):
    """Signature-flexible return-unchanged-input function"""
    if args:
        return (x,) + args
    return x


class MustImplementError(NotImplementedError):
    """Standardize message for NotImplementedError"""

    def __init__(self, instance, method):
        super(MustImplementError, self).__init__(
            f"Subclasses of {instance.__class__.__name__} must provide a {method} method"
        )
