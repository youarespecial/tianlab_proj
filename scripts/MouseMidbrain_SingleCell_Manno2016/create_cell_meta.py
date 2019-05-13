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
    
    MAKE_EXIST(args.output, 'd')

    output_path = os.path.join(args.output, 'cell_meta.txt')
    df_meta = parse_meta(args.input, cell_id_row_idx=3, cell_type_row_idx=4, sep=',')
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
