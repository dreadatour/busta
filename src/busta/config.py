"""
Read and parse config files.
"""
import json
import os

from busta.bundle import Bundle
from busta.minify_json import minify_json
from busta.module import Module


class ConfigException(Exception):
    """
    Config exception.
    """
    pass


class Config(object):
    """
    Config parser and validator.
    """
    config_file = None  # file with JSON config
    root_dir = None  # root directory, defined in config
    output_dir = None  # default output directory
    modules = None  # modules dictionary
    bundles = None  # bundles dictionary
    pre_processors = None  # pre-processors dictionary
    post_processors = None  # post-processors dictionary

    def __init__(self, config_file):
        """
        Initialize config parser.
        """
        self.config_file = os.path.abspath(config_file)
        self.root_dir = None
        self.output_dir = None
        self.modules = {}
        self.bundles = {}
        self.pre_processors = {}
        self.post_processors = {}
        self.parse_config()

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
                return json.loads(minify_json(file_data.read()))
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

        if 'root_dir' in config:
            if not isinstance(config['root_dir'], basestring):
                raise ConfigException("Param 'root_dir' must be 'string'")

        if 'output_dir' in config:
            if not isinstance(config['output_dir'], basestring):
                raise ConfigException("Param 'output_dir' must be 'string'")

        if 'modules' not in config:
            raise ConfigException("Param 'modules' is not found")
        if not isinstance(config['modules'], dict):
            raise ConfigException("Param 'modules' must be 'dict'")

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
            'root_dir', 'output_dir', 'modules', 'bundles',
            'pre_processors', 'post_processors'
        )
        for param in config.keys():
            if param not in config_params:
                raise ConfigException("Unknown param '{0}'".format(param))

    @staticmethod
    def validate_pre_processors(pre_processors):
        """
        Validate modules from config.
        """
        if not isinstance(pre_processors, dict):
            raise ConfigException("Pre_processors must be 'dict'")

        for name, command in pre_processors.iteritems():
            if not isinstance(name, basestring):
                raise ConfigException(
                    "Pre_processor name '{0}' must be 'string'".format(name)
                )
            if not isinstance(command, basestring):
                raise ConfigException(
                    "Pre_processor command '{0}' must be 'string'".format(name)
                )

    @staticmethod
    def validate_post_processors(post_processors):
        """
        Validate modules from config.
        """
        if not isinstance(post_processors, dict):
            raise ConfigException("Post_processors must be 'dict'")

        for name, command in post_processors.iteritems():
            if not isinstance(name, basestring):
                raise ConfigException(
                    "Post_processor name '{0}' must be 'string'".format(name)
                )
            if not isinstance(command, basestring):
                raise ConfigException((
                    "Post_processor command '{0}'"
                    " must be 'string'").format(name)
                )

    @staticmethod
    def validate_module(name, path):
        """
        Validate module from config.
        """
        if not isinstance(name, basestring):
            raise ConfigException(
                "Module '{0}' name must be 'string'".format(name)
            )
        if not isinstance(path, basestring):
            raise ConfigException(
                "Module '{0}' path must be 'string'".format(name)
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
        if name != name.lower():
            raise ConfigException(
                "Bundle '{0}' name must be lowercase".format(name)
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

        if 'output_dir' in params:
            if not isinstance(params['output_dir'], basestring):
                raise ConfigException((
                    "Bundle '{0}' 'output_dir' param"
                    " must be 'string'").format(name)
                )

        if 'exclude' in params:
            if not isinstance(params['exclude'], list):
                raise ConfigException((
                    "Bundle '{0}' 'exclude' param"
                    " must be 'string'").format(name)
                )
            for exclude in params['exclude']:
                if not isinstance(exclude, basestring):
                    raise ConfigException((
                        "Bundle '{0}' exclude name '{0}'"
                        " must be 'string'").format(name, exclude)
                    )

        if 'pre_processors' in params:
            if not isinstance(params['pre_processors'], list):
                raise ConfigException((
                    "Bundle '{0}' 'pre_processors' param"
                    " must be 'string'").format(name)
                )
            for processor in params['pre_processors']:
                if not isinstance(processor, basestring):
                    raise ConfigException((
                        "Bundle '{0}' pre_processor name '{0}'"
                        " must be 'string'").format(name, processor)
                    )

        if 'post_processors' in params:
            if not isinstance(params['post_processors'], list):
                raise ConfigException((
                    "Bundle '{0}' 'post_processors' param"
                    " must be 'string'").format(name)
                )
            for processor in params['post_processors']:
                if not isinstance(processor, basestring):
                    raise ConfigException((
                        "Bundle '{0}' post_processor name '{0}'"
                        " must be 'string'").format(name, processor)
                    )

        bundle_params = (
            'modules', 'output_dir', 'exclude', 'pre_processors',
            'post_processors'
        )
        for param in params.keys():
            if param not in bundle_params:
                raise ConfigException(
                    "Unknown param '{0}' in bundle '{1}'".format(param, name)
                )

    def parse_config(self):
        """
        Parse config file and validate it.
        """
        config = Config.read_json(self.config_file)

        # config base validation
        Config.validate_config(config)

        # get and validate root dir
        config_dir = os.path.dirname(self.config_file)
        if 'root_dir' in config:
            self.root_dir = os.path.join(config_dir, config['root_dir'])
        else:
            self.root_dir = config_dir

        if 'output_dir' in config:
            self.output_dir = os.path.abspath(
                os.path.join(self.root_dir, config['output_dir'])
            )

        if not os.path.isdir(self.root_dir):
            raise ConfigException(
                "Root directory '{0}' is not exist".format(self.root_dir)
            )

        # get and validate pre_processors
        if 'pre_processors' in config:
            self.pre_processors = config['pre_processors']
            Config.validate_pre_processors(self.pre_processors)

        # get and validate post_processors
        if 'post_processors' in config:
            self.post_processors = config['post_processors']
            Config.validate_post_processors(self.post_processors)

        # get and validate modules, create Module objects
        for name, path in config['modules'].iteritems():
            Config.validate_module(name, path)
            self.modules[name] = Module(
                name=name,
                path=path,
                config=self
            )

        # get and validate bundles, create Bundle objects
        for name, params in config['bundles'].iteritems():
            Config.validate_bundle(name, params)
            if 'output_dir' in params:
                output_dir = os.path.abspath(
                    os.path.join(self.root_dir, params['output_dir'])
                )
            elif self.output_dir:
                output_dir = self.output_dir
            else:
                raise ConfigException((
                    "Bundle '{0}' 'output_dir' param is not defined"
                    " and global 'output_dir' param"
                    " in not defined".format(name)
                ))

            self.bundles[name] = Bundle(
                name=name,
                modules=params['modules'],
                output_dir=output_dir,
                exclude=params.get('exclude'),
                pre_processors=params.get('pre_processors'),
                post_processors=params.get('post_processors'),
                config=self
            )
