# -*- coding: utf-8 -*-
"""Please directly install `%(module_name)s` instead."""

from __future__ import print_function, unicode_literals

import os
import warnings
import sys
from distutils.command.install import install

# version string
__version__ = '%(version)s'


class Install(install):
    """Magic install command."""

    def check_call(self, cmd):  # pylint: disable=no-self-use
        """Wrapper for functionality of `subprocess.check_call`."""
        return_code = os.system(cmd)
        if return_code != 0:
            raise OSError('[EXIT %%s] %%s' %% (return_code, cmd))

    def run(self):  # pylint: disable=no-self-use
        if %(raise_flag)s:
            raise RuntimeError('This is a dummy package for `%(module_name)s`. '
                               'Please directly install `%(module_name)s` instead.')
        else:
            print(u'This is a dummy package for `%(module_name)s`.', file=sys.stderr)
            print(u'Trying to reinstall...', file=sys.stderr)
            try:
                self.check_call('%%s -m pip install %(module_name)s' %% sys.executable)
            except OSError:
                print(u'Failed to reinstall...', file=sys.stderr)
                print(u'Please directly install `%(module_name)s` instead.', file=sys.stderr)
                raise
            print(u'Successfully reinstalled...', file=sys.stderr)


# setup attributes
attrs = dict(
    name='%(name)s',
    version=__version__,
    description='Dummy package for %(module_name)s.',
    long_description=__doc__,
    author='%(author)s',
    author_email='%(author_email)s',
    maintainer='%(maintainer)s',
    maintainer_email='%(maintainer_email)s',
    url='%(url)s',
    # download_url
    py_modules=['%(module)s'],
    # scripts
    # ext_modules
    classifiers=[
        'Development Status :: 7 - Inactive',
    ],
    # distclass
    # script_name
    # script_args
    # options
    license='The Unlicensed',
    keywords=[
        'dummy',
        '%(module)s',
        '%(module_name)s',
    ],
    platforms=[
        'any'
    ],
    cmdclass=dict(
        install=Install,
    ),
    # data_files
    # package_dir
    # obsoletes
    # provides
    # requires
    # command_packages
    # command_options
    package_data={
        '': [
            'LICENSE',
            'README.md',
        ],
    },
    # include_package_data
    # libraries
    # headers
    # ext_package
    # include_dirs
    # password
    # fullname
    # long_description_content_type
    # python_requires
    # zip_safe,
    # install_requires
)

try:
    from setuptools import setup

    attrs.update(dict(
        include_package_data=True,
        # libraries
        # headers
        # ext_package
        # include_dirs
        # password
        # fullname
        long_description_content_type='text/markdown',
        # python_requires
        zip_safe=True,
    ))
except ImportError:
    from distutils.core import setup

# set-up script for pip distribution
setup(**attrs)

# warn about the package
warnings.warn('This is a dummy package for `%(module_name)s`. '
              'Please directly install `%(module_name)s` instead.')
