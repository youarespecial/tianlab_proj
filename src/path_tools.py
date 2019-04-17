#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os
import sys
import json
import glob
from collections import defaultdict
import fnmatch
import shutil
import inspect


def wprint(*info):
    txt = ' '.join([str(i) for i in info])
    print("\033[0;31m%s\033[0m" % txt)


def glob_file(src_dir, suffix, recursive=False):
    py_version = sys.version_info.major
    if py_version == 2:
        return  glob_file_python2(src_dir, suffix, recursive)
    elif py_version == 3:
        return glob_file_python3(src_dir, suffix, recursive)
    else:
        raise ValueError('Parsed wrong python version =%d, not in [2, 3]'%(py_version))


def glob_file_python2(src_dir, suffix, recursive=False):

    if recursive:
        matches = []
        for root, dirnames, filenames in os.walk(src_dir):
            for filename in fnmatch.filter(filenames, '*.' + suffix):
                matches.append(os.path.join(root, filename))
    else:
        matches = [os.path.join(src_dir, filename) for filename in os.listdir(src_dir) if filename.endswith('.' + suffix)]
        matches = [p for p in matches if os.path.isfile(p)]

    return matches


def glob_file_python3(src_dir, suffix='json', recursive=False):

    if recursive:
        matches = glob.glob(os.path.join(src_dir, '**', '*.' + suffix), recursive=True)
    else:
        matches = glob.glob(os.path.join(src_dir, '*.' + suffix))
    return matches


def parse_paths(input_dir, annot_typ, image_dir='', img_ext='jpg', recursive=True, verbose=False):
    annot_paths = glob_file(input_dir, suffix=annot_typ, recursive=recursive)
    image_paths, annot_paths_good = [], []
    nrof_aplhabet = len(annot_typ)

    if not image_dir:
        image_dir = input_dir
    input_dir, image_dir = [os.path.abspath(p) for p in [input_dir, image_dir]]
    for annot_path in annot_paths:
        img_path = annot_path.replace(input_dir.rstrip('/'), image_dir.rstrip('/'))[:-nrof_aplhabet] + img_ext
        if not os.path.exists(img_path):
            dir_, filename = os.path.split(img_path)
            if '_' in filename:
                img_fname = filename.rsplit('_', 1)[0]
                img_path = os.path.join(dir_, img_fname + '.' + img_ext)

        if not os.path.exists(img_path) or not os.path.isfile(img_path):
            img_path = json.load(open(annot_path, 'r')).get('photo_path', '')
                
        if not os.path.exists(img_path) or not os.path.isfile(img_path):
            if verbose:
                wprint('Not exists: ' + img_path)
            continue

        image_paths.append(img_path)
        annot_paths_good.append(annot_path)
    return image_paths, annot_paths_good


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


def get_cur_info():
    """Returns the current line number in our program."""
    f = inspect.currentframe().f_back
    cal_func_name = f.f_code.co_name
    cal_line_num = f.f_lineno + 1
    info = 'Func=%s, line=%d '%(cal_func_name, cal_line_num)
    return info

