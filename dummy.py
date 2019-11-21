# -*- coding: utf-8 -*-
"""Dummy package generator."""

import argparse
import base64
import json
import logging
import os
import re
import sys
import tarfile

# ConfigParser backport
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# JSON backport
try:
    import simplejson as json
    from simplejson import JSONDecodeError
except ImportError:
    try:
        from json import JSONDecodeError
    except ImportError:
        JSONDecodeError = ValueError

# YAML support
try:
    import yaml
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import SafeLoader as Loader
except ImportError:
    yaml = None

# template root
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'template')
if not os.path.isdir(ROOT):
    TEMPLATE_CTX = (
        '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'
        'CSWUUEIJfxP4H2ASOWoAUAAA'
    ).encode()

    file_name = '%s.tar.gz' % ROOT
    with open(file_name, 'wb') as tempfile:
        tempfile.write(base64.b64decode(TEMPLATE_CTX))

    with tarfile.open(file_name, 'r') as archive:
        archive.extractall(os.path.dirname(ROOT))
    os.remove(file_name)

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


# makedirs
def makedirs(name, mode=0o777, exist_ok=False):
    """makedirs(name [, mode=0o777][, exist_ok=False])

    Super-mkdir; create a leaf directory and all intermediate ones.  Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist. If the target directory already
    exists, raise an OSError if exist_ok is False. Otherwise no exception is
    raised.  This is recursive.

    """
    head, tail = os.path.split(name)
    if not tail:
        head, tail = os.path.split(head)
    if head and tail and not os.path.exists(head):
        try:
            makedirs(head, exist_ok=exist_ok)
        except FileExistsError:
            # Defeats race condition when another thread created the path
            pass
        cdir = os.curdir
        if isinstance(tail, bytes):
            cdir = bytes(os.curdir, 'ASCII')
        if tail == cdir:           # xxx/newdir/. exists if xxx/newdir exists
            return
    try:
        os.mkdir(name, mode)
    except OSError:
        # Cannot rely on checking for EEXIST, since the operating system
        # could give priority to other errors like EACCES or EROFS
        if not exist_ok or not os.path.isdir(name):
            raise


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
            if not self.flag_force:
                self.logger.error('package already exists: %s', name)
                return
            self.logger.warning('overwriting existing package: %s', name)
        makedirs(dest, exist_ok=True)

        # rendering context
        context = dict(
            name=name, version=version, url=url,
            module=module, module_name=module_name,
            author=author, author_email=author_email,
            maintainer=maintainer, maintainer_email=maintainer_email,
            raise_flag=self.flag_raise,
        )
        for key, val in context.items():
            self.logger.debug('[rendering context] %s: %s', key, val)

        def makefile(src, dst):  # pylint: disable=no-self-use
            """Copy and render file."""
            with open(src, 'r') as file:
                text = file.read() % context
            with open(dst, 'w') as file:
                file.write(text)

        # copy files
        for filename in os.listdir(ROOT):
            src = os.path.join(ROOT, filename)
            if filename == 'module.py':
                filename = '%s.py' % module
            dst = os.path.join(dest, filename)

            self.logger.debug('copying %s -> %s', src, dst)
            makefile(src, dst)

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

    def process_cfg(self, config):
        """Process parsed configuration."""
        for name, cfg in config.items():
            # skip default section of ConfigParser
            if name == configparser.DEFAULTSECT:
                continue

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

        # traverse config
        self.process_cfg(config)

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
                    self.logger.error('malformed configuration file: %s (content type is %s)',
                                      path, type(config).__name__)
                    continue

                # traverse config
                self.process_cfg(config)

    def process_json(self, path):
        """Process JSON format configuration file."""
        self.logger.info('processing JSON configuration file: %s', path)
        if not os.path.isfile(path):
            self.logger.error('file not found: %s', path)
            return

        with open(path) as file:
            try:
                config = json.load(file)
            except JSONDecodeError as error:  # pylint: disable=overlapping-except
                self.logger.error('malformed configuration file: %s (%s)', path, error)
                return

        if not isinstance(config, dict):
            self.logger.error('malformed configuration file: %s (content type is %s)', path, type(config).__name__)
            return

        # traverse config
        self.process_cfg(config)

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
        parser.add_argument('-r', '--raise', action='store_true', dest='raise_error',
                            help='raise error at runtime instead of reinstall')
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
        makedirs(self.dest, exist_ok=True)

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
        self.flag_force = self.args.force
        self.flag_raise = self.args.raise_error

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
