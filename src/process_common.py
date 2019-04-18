#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import shutil
import argparse 
import pandas as pd
import numpy as np
from collections import defaultdict

current_dir = os.path.dirname(__file__)

sys.path.append(os.path.join(current_dir, '.'))
sys.path.append(os.path.join(current_dir, '../src'))

from path_tools import *


def read_celltype(csv_path, key_name='Raw_colnm', value_names=['Dir', 'CL_ID'], sep='\t', header=0, index_col=None):
    df = pd.read_csv(csv_path, header=header, sep=sep, index_col=index_col)
    columns = list(df.columns)
    for name in [key_name] + value_names:
        if name not in columns:
            raise ValueError('name=%s not in columns=%s'%(name, columns))
    map_dic = {}
    for idx, row in df.iterrows():
        key = row[key_name]
        values = [row[n] for n in value_names]
        if key not in map_dic:
            map_dic[key] = values
        else:
            info = get_cur_info()
            wprint(info + 'key_name=%s has repeated value=%s'%(key_name, key))
    return map_dic


def gen_meta(input_, map_dic, sep='\t', header=0, index_col=None, columns=['ID', 'Cluster'], id_col_idx=0, cluster_col_idx=1):
    if isinstance(input_, str):
        df_in = pd.read_csv(input_, sep=sep, header=header, index_col=index_col)
    elif isinstance(input_, pd.DataFrame):
        df_in = input_
    else:
        raise ValueError('input_ type wrong %s'%(type(input_)))
    nrof_col = len(df_in.columns)
    if nrof_col != 2:
        info = get_cur_info()
        wprint(info + 'input_ has columns=%s, number is %d != 2'%(df_in.columns, nrof_col))

    col_id_name = df_in.columns[id_col_idx]
    col_cluster_name = df_in.columns[cluster_col_idx]

    li_out = []
    for idx, row in df_in.iterrows():
        v_id = row[col_id_name]
        v_cls = row[col_cluster_name]
        if v_cls in map_dic:
            v_cls_new = map_dic[v_cls]
            li_out.append([v_id, v_cls_new])
        else:
            info = get_cur_info()
            wprint(info + ' skipp annot row with id=%s, cluster=%s'%(v_id, v_cls))
    df_out = pd.DataFrame(li_out, columns=columns, index=None)
    return df_out


def gen_exp(input_, df_meta, sep='\t', header=0, index_col=0, col_id_name='ID', col_cluster_name='Cluster'):
    if isinstance(input_, str):
        df_in = pd.read_csv(input_, sep=sep, header=header, index_col=index_col)
    elif isinstance(input_, pd.DataFrame):
        df_in = input_
    else:
        raise ValueError('input_ type wrong %s'%(type(input_)))
    for x in [col_id_name, col_cluster_name]:
        if x not in list(df_meta.columns):
            raise ValueError('col-name=%s not in %s'%(x, df_meta.columns))
    col_li = []
    columns = []
    columns_in = set(list(df_in.columns))
    unmatched_names = set()
    matched_names = set()
    for idx, row in df_meta.iterrows():
        id_ = row[col_id_name]
        if id_ not in columns_in:
            unmatched_names.add(id_)
            info = get_cur_info()
            # wprint(info + 'col-name=%s not in %s'%(id_, columns_in))
            continue
        matched_names.add(id_)
        cluster = row[col_cluster_name]
        columns.append(cluster)
        col_li.append(df_in[id_])
    # print('unmatched_names/all %5d/%5d'%(len(unmatched_names), len(unmatched_names) + len(matched_names)))
    # print('matched_names/all columns %5d/%5d'%(len(matched_names), len(df_in.columns)))
    df_out = pd.concat(col_li, axis=1)
    df_out.index = df_in.index
    df_out.columns = columns
    
    return df_out


def gen_raw(input_, col_name_map, sep='\t', header=0, index_col=0):
    if isinstance(input_, str):
        df_in = pd.read_csv(input_, sep=sep, header=header, index_col=index_col)
    elif isinstance(input_, pd.DataFrame):
        df_in = input_
    else:
        raise ValueError('input_ type wrong %s'%(type(input_)))

    dic = {}
    for col_name, name_li in col_name_map.items():
        col_values = None
        for name in name_li:
            if name not in df_in.columns:
                info = get_cur_info()
                wprint( info + 'col-name = %s not in %s'%(name, df_in.columns))
                continue
            values = np.array(list(df_in[name])).astype(np.int32)
            if col_values is None:
                col_values = values
            else:
                col_values += values
        if col_values is not None:
            dic[col_name] = list(col_values)
        else:
            info = get_cur_info()
            wprint(info + 'No col_values found for col_name=%s'%(col_name))

    df_out = pd.DataFrame(dic, index=df_in.index)
    return df_out


