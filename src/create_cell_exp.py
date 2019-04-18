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


def gen_meta_map_dic():
    pass

def main(args):
    CHECK_EXIST(args.input, 'f')
    CHECK_EXIST(args.cell_meta, 'f')
    
    MAKE_EXIST(args.output, 'd')

    output_path = os.path.join(args.output, 'cell_exp.txt')
    
    df_meta = pd.read_csv(args.cell_meta, sep='\t', header=0, index_col=None)

    df_exp = gen_exp(args.input, df_meta, sep='\t', header=0, index_col=0, col_id_name='ID', col_cluster_name='Cluster')
    # print(df_exp.head())
    # print(df_exp.describe())
    write_csv(df_exp, output_path, index=True)

    prepend_to_file(output_path, 'Gene')
    
    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, 
        help='Input matrix file.')
    parser.add_argument('--cell-meta', type=str, required=True, 
        help='Input cell meta file.')
    parser.add_argument('-o', '--output', type=str, default='./output', 
        help='Directory to save cell meta file.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
