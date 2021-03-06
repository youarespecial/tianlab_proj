bash_dir=$(cd `dirname $0`; pwd)

data_dir=$bash_dir

deg_path=$data_dir/deg.txt
attr_path=$data_dir/attr.txt
celltype_path=$data_dir/cell_type.txt

output_dir=$bash_dir/output-test
src_dir=$bash_dir/../../src

python $src_dir/process_sum.py \
	--input-deg $deg_path \
	--input-attr $attr_path \
	--cell-type $celltype_path \
	--output $output_dir \
	--version 1
