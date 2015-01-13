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
    output_dir = None  # output directory for this bundle
    exclude = None  # list of modules we need to exclude from out bundle
    pre_processors = None  # list of bundle pre-processors
    post_processors = None  # list of bundle post-processors
    config = None  # config object

    _js_files_list = None
    _css_files_list = None

    def __init__(self, name, modules, output_dir, exclude, pre_processors,
                 post_processors, config):
        self._js_files_list = None
        self._css_files_list = None

        self.name = name
        self.modules = modules or []
        self.output_dir = output_dir
        self.exclude = exclude or []
        self.pre_processors = pre_processors or []
        self.post_processors = post_processors or []
        self.config = config

    def output_file(self, ext):
        """
        Returns output filename with defined extension.
        """
        return '{0}/{1}.{2}'.format(self.output_dir, self.name, ext)

    @property
    def js_files_list(self):
        """
        Returns list of JS files.
        """
        if self._js_files_list is None:
            self._js_files_list = []

            for module in self.modules:
                self._js_files_list.extend(
                    self.config.modules[module].js_files_list or []
                )

        return self._js_files_list

    @property
    def css_files_list(self):
        """
        Returns list of CSS files.
        """
        if self._css_files_list is None:
            self._css_files_list = []

            for module in self.modules:
                self._css_files_list.extend(
                    self.config.modules[module].css_files_list or []
                )

        return self._css_files_list
