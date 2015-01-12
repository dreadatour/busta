#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys

from busta.config import Config


def print_modules_list(config):
    """
    Print modules list from config.
    """
    if not config.modules:
        print("No modules defined")
        return

    print("Modules list:")

    max_length = 0
    for module_name in config.modules.keys():
        if len(module_name) > max_length:
            max_length = len(module_name)
    str_format = "  {{0: >{0}}} -> {{1}}".format(max_length)

    for module_name in sorted(config.modules.keys()):
        module = config.modules[module_name]
        if module.is_simple:
            print(str_format.format(module_name, module.js_file))
        else:
            print(str_format.format(module_name, module.abs_path + '/'))

    print()


def print_bundles_list(config):
    """
    Print bundles list from config.
    """
    if not config.bundles:
        print("  No bundles defined")
        return

    print("Bundles list:".format(config.config_file))

    max_length = 0
    for bundle in config.bundles:
        if len(bundle) > max_length:
            max_length = len(bundle)
    str_format = "  {{0: >{0}}} -> {{1}}".format(max_length)

    for bundle_name in sorted(config.bundles.keys()):
        bundle = config.bundles[bundle_name]
        print(str_format.format(bundle_name, bundle.output))

    print()


def print_bundle_info(bundle):
    """
    Print info about bundle.
    """
    print(" Modules:")
    print_modules_list(bundle.modules)
    print(" Output: {0}".format(bundle.output))
    if bundle.exclude:
        print(" Exclude:")
        for exclude in bundle.exclude:
            print("  {0}".format(exclude))
    else:
        print(" Excludes are not defined")
    if bundle.pre_processors:
        print(" Pre-processors:")
        for processor in bundle.pre_processors:
            print("  {0}".format(processor))
    else:
        print(" Pre-processors are not defined")
    if bundle.post_processors:
        print(" Post-processors:")
        for processor in bundle.post_processors:
            print("  {0}".format(processor))
    else:
        print(" Post-processors are not defined")


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

    if options.verbosity >= 2:
        print_modules_list(config)

    if options.verbosity >= 2:
        print_bundles_list(config)

    if options.verbosity >= 1:
        print("Config is OK")
