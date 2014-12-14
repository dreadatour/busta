"""
Bundle implementation.
"""


class Bundle(object):
    """
    Bundle object.
    """
    name = None
    modules = None
    output = None
    config = None
    exclude = None
    pre_processors = None
    post_processors = None

    def __init__(self, name, modules, output, config):
        self.name = name
        self.modules = modules
        self.output = output
        # TODO: add 'exclude' param
        # TODO: add 'pre_processors' param
        # TODO: add 'post_processors' param
        self.config = config