def gen_sum(input_, splitter='|', from_start=False, sep='\t', header=0, index_col=0):
    if isinstance(input_, str):
        df_in = pd.read_csv(input_, sep=sep, header=header, index_col=index_col)
    elif isinstance(input_, pd.DataFrame):
        df_in = input_
    else:
        raise ValueError('input_ type wrong %s'%(type(input_)))

    columns = df_in.columns
    
    if from_start:
        columns_new = list(set([n.split(splitter)[0] for n in columns]))
    else:
        columns_new = list(set([n.split(splitter)[-1] for n in columns]))
    li_out = []
    columns_final = []
    for name in columns_new:
        split_names = [i for i in columns if i.endswith(name)][0].split(splitter)
        dir_ = split_names[0]
        # cl_id = split_names[-1] ### == name
        if from_start:
            target_cols = np.asarray([list(df_in[i]) for i in columns if i.startswith(name)]).astype(np.int32)
        else:
            target_cols = np.asarray([list(df_in[i]) for i in columns if i.endswith(name)]).astype(np.int32)
        target_sum = list(target_cols.sum(axis=0))
        li_out.append(target_sum)
        columns_final.append('%s%s%s'%(dir_, splitter, name))
    np_out = np.asarray(li_out).T
    df_out = pd.DataFrame(np_out, columns=columns_final, index=df_in.index)
    return df_out


def merge_multi(file_paths, header=0, index_col=0, sep='\t'):
    nrof_file = len(file_paths)
    df_out = None
    for p in file_paths:
        df = pd.read_csv(p, header=header, index_col=index_col, sep=sep)
        if df_out is None:
            df_out = df
        else:
            df_out = df_out.join(df) 
    return df_out


def write_csv(df, file, sep='\t', index=True, header=True, verbose=True):
    MAKE_EXIST(file, 'f')
    df.to_csv(file, sep=sep, header=header, index=index)
    if verbose:
        print('Saving to ', file)


def prepend_to_file(file_path, content):
    with open(file_path, "r+") as f:
        old = f.read()
        f.seek(0)
        f.write(content)
        f.write(old)


def gen_raw_map_dic(df_meta, celltype_map, fname=None):
    dic = {}
    for idx, row in df_meta.iterrows():
        col_name = row['ID']
        cluster = row['Cluster']
        if not cluster in celltype_map:
            info = get_cur_info()
            wprint( info + 'celltype=%s not in celltype_map.keys=%s'%(cluster, celltype_map.keys()))
            continue
        dir_, cl_id = celltype_map[cluster]
        if fname is None:
            li = [dir_, cluster, cl_id]
        else:
            li = [dir_, fname, cluster, cl_id]
        new_name = '|'.join(li)
        if not new_name in dic:
            dic[new_name] = []
        dic[new_name].append(col_name)
    return dic


def parse_meta(file_in, cell_id_row_idx=3, cell_type_row_idx=4, sep=','):
    
    def func_split(x, cont):
        return x.strip().strip(sep).lstrip(cont).strip().strip(sep).split(sep)
    
    row_id, row_typ = [], []

    with open(file_in, 'r') as reader:
        for idx, line in enumerate(reader, start=1):
            if idx == cell_type_row_idx:
                row_typ = func_split(line, 'Cell_type')
            if idx == cell_id_row_idx:
                row_id = func_split(line, 'CELL_ID')
            if row_id and row_typ:
                break
    if not row_id:
        raise ValueError('Parsed empty ID col')

    if not row_typ:
        raise ValueError('Parsed empty Cluster col')

    nrof_id, nrof_typ = len(row_id), len(row_typ)
    if nrof_id != nrof_typ:
        raise ValueError('Parsed ID and Cluster value number %s != %s\n ID=%s\nCluster=%s'%(nrof_id, 
            nrof_typ, row_id, row_typ))

    s_id = pd.Series(row_id, name='ID', index=None)
    s_cls = pd.Series(row_typ, name='Cluster', index=None)
    df = pd.concat([s_id, s_cls], axis=1)
    return df