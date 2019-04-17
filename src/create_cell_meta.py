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
    CHECK_EXIST(args.anno, 'f')
    CHECK_EXIST(args.celltype, 'f')
    
    MAKE_EXIST(args.output, 'd')

    output_path = os.path.join(args.output, 'cell_meta.txt')
    
    celltype_map = read_celltype(args.celltype, key_name=args.key_name, index_col=None)
    df_anno = pd.read_csv(args.anno, sep='\t', header=0, index_col=None)
    meta_map_dic = gen_meta_map_dic()
    df_meta = gen_meta(df_anno, meta_map_dic, columns=['ID', 'Cluster'], id_col_idx=0, cluster_col_idx=1)
    # print(df_meta.head())
    # print(df_meta.describe())
    write_csv(df_meta, output_path, index=False)

    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--anno', type=str, required=True, 
        help='Input cell annotation file.')
    parser.add_argument('--celltype', type=str, required=True, 
        help='Input cell type file.')
    parser.add_argument('--key-name', default='Raw_colnm', 
        help='Key name of cell-type file ')
    parser.add_argument('-o', '--output', type=str, default='./output', 
        help='Directory to save cell meta file.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
