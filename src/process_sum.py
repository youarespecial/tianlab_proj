#!/usr/bin/python3
### python 3.5
# -*- coding: utf-8 -*-

import sys
import argparse 
import os
import pandas as pd
import numpy as np
from collections import defaultdict

def read_celltype(csv_path, key_name='Raw_colnm', value_names=['Dir', 'CL_ID'], sep='\t'):
    #df = pd.read_csv(csv_path, header=0, sep=sep, index_col=None)
    #df = pd.DataFrame(li[1:], columns=li[0], index=None)
    colunms = []
    with open(csv_path, 'r') as f:
        lines = f.readlines()
        lines_split = [l.strip().split(sep) for l in lines]
        columns = lines_split[0]
        nrof_col = len(columns)
        data = [i[:nrof_col] for i in lines_split[1:]]
        df = pd.DataFrame(data, columns=columns, index=None)
    columns = list(df.columns)

    for name in [key_name] + value_names:
        if name not in columns:
            raise ValueError('name=%s not in columns=%s'%(name, columns))
    print('cell_type df.head()\n', df.head())
    map_dic = {}
    for idx, row in df.iterrows():
        key = row[key_name]
        values = [row[n] for n in value_names]
        if key not in map_dic:
            map_dic[key] = values
        else:
            print('key_name=%s has repeated value=%s'%(key_name, key))
    return map_dic


def read_cell_annot(csv_path, key_name='Cluster', sep='\t'):
    df = pd.read_csv(csv_path, header=0, sep=sep, index_col=None)
    #df = pd.DataFrame(li[1:], columns=li[0], index=None)
    columns = list(df.columns)
    print('cell_annot df.head()\n', df.head())
    map_dic = defaultdict(list) 
    for idx, row in df.iterrows():
        key = row[key_name]
        cell = row['Cell']
        #print('row_cell=', cell)
        map_dic[key].append(cell)
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
    df_in = pd.read_csv(input_file, sep=sep, header=0, index_col=0)
    columns = df_in.columns
    
    index = df_in.index
    if from_start:
        columns_new = list(set([n.split(splitter)[0] for n in columns]))
    else:
        columns_new = list(set([n.split(splitter)[-1] for n in columns]))
    li_out = []
    columns_final = []
    for name in columns_new:
        dir_ = [i for i in columns if i.endswith(name)][0].split(splitter)[0]
        if from_start:
            target_cols = np.asarray([list(df_in[i]) for i in columns if i.startswith(name)]).astype(np.int32)
        else:
            target_cols = np.asarray([list(df_in[i]) for i in columns if i.endswith(name)]).astype(np.int32)
        target_sum = list(target_cols.sum(axis=0))
        li_out.append(target_sum)
        columns_final.append('%s%s%s'%(dir_, splitter, name))
    
    np_out = np.asarray(li_out).T
    df_out = pd.DataFrame(np_out, columns=columns_final, index=index)
    df_out.to_csv(out_file, sep=sep)
    return df_out


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
    return dic, df.index


def read_file(file, sep='\t'):
    df = pd.read_csv(file, sep=sep, header=0, index_col=0)
    return df


