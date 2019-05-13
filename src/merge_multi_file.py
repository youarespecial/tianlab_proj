#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os
import sys
import glob
import numpy as np
import pandas as pd
import json
import argparse
from collections import defaultdict
import shutil

current_dir = os.path.dirname(__file__)

sys.path.append(os.path.join(current_dir, '.'))


from path_tools import *
from process_common import *


def main(args):
    CHECK_EXIST(args.input, 'd')
    
    MAKE_EXIST(args.output, 'f')

    if args.fnames:
        file_paths = []
        for name in args.fnames:
            path = os.path.join(args.input, name)
            if not os.path.exists(path):
                wprint('File not exists: ', path)
                continue
            file_paths.append(path)
    else:
        file_paths = glob.glob(os.path.join(args.input, "*." + args.file_ext))
    nrof_file = len(file_paths)
    print('Totally %5d input files'%(nrof_file))
    if not nrof_file:
        wprint('Warning: no file with extension=%s found in %s'%(args.file_ext, args.input))
        return

    df_merge = merge_multi(file_paths, header=0, index_col=0, sep=args.sep)
    write_csv(df_merge, args.output)
    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, 
        help='Directory of all files')
    parser.add_argument('--fnames',  nargs='+', default=[],
        help='key name of cell-type file ')
    parser.add_argument('--sep', default='\t',
        help='Sep of input files.')
    parser.add_argument('-o', '--output', default='./output/output.txt', 
        help='File path to save output.')
    parser.add_argument('--file-ext', default='csv',
        help='File extension')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
