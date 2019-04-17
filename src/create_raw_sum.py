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
    CHECK_EXIST(args.input, 'f')
    CHECK_EXIST(args.cell_meta, 'f')
    CHECK_EXIST(args.cell_typ, 'f')
    
    MAKE_EXIST(args.output, 'd')

    output_raw_path = os.path.join(args.output, 'exp_raw.txt')
    output_sum_path = os.path.join(args.output, 'exp_sum.txt')


    #### 1. create raw file
    celltype_map = read_celltype(args.cell_typ, key_name=args.key_name, index_col=None)
    df_meta = pd.read_csv(args.cell_meta, sep='\t', header=0, index_col=None)
    fname = os.path.split(args.input)[-1]
    # fname = None
    raw_map_dic = gen_raw_map_dic(df_meta, celltype_map, fname)
    df_raw = gen_raw(args.input, raw_map_dic, sep='\t', header=0, index_col=0)

    write_csv(df_raw, output_raw_path)

    #### 2. create sum file
    df_sum = gen_sum(df_raw, splitter='|', from_start=False, sep='\t', header=0, index_col=0)
    write_csv(df_sum, output_sum_path)

    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, 
        help='xxx')
    parser.add_argument('--cell-meta',default='', 
        help='xxx')
    parser.add_argument('--cell-typ',default='', 
        help='xxx')
    parser.add_argument('--key-name', default='Cell type', 
        help='key name of cell-type file ')
    parser.add_argument('-o', '--output', default='./output', 
        help='xxx')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
