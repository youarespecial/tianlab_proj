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



def read_meta(file_in, cell_id_row_idx=3, cell_type_row_idx=4, sep='\t'):
    cell_type_row, cell_id_row = '', ''
    with open(file_in, 'r') as reader:
        for idx, line in enumerate(reader, start=1):
            if idx == cell_type_row_idx:
                cell_type_row = line.split('Cell_type')[1].strip().split(sep)
            if idx == cell_id_row_idx:
                cell_id_row = line.split('Cell_ID')[1].strip().split(sep)
            if cell_id_row and cell_type_row:
                break
    columns=['ID', 'Cluster']
    arr = np.array([cell_id_row, cell_type_row]).T
    df = pd.DataFrame(arr, columns=columns)
    return df


def main(args):
    CHECK_EXIST(args.input, 'f')
    
    MAKE_EXIST(args.output, 'd')

    output_path = os.path.join(args.output, 'cell_meta.txt')

    df_meta = read_meta(args.input)
    ### df_meta = parse_meta(args.input, cell_id_row_idx=3, cell_type_row_idx=4, sep=',')
    # print(df_meta.head())
    # print(df_meta.describe())
    write_csv(df_meta, output_path, index=False)

    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, 
        help='Input cell annotation file.')
    parser.add_argument('-o', '--output', type=str, default='./output', 
        help='Directory to save cell meta file.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
