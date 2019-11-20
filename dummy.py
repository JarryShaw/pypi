# -*- coding: utf-8 -*-

import argparse


def get_parser():
    """Get argument parser."""
    parser = argparse.ArgumentParser(prog='dummy',
                                     description='dummy package generator')
    parser.add_argument('-n', '--name', help='dummy package name')
