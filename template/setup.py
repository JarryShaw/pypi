# -*- coding: utf-8 -*-
"""Please directly install `{{ module_name }}` instead."""

# version string
__version__ = '{{ version }}'

# setup attributes
attrs = dict(
    name='{{ name }}',
    version=__version__,
    description='Dummy package for {{ module_name }}.',
    long_description=__doc__,
    author='{{ author }}',
    author_email='{{ author_email }}',
    maintainer='{{ maintainer }}',
    maintainer_email='{{ maintainer_email }}',
    url='{{ url }}',
    # download_url
    py_modules=['{{ module }}'],
    # scripts
    # ext_modules
    classifiers=[
        'Development Status :: 7 - Inactive',
    ],
    # distclass
    # script_name
    # script_args
    # options
    license='{{ license }}',
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
