# -*- coding: utf-8 -*-
"""Dummy package generator."""

# version string
__version__ = '0.1.0'

with open('README.md') as file:
    long_description = file.read()

# setup attributes
attrs = dict(
    name='python-dummy',
    version=__version__,
    description=__doc__,
    long_description=long_description,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    maintainer='Jarry Shaw',
    maintainer_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/pypi',
    download_url='https://github.com/JarryShaw/pypi/archive/v%s.tar.gz' % __version__,
    py_modules=['dummy'],
    # scripts
    # ext_modules
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    # distclass
    # script_name
    # script_args
    # options
    license='MIT License',
    keywords=[
        'dummy',
    ],
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
        'template': ['*'],
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
    install_requires=[
        # 'ConfigUpdater',
        'PyYAML',
        'simplejson',
    ],
    entry_points={
        'console_scripts': [
            'dummy = dummy:main',
        ]
    },
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
        # zip_safe
    ))
except ImportError:
    from distutils.core import setup

# set-up script for pip distribution
setup(**attrs)
