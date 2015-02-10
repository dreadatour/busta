"""
Bundle implementation.
"""


def deduplicate(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


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

    _js_files = None
    _css_files = None
    _js_excluded = None
    _css_excluded = None

    def __init__(self, name, modules, output_dir, exclude, pre_processors,
                 post_processors, config):
        self._js_files = None
        self._css_files = None
        self._js_excluded = None
        self._css_excluded = None

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
    def all_js_files(self):
        """
        Returns list of all JS files (deduplicated and even excluded).
        """
        js_files = []
        for module_name in self.modules:
            js_files.extend(self.config.modules[module_name].js_files_list)
        return js_files

    @property
    def all_css_files(self):
        """
        Returns list of CSS files (deduplicated and even excluded).
        """
        css_files = []
        for module_name in self.modules:
            css_files.extend(self.config.modules[module_name].css_files_list)
        return css_files

    @property
    def js_files(self):
        """
        Returns list of JS files.
        """
        if self._js_files is not None:
            return self._js_files

        self._js_files = []
        self._js_excluded = []

        for js_file in deduplicate(self.all_js_files):
            excluded_files = set()

            for exclude_name in self.exclude:
                excludes = self.config.bundles[exclude_name].all_js_files
                excluded_files.update(excludes)

            if js_file in excluded_files:
                self._js_excluded.append(js_file)
            else:
                self._js_files.append(js_file)

        return self._js_files

    @property
    def css_files(self):
        """
        Returns list of CSS files.
        """
        if self._css_files is not None:
            return self._css_files

        self._css_files = []
        self._css_excluded = []

        for css_file in deduplicate(self.all_css_files):

            excluded_files = set()

            for exclude_name in self.exclude:
                excludes = self.config.bundles[exclude_name].all_css_files
                excluded_files.update(excludes)

            if css_file in excluded_files:
                self._css_excluded.append(css_file)
            else:
                self._css_files.append(css_file)

        return self._css_files

    @property
    def js_excluded(self):
        """
        Returns list of excluded JS files.
        """
        if self._js_excluded is None:
            self.js_files
        return self._js_excluded

    @property
    def css_excluded(self):
        """
        Returns list of excluded CSS files.
        """
        if self._css_excluded is None:
            self.css_files
        return self._css_excluded
