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
sys.path.append(os.path.join(current_dir, '..', '..', 'src'))


from path_tools import *
from process_common import *


def main(args):
    CHECK_EXIST(args.input, 'f')
    CHECK_EXIST(args.cell_typ, 'f')
    
    MAKE_EXIST(args.output, 'd')

    output_path = os.path.join(args.output, 'cell_meta.txt')
    df_input = pd.read_csv(args.input, header=0, index_col=0, sep='\t')

    celltype_map = read_celltype(args.cell_typ, key_name=args.key_name, sep='\t', header=0, index_col=None)
    celltype_names = set(celltype_map.keys())
    li = []
    for id_ in df_input.columns:
        if 'DENV' in id_:
            continue
        matched = None
        for cluster in celltype_names:
            if cluster in id_:
                matched = cluster
                break
        if matched is None:
            wprint('No match cluster found for ID=%s in Cluster=%s'%(id_, celltype_names))
            continue
        li.append([id_, matched])

    df_meta = pd.DataFrame(li, columns=['ID', 'Cluster'], index=None)
    # print(df_meta.head())
    # print(df_meta.describe())
    write_csv(df_meta, output_path, index=False)

    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, 
        help='Input cell annotation file.')
    parser.add_argument('--cell-typ', type=str, required=True, 
        help='Input cell type file.')
    parser.add_argument('--key-name', default='Cell_type', 
        help='Key name of cell-type file ')
    parser.add_argument('-o', '--output', type=str, default='./output', 
        help='Directory to save cell meta file.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
