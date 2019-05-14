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
    MAKE_EXIST(args.output, 'd')

    output_sum_path = os.path.join(args.output, 'exp_sum.txt')

    #### 1. read raw file
    df_raw = pd.read_csv(args.input, sep='\t', header=0, index_col=0)
    #### 2. create sum file
    df_sum = gen_sum(df_raw, splitter='|', from_start=False, sep='\t', header=0, index_col=0)
    write_csv(df_sum, output_sum_path)

    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, 
        help='Input raw file.')
    parser.add_argument('-o', '--output', default='./output', 
        help='Directory to save output.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
