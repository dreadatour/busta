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

    def __init__(self, name, modules, output, exclude, pre_processors,
                 post_processors, config):
        self.name = name
        self.modules = modules
        self.output = output
        self.exclude = exclude
        self.pre_processors = pre_processors
        self.post_processors = post_processors
        self.config = config
