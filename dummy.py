# -*- coding: utf-8 -*-
"""Dummy package generator."""

import argparse
import configparser
import json
import logging
import os
import re
import sys

# YAML support
try:
    import yaml
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
except ImportError:
    yaml = None

# template root
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'template')

# default version
VERSION = os.environ.get('DEFAULT_VERSION', '0.0.1.dev0')

# verbosity table
VERBOSITY = {
    logging.CRITICAL: 'CRITICAL',
    logging.ERROR: 'ERROR',
    logging.WARNING: 'WARNING',
    logging.INFO: 'INFO',
    logging.DEBUG: 'DEBUG',
}


class Dummy:
    """Dummy package generator."""

    @property
    def return_code(self):
        return 0

    def generate(self, name, version, url, module, module_name,
                 author, author_email, maintainer, maintainer_email):
        """Generate dummy package."""
        self.logger.info('generating dummy package: %s', name)

        dest = os.path.join(self.dest, name)
        if os.path.isdir(dest):
            if not self.force:
                self.logger.error('package already exists: %s', name)
                return
            self.logger.warning('overwriting existing package: %s', name)
        os.makedirs(dest, exist_ok=True)

        # rendering context
        context = dict(
            name=name, version=version, url=url,
            module=module, module_name=module_name,
            author=author, author_email=author_email,
            maintainer=maintainer, maintainer_email=maintainer_email
        )
        for key, val in context.items():
            self.logger.debug('[rendering context] %s: %s', key, val)

        def makefile(filename):  # pylint: disable=no-self-use
            """Copy and render file."""
            src = os.path.join(ROOT, filename)
            with open(src, 'r') as file:
                text = file.read() % context

            if filename == 'module.py':
                filename = '%s.py' % module

            dst = os.path.join(dest, filename)
            with open(dst, 'w') as file:
                file.write(text)
            self.logger.debug('copying %s -> %s', src, dst)

        # copy files
        for path in os.listdir(ROOT):
            makefile(path)
        self.logger.info('generated dummy package: %s', name)

    def getkey(self, config, name, default=None):
        """Get option from configuration file."""
        option = config.get(name, default)
        if option is None:
            self.parser.error('the following key is required: %s' % name)
        return option

    def getopt(self, name):
        """Get option string of name."""
        for action in self.parser._actions:  # pylint: disable=protected-access
            if name == action.dest:
                return tuple(action.option_strings)
        self.logger.critical('option not found: %s', name)
        return '(null)', '(null)'

    def getarg(self, name, default=None):
        """Get option from parsed namespace."""
        option = getattr(self.args, name, default)
        if option is None:
            self.parser.error('the following arguments are required: %s/%s' % self.getopt(name))
        return option

    def process_ini(self, path):
        """Process INI format configuration file."""
        self.logger.info('processing INI configuration file: %s', path)
        if not os.path.isfile(path):
            self.logger.error('file not found: %s', path)
            return

        # setup config parser
        config = configparser.ConfigParser(allow_no_value=True,
                                           inline_comment_prefixes=(';',),
                                           interpolation=configparser.ExtendedInterpolation())
        config.SECTCRE = re.compile(r'\[\s*(?P<header>[^]]+?)\s*\]')

        with open(path) as file:
            try:
                config.read_file(file)
            except configparser.Error as error:
                self.logger.error('malformed configuration file: %s (%s)', path, error)
                return
        config.remove_section('DEFAULT')

        for name, cfg in config.items():
            module = self.getkey(cfg, 'module', default=name)
            module_name = self.getkey(cfg, 'module-name')
            version = self.getkey(cfg, 'version', default=VERSION)
            author = self.getkey(cfg, 'author')
            author_email = self.getkey(cfg, 'author-email')
            maintainer = self.getkey(cfg, 'maintainer', default=author)
            maintainer_email = self.getkey(cfg, 'maintainer-email', default=author_email)
            url = self.getkey(cfg, 'url')

            # generate files
            self.generate(name=name, version=version, url=url,
                          module=module, module_name=module_name,
                          author=author, author_email=author_email,
                          maintainer=maintainer, maintainer_email=maintainer_email)
        self._processed = True

    def process_yaml(self, path):
        """Process YAML format configuration file."""
        self.logger.info('processing YAML configuration file: %s', path)
        if not os.path.isfile(path):
            self.logger.error('file not found: %s', path)
            return

        with open(path) as file:
            try:
                documents = yaml.load_all(file, Loader=Loader)
            except yaml.YAMLError as error:
                self.logger.error('malformed configuration file: %s (%s)', path, error)
                return

        for config in documents:
            if not isinstance(config, dict):
                self.logger.error('malformed configuration file: %s (content type is %s)', path, type(config).__name__)
                continue

            for name, cfg in config.items():
                module = self.getkey(cfg, 'module', default=name)
                module_name = self.getkey(cfg, 'module-name')
                version = self.getkey(cfg, 'version', default=VERSION)
                author = self.getkey(cfg, 'author')
                author_email = self.getkey(cfg, 'author-email')
                maintainer = self.getkey(cfg, 'maintainer', default=author)
                maintainer_email = self.getkey(cfg, 'maintainer-email', default=author_email)
                url = self.getkey(cfg, 'url')

                # generate files
                self.generate(name=name, version=version, url=url,
                              module=module, module_name=module_name,
                              author=author, author_email=author_email,
                              maintainer=maintainer, maintainer_email=maintainer_email)
        self._processed = True

    def process_json(self, path):
        """Process JSON format configuration file."""
        self.logger.info('processing JSON configuration file: %s', path)
        if not os.path.isfile(path):
            self.logger.error('file not found: %s', path)
            return

        with open(path) as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError as error:
                self.logger.error('malformed configuration file: %s (%s)', path, error)
                return

        if not isinstance(config, dict):
            self.logger.error('malformed configuration file: %s (content type is %s)', path, type(config).__name__)
            return

        for name, cfg in config.items():
            module = self.getkey(cfg, 'module', default=name)
            module_name = self.getkey(cfg, 'module-name')
            version = self.getkey(cfg, 'version', default=VERSION)
            author = self.getkey(cfg, 'author')
            author_email = self.getkey(cfg, 'author-email')
            maintainer = self.getkey(cfg, 'maintainer', default=author)
            maintainer_email = self.getkey(cfg, 'maintainer-email', default=author_email)
            url = self.getkey(cfg, 'url')

            # generate files
            self.generate(name=name, version=version, url=url,
                          module=module, module_name=module_name,
                          author=author, author_email=author_email,
                          maintainer=maintainer, maintainer_email=maintainer_email)
        self._processed = True

    def process_file(self, path, format):  # pylint: disable=inconsistent-return-statements, redefined-builtin
        """Process configuration file."""
        if format == 'json':
            return self.process_json(path)
        if format == 'yaml':
            return self.process_yaml(path)
        if format == 'ini':
            return self.process_ini(path)
        self.logger.critical('unrecognized format: %s', format)

    def process_args(self):
        """Check option arguments."""
        name = self.getarg('name')
        module = self.getarg('module', default=name)
        module_name = self.getarg('module_name')
        version = self.getarg('version', default=VERSION)
        author = self.getarg('author')
        author_email = self.getarg('author_email')
        maintainer = self.getarg('maintainer', default=author)
        maintainer_email = self.getarg('maintainer_email', default=author_email)
        url = self.getarg('url')

        # generate files
        self.generate(name=name, version=version, url=url,
                      module=module, module_name=module_name,
                      author=author, author_email=author_email,
                      maintainer=maintainer, maintainer_email=maintainer_email)

    def get_parser(self):  # pylint: disable=no-self-use
        """Get argument parser."""
        parser = argparse.ArgumentParser(prog='dummy',
                                         description='dummy package generator')

        parser.add_argument('-o', '--output', default='packages', help='output folder')
        parser.add_argument('-f', '--force', action='store_true', help='force generation even if package exists')
        parser.add_argument('-v', '--verbose', default=0, action='count', help='give more output; option is additive')

        file_group = parser.add_argument_group(title='File configuration',
                                               description='use configuration file to setup dummy package')
        file_group.add_argument('-j', '--json', action='append', help='path to JSON format configuration file')
        if yaml is not None:
            file_group.add_argument('-y', '--yaml', action='append', help='path to YAML format configuration file')
        file_group.add_argument('-i', '--ini', action='append', help='path to INI format configuration file')

        opts_group = parser.add_argument_group(title='Command configuration',
                                               description='use command line options to setup dummy package')
        opts_group.add_argument('-n', '--name', help='dummy package name')
        opts_group.add_argument('-m', '--module', help='package module name')
        opts_group.add_argument('-M', '--module-name', help='expected module name')
        opts_group.add_argument('-V', '--version', help='package version string')
        opts_group.add_argument('-a', '--author', help='author name')
        opts_group.add_argument('-A', '--author-email', help='author email')
        opts_group.add_argument('-t', '--maintainer', help='maintainer name')
        opts_group.add_argument('-T', '--maintainer-email', help='maintainer email')
        opts_group.add_argument('-u', '--url', help='project URL')

        return parser

    def get_logger(self):  # pylint: disable=no-self-use
        """Get logger."""
        # create logger
        logger = logging.getLogger('dummy')
        #logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt=r'%Y/%m/%d %H:%M:%S')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        return logger

    def __init__(self):
        """Entry point."""
        self._processed = False

        self.logger = self.get_logger()
        self.parser = self.get_parser()
        self.args = self.parser.parse_args()

        # output folder
        self.dest = os.path.realpath(self.args.output)
        os.makedirs(self.dest, exist_ok=True)

        # logging verbosity
        verbosity = (4 - self.args.verbose) * 10 - 1
        self.logger.setLevel(verbosity)
        for number in range(5):
            level = number * 10
            if verbosity <= level:
                name = VERBOSITY.get(level, 'UNSET')
                self.logger.debug('setting logger level to %s', name)
                break

        # flags
        self.force = self.args.force

        # runtime arguments
        for key, val in self.args._get_kwargs():  # pylint: disable=protected-access
            self.logger.debug('[runtime arguments] %s: %s', key, val)

        # check file arguments
        for name in ('json', 'yaml', 'ini'):
            option = getattr(self.args, name, None)
            if option is not None:
                for path in option:
                    self.process_file(path=path, format=name)

        # check option arguments
        if not self._processed:
            self.process_args()


if __name__ == "__main__":
    sys.exit(Dummy().return_code)
