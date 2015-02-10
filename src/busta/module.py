"""
Module implementation.
"""
import fnmatch
import mmap
import os
import re


class ModuleException(Exception):
    """
    Module exception.
    """
    pass


class Module(object):
    """
    Module object.
    """
    name = None  # module name
    rel_path = None  # module relative path (as defined in config)
    abs_path = None  # module absolute path
    config = None  # config object
    is_simple = False  # `True` if this module is simple (JS file only)

    js_file = None  # module Javascript file (always only one JS file)
    js_dependencies = None  # list of module JavaScript dependencies
    css_files = None  # list of module css files

    _js_files_list = None
    _css_files_list = None

    def __init__(self, name, path, config):
        self._js_files_list = None
        self._css_files_list = None

        self.name = name
        self.rel_path = path
        self.config = config
        self.is_simple = False

        self.abs_path = os.path.abspath(
            os.path.join(self.config.root_dir, self.rel_path)
        )

        self.prepare_files()

    @property
    def human_name(self):
        """
        Returns module human name.
        """
        if self.is_simple:
            return self.js_file[len(self.config.root_dir):]
        else:
            return '{0}/'.format(self.abs_path[len(self.config.root_dir):])

    @property
    def js_human_name(self):
        """
        Returns module human name.
        """
        if self.js_file:
            return self.js_file[len(self.config.root_dir):]

    @staticmethod
    def find_files(directory, pattern):
        """
        Recursively walk a directory and yield all pattern files.
        """
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename

    def find_js(self):
        """
        Find module JavaScript file.
        """
        self.js_file = None

        # check if module is complex ('module' => 'module/module.js')
        if os.path.isdir(self.abs_path):
            module_name = os.path.basename(self.abs_path)
            for filename in os.listdir(self.abs_path):
                if filename.endswith(".js"):
                    if filename[0:-3].lower() == module_name.lower():
                        js_file = os.path.join(self.abs_path, filename)
                        if os.path.isfile(js_file):
                            self.js_file = js_file
                            self.is_simple = False
                            return

        # check if module is simple ('module' => 'module.js')
        js_file = '{0}.js'.format(self.abs_path)
        if os.path.isfile(js_file):
            self.js_file = js_file
            self.is_simple = True
            return

    def find_js_dependencies(self):
        """
        Find JavaScript dependencies.
        """
        self.js_dependencies = []

        if not self.js_file:
            return

        size = os.stat(self.js_file).st_size
        require_re = re.compile(r'\brequire\s*\(\s*([\'"])(.+?)\1\s*\)')

        with open(self.js_file, 'r') as js_file:
            data = mmap.mmap(js_file.fileno(), size, access=mmap.ACCESS_READ)
            self.js_dependencies = [
                require[1] for require in require_re.findall(data)
            ]

    def find_css(self):
        """
        Find module CSS files.
        """
        self.css_files = []

        if self.is_simple:
            return

        self.css_files = sorted([
            css_file for css_file in Module.find_files(self.abs_path, '*.css')
        ])

    def prepare_files(self):
        """
        Find all module files: js, css, fest templates, etc.
        """
        self.find_js()
        self.find_js_dependencies()
        self.find_css()

    @property
    def js_files_list(self):
        """
        Returns list of module JS files (including dependencies).
        """
        if self._js_files_list is None:
            self._js_files_list = []

            if self.js_file and self.js_dependencies:
                for module in self.js_dependencies:
                    for js_deps in self.config.modules[module].js_files_list:
                        self._js_files_list.append(js_deps)

            if self.js_file:
                self._js_files_list.append(self.js_file)

        return self._js_files_list

    @property
    def css_files_list(self):
        """
        Returns list of module CSS files (including dependencies).
        """
        if self._css_files_list is None:
            self._css_files_list = []

            if self.js_file and self.js_dependencies:
                for module in self.js_dependencies:
                    for css_deps in self.config.modules[module].css_files_list:
                        self._css_files_list.append(css_deps)

            if self.css_files:
                self._css_files_list.extend(self.css_files)

        return self._css_files_list