def write_exp_file(file_in, file_out, ignore_col_indices=[1, 2, 4, 5, 6, 7],cell_id_row_idx =3, cell_type_row_idx=4, sep='\t'):
    cell_type_row, cell_id_row = '', ''
    with open(file_in, 'r') as reader, open(file_out, 'w') as writer:
        for idx, line in enumerate(reader, start=1):
            if idx == cell_type_row_idx:
                cell_type_row = line.strip().lstrip('Cell_type').strip()
            if idx in ignore_col_indices:
                print('Skipped line[%d]=%s'%(idx, line))
                continue
            if idx == cell_id_row_idx:
                line = line.lstrip('\t').lstrip('Cell_ID').lstrip('\t')
                cell_id_row = line.strip()
            writer.write(line)

    df = pd.read_csv(file_in, sep=sep, skiprows=7, header=None, index_col=0)
    print('deg.df.head()')
    print(df.head())
    columns = df.columns
    columns_skipped = list(columns)[1:] ### skip first col that is empty, txt format is wrong!!!!
    nrof_col = len(columns_skipped)
    cell_types = cell_type_row.split('\t')
    nrof_typ = len(cell_types)
    cell_ids = cell_id_row.split('\t')
    nrof_id = len(cell_ids)
    if not (nrof_col == nrof_typ and nrof_col == nrof_id):
        # raise ValueError('nrof_col=%s, nrof_typ=%s, nrof_id=%s, not all equal'%(nrof_col, nrof_typ, nrof_id))
        print('Warning nrof_col=%s, nrof_typ=%s, nrof_id=%s, not all equal'%(nrof_col, nrof_typ, nrof_id))
    dic = {}
    for idx, (c_typ, col_name) in enumerate(zip(cell_types, columns_skipped)):
        # col_values_i = rows_arr[:, idx].reshape(1, -1)
        col_values_i = np.array(df[col_name]).reshape(1, -1).astype(np.int32)
        if c_typ not in dic:
            dic[c_typ] = col_values_i
        else:
            dic[c_typ] += col_values_i
    return dic, df.index


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

def write_cell_meta_v3(csv_path, out_path, col_indices=(2,3)):
    columns = ['ID', 'Cluster']
    li = []
    with open(csv_path, 'r' ) as f:
        for idx, l in enumerate(f):
            if idx in col_indices:
                sp = l.strip().split('\t')[1:]
                li.append(sp)
            elif idx > max(col_indices):
                break
    arr = np.array(li).T
    df = pd.DataFrame(arr, columns=columns, index=None)
    df.to_csv(out_path, sep='\t', index=None)
    print('Savint to', out_path)


def write_cell_meta_v2(csv_path, out_path, columns_new=('ID', 'Cluster')):
    df_in = pd.read_csv(csv_path, sep='\t', header=0, index_col=None)
    df_out = df_in.iloc[:,[0, 1]]
    df_out.columns = columns_new
    df_out.to_csv(out_path, sep='\t', index=None)
    print('Savint to', out_path)

def write_cell_meta_v1(csv_path, out_path, columns_new=('ID', 'Cluster')):
    num2cluster, _ = read_attribute_file(csv_path)

    df_in = pd.read_csv(csv_path, sep='\t', header=0, index_col=None, skiprows=3)
    li = []
    #print('write_cell_meta_v1', df_in.columns)
    #print(num2cluster)
    for idx, row in df_in.iterrows():
        bar = row['#CellBarcode']
        cluster = num2cluster[str(row['CellType']).strip()]
        li.append([bar, cluster])
    df_out = pd.DataFrame(li, columns=columns_new, index=None)
    df_out.to_csv(out_path, sep='\t', index=None)
    print('Savint to', out_path)



