#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import argparse
import sys

from busta.config import Config


DRAW_NONE = u'    '
DRAW_ONLY = u'─── '
DRAW_FROM = u'┬── '
DRAW_SKIP = u'│   '
DRAW_NEXT = u'├── '
DRAW_LAST = u'└── '

FONT_UNDERLINE = '\033[4m'
FONT_BOLD = '\033[1m'
FONT_OFF = '\033[0m'


def print_js_dependencies(module, levels=None, padding=0):
    """
    Print module JS dependencies recursively.
    """
    if not module.js_dependencies:
        return

    if levels is None:
        levels = []

    spaces = ' ' * padding
    for level in levels:
        if level:
            spaces += DRAW_NONE
        else:
            spaces += DRAW_SKIP

    last_i = len(module.js_dependencies) - 1
    for i, module_name in enumerate(module.js_dependencies):
        is_last = bool(i == last_i)
        if is_last:
            prefix = spaces + DRAW_LAST
        else:
            prefix = spaces + DRAW_NEXT

        dependency = module.config.modules[module_name]
        print(prefix + dependency.js_human_name)

        if dependency.js_dependencies:
            new_levels = levels + [is_last]
            print_js_dependencies(dependency, new_levels, padding=padding)


def print_modules_list(config, verbosity):
    """
    Print modules list from config.
    """
    if not config.modules:
        print("No modules defined")
        return

    if verbosity >= 3:
        root_len = len(config.root_dir)

        for module_name in sorted(config.modules.keys()):
            module = config.modules[module_name]
            print('\nModule "{0}":'.format(FONT_BOLD + module_name + FONT_OFF))

            if module.js_file:
                filename = module.js_human_name
                print(u'    JS {0}{1}'.format(DRAW_ONLY, filename))
                print_js_dependencies(module, padding=11)

            if module.css_files:
                count_i = len(module.css_files)
                for i, css_file in enumerate(module.css_files):
                    if i == 0:
                        prefix = '   CSS '
                        if count_i == 1:
                            prefix += DRAW_ONLY
                        else:
                            prefix += DRAW_FROM
                    else:
                        prefix = ' ' * 7
                        if i == count_i - 1:
                            prefix += DRAW_LAST
                        else:
                            prefix += DRAW_NEXT
                    print(prefix + css_file[root_len:])

    else:
        print("Modules:")

        max_length = 0
        for module_name in config.modules.keys():
            if len(module_name) > max_length:
                max_length = len(module_name)
        str_format = u"{{0: >{0}}} {1}{{1}}".format(max_length + 2, DRAW_ONLY)

        for module_name in sorted(config.modules.keys()):
            module = config.modules[module_name]
            module_name = '"' + module_name + '"'
            print('  ' + str_format.format(module_name, module.human_name))


