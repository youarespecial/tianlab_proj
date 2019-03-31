#!/usr/bin/python3
### python 3.5
# -*- coding: utf-8 -*-

import sys
import argparse 
import os
import pandas as pd
import numpy as np
from collections import defaultdict

def read_celltype(csv_path, key_name='Raw_colnm', sep='\t'):
    df = pd.read_csv(csv_path, header=0, sep=sep, index_col=None)
    #df = pd.DataFrame(li[1:], columns=li[0], index=None)
    columns = list(df.columns)
    print(columns)
    print(df.head())
    map_dic = {}
    for idx, row in df.iterrows():
        raw_colnm = row[key_name]
        dir_ = row['Dir']
        cl_id = row['CL_ID']
        map_dic[raw_colnm] = (dir_, cl_id)
    return map_dic


def aggregate_cols(input_file, out_file, map_dic,  sep='\t', splitter='_'):
    df_in = pd.read_csv(input_file, sep=sep, header=0, index_col=0)
    columns = df_in.columns
    index = df_in.index
    columns_new = list(set([n.split(splitter)[-1] for n in columns]))

    li_out = []
    print(columns_new)
    for name in columns_new:
        target_cols = np.asarray(list([df_in[i] for i in columns if i.endswith(name)]), dtype=np.float)
        #target_cols = np.asarray(list([df_in[i] for i in columns if i.startswith(name)]))
        target_sum = list(target_cols.sum(axis=0))
        li_out.append(target_sum)

    columns_new_li = []
    out_col_indices = []
    for idx, name in enumerate(columns_new):
        for dir_, cls_id in map_dic[name]:
            new_name = '|'.join([dir_, name, cls_id])
            columns_new_li.append(new_name)
            out_col_indices.append(idx)
    
    new_out_li = [li_out[idx] for idx in out_col_indices]

    np_out = np.asarray(new_out_li).T

    df_out = pd.DataFrame(np_out, columns=columns_new_li, index=index)


    df_out.to_csv(out_file)
    print('Saving to ', out_file)


def aggregate_cols_old(input_file, out_file, sep='\t', splitter='_', from_start=False):
    df_in = pd.read_csv(input_file, sep=sep, header=0, index_col=None)
    columns = df_in.columns
    index = df_in.index
    if from_start:
        columns_new = list(set([n.split(splitter)[0] for n in columns]))
    else:
        columns_new = list(set([n.split(splitter)[-1] for n in columns]))
    li_out = []
    print('line 69 col=', columns_new)
    for name in columns_new:
        if from_start:
            target_cols = np.asarray(list([df_in[i] for i in columns if i.startswith(name)]))
        else:
            target_cols = np.asarray(list([df_in[i] for i in columns if i.endswith(name)]))
        target_sum = list(target_cols.sum(axis=0))
        li_out.append(target_sum)

    np_out = np.asarray(li_out).T
    df_out = pd.DataFrame(np_out, columns=columns_new, index=index)
    df_out.to_csv(out_file)
    print('Saving to ', out_file)


def read_deg_file(file, sep='\t'):
    df = pd.read_csv(file, sep=sep, header=0, index_col=0)
    columns = df.columns
    nrof_col = len(columns)
    name_set = set(columns)
    nrof_name = len(name_set)
    if nrof_name != nrof_col:
        print('Found repeated col names nrof_col=%d != nrof_name=%d '%(nrof_col, nrof_name))
    dic = {}

    for name in name_set:
        col_values = np.asarray(list(df[name]), dtype=np.int32).reshape(-1, 1)
        #print(col_values.shape)
        dic[name] = col_values
    return dic


def read_attribute_file(file, sep='\t', key_col=2):
    counter = 0

    with open(file, 'r') as f:
        for line in f:
            print(line)
            counter += 1
            if counter == key_col:
                break
    print('line=', line)
    num_names = line.strip().split(':')[1].strip().replace(' ', '').split(';')
    num2name_map = {}
    for pair in num_names:
        num, name = pair.strip().split('-')
        num2name_map[num] = name
    df = pd.read_csv(file, sep=sep, skiprows=3, header=0, index_col=None)

    dic = defaultdict(list)

    for idx, row in df.iterrows():
        cell_type = int(row['CellType'])
        cell_barcode = row['#CellBarcode']
        dic[cell_type].append(cell_barcode)

    return num2name_map, dic


def CHECK_EXIST(path, typ='f'):
    tps = ['f', 'd']
    assert typ in tps, 'typ %s not in %s'%(typ, tps) 
    assert os.path.exists(path), 'File or directory not exists: ' + path
    if typ == 'f':
        assert os.path.isfile(path), 'Input is not %s: %s' % (typ, path)
    else:
        assert os.path.isdir(path), 'Input is not %s: %s' % (typ, path)


def MAKE_EXIST(path, typ='f'):
    tps = ['f', 'd']
    assert typ in tps, 'typ %s not in %s'%(typ, tps)
    dir_to_check = path
    if typ == 'f':
        dir_to_check = os.path.split(path)[0]

    if not os.path.exists(dir_to_check):
        os.makedirs(dir_to_check)


def main(args):
    CHECK_EXIST(args.input_deg, 'f')
    CHECK_EXIST(args.input_attr, 'f')

    barcode2col_values = read_deg_file(args.input_deg)
    num2name_map, barcode2col_names = read_attribute_file(args.input_attr)
    print('barcode2col_names.keys=', barcode2col_names.keys())
    print('num2name_map', num2name_map)
    col_sum_arr = None
    columns = []
    for cell_type in sorted(list(barcode2col_names.keys())):
        barcode_li = barcode2col_names[cell_type]
        col_values = None
        for bar in barcode_li:
            if not bar in barcode2col_values:
                print('bar=%s, not in keys=%s'%(bar, barcode2col_values.keys()))
                continue
            col_v = barcode2col_values[bar]
            if col_values is None:
                col_values = col_v
            else:
                col_values += col_v
        columns.append(cell_type)
        print(col_values.shape)
        if col_sum_arr is None:
            col_sum_arr = col_values
        else:
            col_sum_arr = np.hstack([col_sum_arr, col_values])

    columns = [num2name_map[str(i)] for i in columns]

    name2dir_cl_id = read_celltype(args.cell_type)
    print('name2dir_cl_id.keys=', name2dir_cl_id.keys())
    print(columns)

    columns = ['%s|%s|%s'%(name2dir_cl_id[n][0], n, name2dir_cl_id[n][1]) for n in columns]
    print(col_sum_arr.shape)
    df = pd.DataFrame(col_sum_arr, columns=columns, index=None)
    print('exp_sum.head()=\n', df.head())
    output_raw_path = os.path.join(args.output, 'exp_raw.txt')
    MAKE_EXIST(output_raw_path, 'f')
    df.to_csv(output_raw_path, index=None)
    print('Saving to', output_raw_path)


    output_sum_path = os.path.join(args.output, 'exp_sum.txt')
    MAKE_EXIST(output_sum_path, 'f')
    aggregate_cols_old(output_raw_path, output_sum_path, sep='\t', splitter='|', from_start=False)
    print('Saving to', output_sum_path)

    print('All done.')


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1', '--input-deg', type=str, required=True, 
        help='Input xlsx file.')
    parser.add_argument('-i2','--input-attr')
    parser.add_argument('-i3','--cell-type')

    parser.add_argument('-o', '--output', type=str, default='./output.txt', 
        help='output txt file.')
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