def main(args):
    CHECK_EXIST(args.input_deg, 'f')
    deg_filename = os.path.split(args.input_deg)[-1]

    if args.version == 3:
        cell_exp_path = os.path.join(args.output, 'cell_exp.txt')
        cell_meta_path = os.path.join(args.output, 'cell_meta.txt')
        MAKE_EXIST(cell_exp_path, 'f')
        write_cell_meta_v3(args.input_deg, cell_meta_path)
        dat_dic, original_index = write_exp_file(args.input_deg, cell_exp_path)
        print('Saving to ', cell_exp_path)
        cell_type_map = read_celltype(args.cell_type, value_names=['Dir', 'CL_ID']) 
        dat_dic_new = {}
        for idx, (cell_type, summed_arr) in enumerate(dat_dic.items(), start=1):
            if cell_type not in cell_type_map:
                print('cell_type=%s not in %s, is skipped.'%(cell_type, cell_type_map.keys()))
                continue
            dir_, cl_id = cell_type_map[cell_type]

            col_name = '|'.join([dir_, deg_filename, cell_type, cl_id])
            dat_dic_new[col_name] = list(summed_arr.reshape(summed_arr.size))
            print('Process %5d/%5d cell_type=%s, dir_=%s, cl_id=%s'%(idx, len(dat_dic), cell_type, dir_, cl_id))

        df_raw = pd.DataFrame(dat_dic_new, index=original_index)

    elif args.version == 2:
        cluster2cell = read_cell_annot(args.input_attr)
        cell_meta_path = os.path.join(args.output, 'cell_meta.txt')
        MAKE_EXIST(cell_meta_path, 'f')
        write_cell_meta_v2(args.input_attr, cell_meta_path)

        cell_type_map = read_celltype(args.cell_type, value_names=['Dir', 'CL_ID']) 
        print('cell_type_map=', cell_type_map) 

        df = read_file(args.input_deg)
        print('deg file.head()\n', df.head())
        columns = df.columns
        col_raw_arr = None
        columns_raw = []
        for idx, (cluster, cell_li) in enumerate(cluster2cell.items(), start=1):
            col_values = None
            for cell in cell_li:
                if cell not in columns:
                    print('cell=%s not in columns=%s'%(cell, columns))
                    continue
                values = np.array(list(df[cell])).reshape(-1, 1).astype(np.int32)
                if col_values is None:
                    col_values = values
                else:
                    col_values += values
            if col_values is not None:
                if col_raw_arr is None:
                    col_raw_arr = col_values

                else:
                    col_raw_arr += col_values
                    col_raw_arr = np.hstack([col_raw_arr, col_values])
                dir_, cl_id = cell_type_map[cluster]

                col_name = '|'.join([dir_, deg_filename, cluster, cl_id])
                columns_raw.append(col_name)
            print('Process %5d/%5d rawname=%s'%(idx, len(cluster2cell), cluster))

        df_raw = pd.DataFrame(col_raw_arr, columns=columns_raw, index=df.index)

    elif args.version == 1: 
        cell_meta_path = os.path.join(args.output, 'cell_meta.txt')
        MAKE_EXIST(cell_meta_path, 'f')
        write_cell_meta_v1(args.input_attr, cell_meta_path)

        barcode2col_values, deg_index = read_deg_file(args.input_deg)
        num2name_map, barcode2col_names = read_attribute_file(args.input_attr)
        print('barcode2col_names.keys=', barcode2col_names.keys())
        print('num2name_map', num2name_map)
        col_sum_arr = None
        columns = []
        nrof_col = len(barcode2col_names)

        name2dir_cl_id = read_celltype(args.cell_type)
        print('Finish reading celltype file')

        for idx, cell_type in enumerate(sorted(list(barcode2col_names.keys())), start=1):
            name = num2name_map[str(cell_type)]
            if not name in name2dir_cl_id:
                print('cell_type=%s-%s not in keys=%s, sum_col_vaules are skipped'%(cell_type, name, name2dir_cl_id.keys()))
                continue
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
            if col_sum_arr is None:
                col_sum_arr = col_values
            else:
                col_sum_arr = np.hstack([col_sum_arr, col_values])
            print('Processing %5d/%5d col ...'%(idx, nrof_col))

        columns = [num2name_map[str(i)] for i in columns]

        print('name2dir_cl_id.keys=', name2dir_cl_id.keys())
        print('output-columns=', columns)

        columns = ['%s|%s|%s|%s'%(name2dir_cl_id[n][0],deg_filename, n, name2dir_cl_id[n][1]) for n in columns]
        df_raw = pd.DataFrame(col_sum_arr, columns=columns, index=deg_index)
    

    print('exp_raw.head()=\n', df_raw.head())
    output_raw_path = os.path.join(args.output, 'exp_raw.txt')
    MAKE_EXIST(output_raw_path, 'f')
    df_raw.to_csv(output_raw_path, sep='\t')
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
    parser.add_argument('-v', '--version', type=int, choices=[1, 2, 3], 
        help='Code version to process different data.')
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
