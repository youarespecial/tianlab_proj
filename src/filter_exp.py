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


def gen_pmid2path(input_dir, tar_col_name='PMID', sep='\t', header=0, index_col=None):
    dic = {}
    dir_names = os.listdir(input_dir)
    for d_name in dir_names:
        dir_ = os.path.join(input_dir, d_name)
        if not os.path.isdir(dir_):
            continue
        cell_type_path = os.path.join(dir_, 'cell_type.txt')
        cell_meta_path = os.path.join(dir_, 'raw_count', 'cell_meta.txt')
        cell_exp_path = os.path.join(dir_, 'raw_count', 'cell_exp.txt')
        if not os.path.exists(cell_type_path):
            print('File not exists ', cell_type_path)
            continue
        if not os.path.exists(cell_meta_path):
            print('File not exists ', cell_meta_path)
            continue
        if not os.path.exists(cell_exp_path):
            print('File not exists ', cell_exp_path)
            continue
        if not os.path.exists(cell_type_path):
            print('File %s not found in %s'%(fname, dir_))
            continue
        df = pd.read_csv(cell_type_path, header=header, index_col=index_col, sep=sep)
        if tar_col_name not in df.columns:
            wprint('Col-name=%s not found in df.columns=%s for file=%s'%(tar_col_name, df.columns, cell_type_path))
            continue
        pmid_values = set(list(df[tar_col_name]))
        nrof_v = len(pmid_values)
        if not nrof_v:
            wprint('Col-name=%s is empty for file=%s'%(fname, cell_type_path))
            continue
        elif nrof_v:
            wprint('Col-name=%s has more than one values=%s in file=%s'%(fname, pmid_values, cell_type_path))
        pmid = str(pmid_values[0])

        if pmid not in dic:
            dic[pmid] = (cell_meta_path, cell_exp_path, cell_type_path)
        else:
            wprint('PMID=%s repeated in multipul directory, pls. check those directories: '%(pmid))
            wprint(os.path.split(dic[pmid][2])[0])
            wprint(dir_)
    return dic


def gen_pmid(df_in, df_meta, df_exp):
    df_out = None
    key_col_names = ['cell_type', 'pmid', 'location', 'CL_ID', 'CL_name', 'Relationship']
    for n in key_col_names:
        if n not in df_in.columns:
            wprint('col-name = %s not in df_human.columns=%s'%(n, df_in.columns))
            return df_out

    for idx, row in df_in.iterrows():
        cell_type = row['cell_type']
        pmid = row['pmid']
        location = row['location']
        cl_id = row['CL_ID']
        cl_name = row['CL_name']
        rela = row['Relationship']
        tar_ids = list(set(list(df_meta[df_meta['Cluster'] == cell_type])['ID']))
        nrof_id = len(tar_ids)
        if not nrof_id:
            wprint('No ID values found with cell_type=%s in df_meta=\n%s'%(cell_type, df.head()))
            continue
        tar_ids_clean = []
        for id_ in tar_ids:
            if id_ not in df_exp.columns:
                wprint('ID=%s not found in df_exp.columns=%s'%(id_, df_exp.columns))
                continue
            tar_ids_clean.append(id_)

        df_new = df_exp[tar_ids_clean]
        columns_new = ['|'.join([location, ]) for col in df_new.columns]
        df_new.columns = columns_new
        if df_out is None:
            df_out = df_new
        else:
            df_out = df_out.join(df_new)

    return df_out



def main(args):
    CHECK_EXIST(args.input, 'f')
    CHECK_EXIST(args.data_dir, 'd')
    
    MAKE_EXIST(args.output, 'd')

    pmid2path = gen_pmid2path(args.data_dir, sep=args.sep)
    nrof_pmid_db = len(pmid2path)
    print('Totally %d pmid in database=%s'%(nrof_pmid_db, args.data_dir))
    if not nrof_pmid_db:
        wprint('No pmid directory found in %s'%(args.data_dir))
        return
    df_human = pd.read_csv(args.input, header=0, index_col=None, sep=arg.sep)
    pmid_targets = []
    if not args.pmid_li:
        pmid_targets = pmid2path.keys()
        
    for pmid in pmid_targets:
        if pmid not in pmid2path:
            wprint('pmid=%s not found in %s'%(pmid, args.data_dir))
            continue
        cell_meta_path, cell_exp_path, cell_type_path = pmid2path[pmid]
        df_meta = pd.read_csv(cell_meta_path, header=0, index_col=None, sep=args.sep)
        df_exp = pd.read_csv(cell_exp_path, header=0, index_col=0, sep=args.sep)
        df_in = df_human[df_human['pmid'] == pmid]
        if not df_in.size:
            wprint('pmid=%s not found in %s with df_human.head=\n%s'%(pmid, args.input, df_human.head()))
            continue
        df_out = gen_pmid(df_in, df_meta, df_exp)
        if df_out is None:
            wprint('empty after filter cell_exp, for pmid=%s, cell_exp_path=%s'%(pmid, cell_exp_path))
        else:
            output_pmid_path = os.path.join(args.output, pmid + '.txt')
            write_csv(df_out, output_pmid_path, index=False)
    print('All done.')
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, 
        help='Input location file.')
    parser.add_argument('--data-dir', type=str, required=True, 
        help='Input directory.')
    parser.add_argument('--sep', default='\t',
        help='Sep')
    parser.add_argument('--key-name', default='Cell type', 
        help='Key name of cell-type file ')
    parser.add_argument('--pmid-li',  nargs='+', default=[],
        help='Zero or one or multiple pmid')
    parser.add_argument('-o', '--output', type=str, default='./output', 
        help='Directory to save cell meta file.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
