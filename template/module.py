# -*- coding: utf-8 -*-
"""Dummy package for `%(module_name)s`."""

from __future__ import print_function, unicode_literals

import os
import sys
import warnings

if %(raise_flag)s:
    raise RuntimeError(u'This is a dummy package for `%(module_name)s`. '
                       u'Please directly install `%(module_name)s` instead.')
else:
    # warn about the package
    warnings.warn('This is a dummy package for `%(module_name)s`. '
                  'Please directly install `%(module_name)s` instead.', RuntimeWarning)

    def check_call(cmd):
        """Wrapper for functionality of `subprocess.check_call`."""
        return_code = os.system(cmd)
        if return_code != 0:
            raise OSError('[EXIT %%s] %%s' %% (return_code, cmd))

    # try to reinstall
    print(u'This is a dummy package for `%(module_name)s`.', file=sys.stderr)
    print(u'Trying to reinstall...', file=sys.stderr)
    try:
        check_call('%%s -m pip uninstall -y %(name)s' %% sys.executable)
        check_call('%%s -m pip install %(module_name)s' %% sys.executable)
    except OSError:
        print(u'Failed to reinstall...', file=sys.stderr)
        print(u'Please uninstall `%(name)s` and directly install `%(module_name)s` instead.', file=sys.stderr)
        raise
    print(u'Successfully reinstalled...', file=sys.stderr)

    # try to restart
    print(u'Trying to restart your program...', file=sys.stderr)
    try:
        os.execlp(sys.argv[0], *sys.argv)
    except BaseException:
        print(u'Failed to restart your program...', file=sys.stderr)
        print(u'Please manually restart `%%s`.' %% ' '.join(sys.argv), file=sys.stderr)
        raise
