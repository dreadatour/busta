#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import argparse
import sys

from busta.config import Config


def print_js_deps(config, module, level=0, used_modules=None):
    """
    Print module JS deps.
    """
    if not module.js_dependencies:
        return

    if used_modules is None:
        used_modules = []

    spaces = '         {0}'.format('    ' * level)
    last_i = len(module.js_dependencies) - 1
    for i, module_name in enumerate(module.js_dependencies):
        module_deps = config.modules[module_name]
        if i == last_i:
            prefix = u'{0}└── '.format(spaces)
        else:
            prefix = u'{0}├── '.format(spaces)
        print(u'{0}{1}'.format(prefix, module_deps.js_human_name))
        used_modules.append(module_name)
        print_js_deps(config, module_deps, level + 1, used_modules)


def print_modules_list(config, verbosity):
    """
    Print modules list from config.
    """
    if not config.modules:
        print("No modules defined")
        return

    print("Modules:")

    if verbosity >= 3:
        root_len = len(config.root_dir)
        for module_name in sorted(config.modules.keys()):
            module = config.modules[module_name]
            print('\n  "{0}":'.format(module_name))
            if module.js_file:
                print('    JS:  {0}'.format(module.js_human_name))

            if module.is_simple:
                continue

            print_js_deps(config, module)

            if module.css_files:
                for i, css_file in enumerate(module.css_files):
                    if i == 0:
                        prefix = '    CSS: '
                    else:
                        prefix = '         '
                    print('{0}{1}'.format(prefix, css_file[root_len:]))

    else:
        max_length = 0
        for module_name in config.modules.keys():
            if len(module_name) > max_length:
                max_length = len(module_name)

        str_format = "  {{0: >{0}}} -> {{1}}".format(max_length + 2)
        for module_name in sorted(config.modules.keys()):
            module = config.modules[module_name]
            module_name = '"{0}"'.format(module_name)
            print(str_format.format(module_name, module.human_name))

    print()


def print_bundles_list(config, verbosity):
    """
    Print bundles list from config.
    """
    if not config.bundles:
        print("  No bundles defined")
        return

    print("Bundles:")

    root_len = len(config.root_dir)
    for bundle_name in sorted(config.bundles.keys()):
        bundle = config.bundles[bundle_name]

        if verbosity >= 3:
            print('\n  "{0}"'.format(bundle_name))

            print('     Modules:')
            for module_name in bundle.modules:
                print(u'     - {0}'.format(module_name))

            print('     Files:')

            if bundle.js_files_list:
                print('     - {0}:'.format(
                    bundle.output_file('js')[root_len:])
                )
                last_i = len(bundle.js_files_list) - 1
                for i, js_file in enumerate(bundle.js_files_list):
                    if i == last_i:
                        prefix = u'        └── '
                    else:
                        prefix = u'        ├── '
                    print(u'{0}{1}'.format(prefix, js_file[root_len:]))

            if bundle.css_files_list:
                print('     - {0}:'.format(
                    bundle.output_file('css')[root_len:])
                )
                last_i = len(bundle.css_files_list) - 1
                for i, css_file in enumerate(bundle.css_files_list):
                    if i == last_i:
                        prefix = u'        └── '
                    else:
                        prefix = u'        ├── '
                    print(u'{0}{1}'.format(prefix, css_file[root_len:]))

        else:
            print('  "{0}" modules:'.format(bundle_name))
            last_i = len(bundle.modules) - 1
            for i, module_name in enumerate(bundle.modules):
                if i == last_i:
                    prefix = u'   └── '
                else:
                    prefix = u'   ├── '
                print(u'{0}"{1}"'.format(prefix, module_name))

    print()


def main():
    parser = argparse.ArgumentParser(description='Build static bundles')
    parser.add_argument('config', metavar='[config_file]',
                        help='bundles config filename')
    parser.add_argument('-v', action='count', default=0, dest='verbosity',
                        help='verbosity level')
    options = parser.parse_args()

    try:
        config = Config(options.config)
    except Exception as exc:
        print("Error: {0}".format(exc))
        sys.exit(1)

    if options.verbosity >= 1:
        print("Config file: {0}".format(config.config_file))
        if options.verbosity >= 2:
            print()

    if options.verbosity >= 1:
        print("Root directory: {0}".format(config.root_dir))
        if options.verbosity >= 2:
            print()

    if options.verbosity >= 2 and config.pre_processors:
        print("Pre-processors:")
        for pre_processor in config.pre_processors.keys():
            print('  "{0}"'.format(pre_processor))
        print()

    if options.verbosity >= 2 and config.post_processors:
        print("Post-processors:")
        for post_processor in config.post_processors.keys():
            print('  "{0}"'.format(post_processor))
        print()

    if options.verbosity >= 2:
        print_modules_list(config, options.verbosity)

    if options.verbosity >= 2:
        print_bundles_list(config, options.verbosity)

    if options.verbosity >= 1:
        print("Config is OK")
