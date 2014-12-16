"""
Bundle implementation.
"""


class BundleException(Exception):
    """
    Bundle exception.
    """
    pass


class Bundle(object):
    """
    Bundle object.
    """
    name = None  # bundle name
    modules = None  # list of modules, included in bundle
    output = None  # output directory for this bundle
    exclude = None  # list of modules we need to exclude from out bundle
    pre_processors = None  # list of bundle pre-processors
    post_processors = None  # list of bundle post-processors
    config = None  # config object

    def __init__(self, name, modules, output, exclude, pre_processors,
                 post_processors, config):
        self.name = name
        self.modules = modules
        self.output = output
        self.exclude = exclude
        self.pre_processors = pre_processors
        self.post_processors = post_processors
        self.config = config
