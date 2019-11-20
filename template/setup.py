# -*- coding: utf-8 -*-
"""Please directly install `%(module_name)s` instead."""

import warnings

# warn about the package
warnings.warn('This is a dummy package for `%(module_name)s`. '
              'Please directly install `%(module_name)s` instead.')

# version string
__version__ = '%(version)s'

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
    # keywords
    platforms=[
        'any'
    ],
    # cmdclass
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
        #python_requires
        zip_safe=True,
    ))
except ImportError:
    from distutils.core import setup

# set-up script for pip distribution
setup(**attrs)
