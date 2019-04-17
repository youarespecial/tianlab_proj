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

sys.path.append(os.path.join(current_dir, '..'))
sys.path.append(os.path.join(current_dir, '..', '..', 'src'))

from path_tools import *
from process_common import *


def gen_meta_map_dic(celltype_names, anno_names, sep=' '):
    dic = {}
    
    pre = 'pre-'
    pro = 'progenitor '
    unmatched_names = set()
    for x in anno_names:
        if x in dic:
            continue
        sp = x.split(sep)
        nrof_sp = len(sp)
        if nrof_sp == 1:
            if pre in x:
                x_key = x.replace(pre, pro)
            else:
                raise ValueError('x=%s , split by "%s" is %s, which has no %s'%(x, sep, sp, pre))
        elif nrof_sp == 2:
            x_key = sp[0]
        else:
            raise ValueError('x=%s , split by "%s" is %s, length=%s != 2'%(x, sep, sp, nrof_sp))
        matched_name = None
        for cell_name in celltype_names:
            if x_key in cell_name:
                matched_name = cell_name
                break

        if matched_name is None:
            if x not in unmatched_names:
                unmatched_names.add(x)
                wprint('No matched name for x=%s in celltype_names=%s'%(x, celltype_names))
        else:
            dic[x] = matched_name

    return dic


def main(args):
    CHECK_EXIST(args.input, typ='d')
    output_exp_path = os.path.join(args.output, 'cell_exp.txt')
    output_meta_path = os.path.join(args.output, 'cell_meta.txt')
    output_raw_path = os.path.join(args.output, 'exp_raw.txt')
    output_sum_path = os.path.join(args.output, 'exp_sum.txt')
    MAKE_EXIST(output_exp_path, 'f')


    #### 1. create meta file
    celltype_map = read_celltype(args.cell_type, key_name='Raw_Column', sep='\t', header=0, index_col=None)
    celltype_names = list(set(celltype_map.keys()))
    df_anno = pd.read_csv(args.anno_all, header=0, index_col=None, sep=',')
    anno_names = list(df_anno['celltype'])
    
    meta_map_dic = gen_meta_map_dic(celltype_names, anno_names, sep=' ')

    df_meta = gen_meta(df_anno, meta_map_dic, columns=['ID', 'Cluster'], id_col_idx=0, cluster_col_idx=1)
    write_csv(df_meta, output_meta_path, index=False)

    #### 2. create exp file
    df_mat = merge_multi(args.input, match_rule='*_EB-*.csv', header=0, index_col=0, sep=',')
    ## matrix_path = os.path.join(args.output, 'matrix.txt')
    ## df_mat = pd.read_csv(matrix_path, sep='\t', header=0, index_col=0)

    df_exp = gen_exp(df_mat, df_meta, col_id_name='ID', col_cluster_name='Cluster')
    write_csv(df_exp, output_exp_path)
    prepend_to_file(output_exp_path, 'Gene') ## add Gene to head

    #### 3. create raw file
    raw_map_dic = gen_raw_map_dic(df_meta, celltype_map, fname=None)
    df_raw = gen_raw(df_mat, raw_map_dic)
    write_csv(df_raw, output_raw_path)

    #### 4. create sum file
    df_sum = gen_sum(df_raw, splitter='|', from_start=False, sep='\t', header=0, index_col=0)
    write_csv(df_sum, output_sum_path)

    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, 
        help='xxx')
    parser.add_argument('--cell-type', type=str, required=True, 
        help='xxx')
    parser.add_argument('--anno-all', type=str, required=True, 
        help='xxx')
    parser.add_argument('-o', '--output', type=str, default='./output', 
        help='xxx')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
