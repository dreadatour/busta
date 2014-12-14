#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys

from busta.config import Config, ConfigException


def print_modules_list(modules):
    """
    Print modules list from config.
    """
    if not modules:
        print("  No modules defined")
        return

    max_length = 0
    for module in modules.keys():
        if len(module) > max_length:
            max_length = len(module)
    str_format = "  {{0: >{0}}} -> {{1}}".format(max_length)

    for module in sorted(modules.keys()):
        print(str_format.format(module, modules[module]))


def print_bundles_list(bundles):
    """
    Print bundles list from config.
    """
    if not bundles:
        print("  No bundles defined")
        return

    max_length = 0
    for bundle in bundles:
        if len(bundle) > max_length:
            max_length = len(bundle)
    str_format = "  {{0: >{0}}} -> {{1}}".format(max_length)

    for bundle_name in sorted(bundles.keys()):
        bundle = bundles[bundle_name]
        print(str_format.format(bundle_name, bundle.output))


def print_bundle_info(bundle):
    """
    Print info about bundle.
    """
    print(" Modules:")
    print_modules_list(bundle.modules)
    print(" Output: {0}".format(bundle.output))
    if bundle.exclude:
        print(" Exclude:")
        print_modules_list(bundle.exclude)
    else:
        print(" Excludes are not defined")
    if bundle.pre_processors:
        print(" Pre-processors:")
        # TODO: print pre-processors
    else:
        print(" Pre-processors are not defined")
    if bundle.post_processors:
        print(" Post-processors:")
        # TODO: print post-processors
    else:
        print(" Post-processors are not defined")


def main():
    parser = argparse.ArgumentParser(description='Build static bundles')
    parser.add_argument('config', metavar='[config_file]',
                        help='bundles config filename')
    parser.add_argument('--show-modules-list', action='store_true',
                        help='print modules list and exit')
    parser.add_argument('--show-bundles-list', action='store_true',
                        help='print bundles list and exit')
    parser.add_argument('--show-bundle-info', type=str,
                        help='print bundle info and exit')
    options = parser.parse_args()

    try:
        config = Config(options.config)
    except ConfigException as exc:
        print("Error: {0}".format(exc))
        sys.exit(1)

    if options.show_modules_list:
        print("Modules defined in {0}:".format(config.modules_file))
        print_modules_list(config.modules)
        sys.exit(0)

    if options.show_bundles_list:
        print("Bundles defined in {0}:".format(config.config_file))
        print_bundles_list(config.bundles)
        sys.exit(0)

    if options.show_bundle_info:
        bundle = config.bundles.get(options.show_bundle_info)
        if bundle is not None:
            print("Bundle '{0}' defined in {1}:".format(
                options.show_bundle_info, config.config_file
            ))
            print_bundle_info(bundle)
        else:
            print("Bundle '{0}' is not found in {1}".format(
                options.show_bundle_info, config.config_file
            ))
        sys.exit(0)

    print("Config is OK: {0}".format(config.root_dir))
