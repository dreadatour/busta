"""
Read and parse config files.
"""
import json
import os

from busta.bundle import Bundle


class ConfigException(Exception):
    """
    Config exception.
    """
    pass


class Config(object):
    """
    Config parser and validator.
    """
    config_file = None
    root_dir = None
    modules = None
    modules_file = None
    bundles = None
    pre_processors = None
    post_processors = None

    def __init__(self, config_file):
        """
        Initialize config parser.
        """
        self.config_file = os.path.abspath(config_file)
        try:
            self.parse_config()
        except ConfigException as exc:
            raise ConfigException("{0} in {1}".format(exc, self.config_file))

    @staticmethod
    def read_json(filename):
        """
        Read JSON file.

        :param filename: name of JSON file
        :return: JSON content
        """
        file_abs = os.path.abspath(filename)

        if not os.path.isfile(file_abs):
            raise ConfigException("File is not exist: {0}".format(filename))

        try:
            file_data = open(file_abs)
            try:
                return json.load(file_data)
            except ValueError as exc:
                raise ConfigException(
                    "Error while parsing JSON {0}: {1}".format(filename, exc)
                )
            finally:
                file_data.close()
        except (IOError, OSError) as exc:
            raise ConfigException(
                "Error while reading file {0}: {1}".format(filename, exc)
            )

    @staticmethod
    def validate_config(config):
        """
        Validate config root.
        """
        if not isinstance(config, dict):
            raise ConfigException("Only 'dict' type allowed for config")

        if 'root' in config:
            if not isinstance(config['root'], basestring):
                raise ConfigException("Param 'root' must be 'string'")

        if 'modules' not in config:
            raise ConfigException("Param 'modules' is not found")
        if not isinstance(config['modules'], (basestring, dict)):
            raise ConfigException("Param 'modules' must be 'string' or 'dict'")

        if 'bundles' not in config:
            raise ConfigException("Param 'bundles' is not found")
        if not isinstance(config['bundles'], dict):
            raise ConfigException("Param 'bundles' must be 'dict'")

        if 'pre_processors' in config:
            if not isinstance(config['pre_processors'], dict):
                raise ConfigException("Param 'pre_processors' must be 'dict'")
        if 'post_processors' in config:
            if not isinstance(config['post_processors'], dict):
                raise ConfigException("Param 'post_processors' must be 'dict'")

        config_params = (
            'root', 'modules', 'bundles', 'pre_processors', 'post_processors'
        )
        for param in config.keys():
            if param not in config_params:
                raise ConfigException("Unknown param '{0}'".format(param))

    @staticmethod
    def validate_modules(modules):
        """
        Validate modules from config.
        """
        if not isinstance(modules, dict):
            raise ConfigException("Aliases must be 'dict'")

        for name, directory in modules.iteritems():
            if not isinstance(name, basestring):
                raise ConfigException(
                    "Module name '{0}' must be 'string'".format(name)
                )
            if not isinstance(directory, basestring):
                raise ConfigException(
                    "Module directory '{0}' must be 'string'".format(name)
                )

    @staticmethod
    def validate_bundle(name, params):
        """
        Validate bundles from config.
        """
        if not isinstance(name, basestring):
            raise ConfigException(
                "Bundle '{0}' name must be string".format(name)
            )
        if not isinstance(params, dict):
            raise ConfigException(
                "Bundle '{0}' params must be 'dict'".format(name)
            )

        if 'modules' not in params:
            raise ConfigException(
                "Bundle '{0}' have no 'module' param".format(name)
            )
        if not isinstance(params['modules'], list):
            raise ConfigException(
                "Bundle '{0}' 'modules' param must be 'list'".format(name)
            )
        if not len(params['modules']):
            raise ConfigException(
                "Bundle '{0}' 'modules' param is empty".format(name)
            )

        if 'output' not in params:
            raise ConfigException(
                "Bundle '{0}' have no 'output' param".format(name)
            )
        if not isinstance(params['output'], basestring):
            raise ConfigException(
                "Bundle '{0}' 'output' param must be 'string'".format(name)
            )

        if 'exclude' in params:
            if not isinstance(params['exclude'], list):
                raise ConfigException((
                    "Bundle '{0}' 'exclude' param"
                    "must be 'string'").format(name)
                )

        if 'pre_processors' in params:
            if not isinstance(params['pre_processors'], list):
                raise ConfigException((
                    "Bundle '{0}' 'pre_processors' param"
                    "must be 'string'").format(name)
                )

        if 'post_processors' in params:
            if not isinstance(params['post_processors'], list):
                raise ConfigException((
                    "Bundle '{0}' 'post_processors' param"
                    "must be 'string'").format(name)
                )

        bundle_params = (
            'modules', 'output', 'exclude', 'pre_processors', 'post_processors'
        )
        for param in params.keys():
            if param not in bundle_params:
                raise ConfigException(
                    "Unknown param '{0}' in bundle '{1}'".format(param, name)
                )

    def absolute_modules(self, modules):
        """
        Find absolute directories names for all modules.
        """
        result = {}
        for name, dir_name in modules.iteritems():
            module_dir = os.path.abspath(os.path.join(self.root_dir, dir_name))
            if os.path.isdir(module_dir):
                result[name] = module_dir
            else:
                raise ConfigException((
                    "Source dir {0} for module '{1}'"
                    "is not found").format(module_dir, name)
                )
        return result

    def bundle_absolute_modules(self, modules):
        """
        Find absolute filename for all sources (use modules).
        """
        result = {}
        for module in modules:
            if module in self.modules:
                result[module] = self.modules[module]
            else:
                raise ConfigException(
                    "Module is not defined: {0}".format(module)
                )
        return result

    def parse_config(self):
        """
        Parse config file and validate it.
        """
        config = Config.read_json(self.config_file)

        # config base validation
        Config.validate_config(config)

        # get root dir from config and check if dir is exist
        config_dir = os.path.dirname(self.config_file)
        if 'root' in config:
            self.root_dir = os.path.join(config_dir, config['root'])
        else:
            self.root_dir = config_dir

        if not os.path.isdir(self.root_dir):
            raise ConfigException(
                "Root directory '{0}' is not exist".format(self.root_dir)
            )

        # find modules from config
        if isinstance(config['modules'], basestring):
            self.modules_file = os.path.join(self.root_dir, config['modules'])
            modules = Config.read_json(self.modules_file)
        else:
            self.modules_file = self.config_file
            modules = config['modules']

        # validate modules and build abs paths for them
        self.validate_modules(modules)
        self.modules = self.absolute_modules(modules)

        # get bundles from config, validate them and create Bundle objects
        self.bundles = {}
        for name, params in config['bundles'].iteritems():
            # validate bundle
            Config.validate_bundle(name, params)

            bundle_modules = self.bundle_absolute_modules(params['modules'])
            output = os.path.abspath(os.path.join(
                self.root_dir, params['output']
            ))

            # TODO: parse bundle 'exclude' param
            # TODO: parse bundle 'pre_processors' param
            # TODO: parse bundle 'post_processors' param

            # build bundle
            self.bundles[name] = Bundle(
                name=name,
                modules=bundle_modules,
                output=output,
                config=self
            )

        # TODO: parse 'pre_processors' param
        # TODO: parse 'post_processors' param
