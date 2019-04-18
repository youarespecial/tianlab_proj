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
    CHECK_EXIST(args.anno, 'f')
    CHECK_EXIST(args.cell_typ, 'f')
    
    MAKE_EXIST(args.output, 'd')

    output_path = os.path.join(args.output, 'cell_meta.txt')
    celltype_map = read_celltype(args.cell_typ, key_name=args.key_name, sep='\t', header=0, index_col=None)
    celltype_names = list(set(celltype_map.keys()))
    df_anno = pd.read_csv(args.anno, header=0, index_col=None, sep=',')
    anno_names = list(df_anno['celltype'])
    
    meta_map_dic = gen_meta_map_dic(celltype_names, anno_names, sep=' ')
    df_meta = gen_meta(df_anno, meta_map_dic, columns=['ID', 'Cluster'], id_col_idx=0, cluster_col_idx=1)
    # print(df_meta.head())
    # print(df_meta.describe())
    write_csv(df_meta, output_path, index=False)

    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--anno', type=str, required=True, 
        help='Input cell annotation file.')
    parser.add_argument('--cell-typ', type=str, required=True, 
        help='Input cell type file.')
    parser.add_argument('--key-name', default='Cell type', 
        help='Key name of cell-type file ')
    parser.add_argument('-o', '--output', type=str, default='./output', 
        help='Directory to save cell meta file.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