def print_bundles_list(config, verbosity):
    """
    Print bundles list from config.
    """
    if not config.bundles:
        print("No bundles defined")
        return

    root_len = len(config.root_dir)
    if verbosity >= 3:
        for bundle_name in sorted(config.bundles.keys()):
            bundle = config.bundles[bundle_name]

            print('\nBundle "{0}"'.format(
                FONT_UNDERLINE + bundle_name + FONT_OFF
            ))

            count_i = len(bundle.modules)
            for i, module_name in enumerate(bundle.modules):
                if i == 0:
                    prefix = '  Modules '
                    if count_i == 1:
                        prefix += DRAW_ONLY
                    else:
                        prefix += DRAW_FROM
                else:
                    prefix = ' ' * 10
                    if i == count_i - 1:
                        prefix += DRAW_LAST
                    else:
                        prefix += DRAW_NEXT
                print(prefix + '"' + FONT_BOLD + module_name
                      + FONT_OFF + '"')

            count_i = len(bundle.exclude)
            for i, exclude_name in enumerate(bundle.exclude):
                if i == 0:
                    prefix = '  Exclude '
                    if count_i == 1:
                        prefix += DRAW_ONLY
                    else:
                        prefix += DRAW_FROM
                else:
                    prefix = ' ' * 10
                    if i == count_i - 1:
                        prefix += DRAW_LAST
                    else:
                        prefix += DRAW_NEXT
                print(prefix + '"' + FONT_UNDERLINE + exclude_name
                      + FONT_OFF + '"')

            if bundle.js_files:
                filename = bundle.output_file('js')[root_len:]
                prefix = '    Files '
                if bundle.css_files:
                    prefix += DRAW_FROM
                else:
                    prefix += DRAW_ONLY
                print(prefix + filename)

                count_i = len(bundle.js_files)
                for i, js_file in enumerate(bundle.js_files):
                    if bundle.css_files:
                        prefix = DRAW_SKIP
                    else:
                        prefix = DRAW_NONE
                    if i == count_i - 1:
                        prefix += DRAW_LAST
                    else:
                        prefix += DRAW_NEXT
                    print(' ' * 10 + prefix + js_file[root_len:])

            if bundle.css_files:
                filename = bundle.output_file('css')[root_len:]
                if bundle.js_files:
                    prefix = '          '
                else:
                    prefix = '    Files '
                if bundle.js_files:
                    prefix += DRAW_LAST
                else:
                    prefix += DRAW_ONLY
                print(prefix + filename)

                for i, css_file in enumerate(bundle.css_files):
                    prefix = DRAW_NONE
                    if i == len(bundle.css_files) - 1:
                        prefix += DRAW_LAST
                    else:
                        prefix += DRAW_NEXT
                    print(' ' * 10 + prefix + css_file[root_len:])
    elif verbosity >= 2:
        for bundle_name in sorted(config.bundles.keys()):
            bundle = config.bundles[bundle_name]

            print('\nBundle "{0}"'.format(
                FONT_UNDERLINE + bundle_name + FONT_OFF
            ))
            count_i = len(bundle.modules)
            for i, module_name in enumerate(bundle.modules):
                if i == 0:
                    prefix = '  Modules '
                    if count_i == 1:
                        prefix += DRAW_ONLY
                    else:
                        prefix += DRAW_FROM
                else:
                    prefix = ' ' * 10
                    if i == count_i - 1:
                        prefix += DRAW_LAST
                    else:
                        prefix += DRAW_NEXT
                print(prefix + '"' + module_name + '"')

            count_i = len(bundle.exclude)
            for i, exclude_name in enumerate(bundle.exclude):
                if i == 0:
                    prefix = '  Exclude '
                    if count_i == 1:
                        prefix += DRAW_ONLY
                    else:
                        prefix += DRAW_FROM
                else:
                    prefix = ' ' * 10
                    if i == count_i - 1:
                        prefix += DRAW_LAST
                    else:
                        prefix += DRAW_NEXT
                print(prefix + '"' + FONT_UNDERLINE + exclude_name
                      + FONT_OFF + '"')

            if bundle.js_files:
                filename = bundle.output_file('js')[root_len:]
                prefix = '    Files '
                if bundle.css_files:
                    prefix += DRAW_FROM
                else:
                    prefix += DRAW_ONLY
                print(prefix + filename)

            if bundle.css_files:
                filename = bundle.output_file('css')[root_len:]
                if bundle.js_files:
                    prefix = '          '
                else:
                    prefix = '    Files '
                if bundle.js_files:
                    prefix += DRAW_LAST
                else:
                    prefix += DRAW_ONLY
                print(prefix + filename)
    elif verbosity >= 1:
        bundles_files = []
        for bundle_name in sorted(config.bundles.keys()):
            bundle = config.bundles[bundle_name]

            if bundle.js_files:
                bundles_files.append(bundle.output_file('js'))

            if bundle.css_files:
                bundles_files.append(bundle.output_file('css'))

        for i, bundle_file in enumerate(bundles_files):
            if i == 0:
                prefix = 'Bundles output:   '
            else:
                prefix = '                  '
            print(prefix + bundle_file)


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
        print("Config file:      {0}".format(config.config_file))
        if options.verbosity >= 3:
            print()

    if options.verbosity >= 1:
        print("Root directory:   {0}".format(config.root_dir))
        if options.verbosity >= 3:
            print()

    if options.verbosity >= 1 and config.output_dir:
        print("Output directory: {0}".format(config.output_dir))
        if options.verbosity >= 2:
            print()

    if options.verbosity >= 2:
        print_modules_list(config, options.verbosity)
        if options.verbosity >= 3:
            print()

    if options.verbosity >= 1:
        print_bundles_list(config, options.verbosity)
