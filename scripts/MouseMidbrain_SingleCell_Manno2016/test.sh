bash_dir=$(cd `dirname $0`; pwd)

data_dir=$bash_dir

deg_path=$data_dir/cef.txt
celltype_path=$data_dir/cell_type.txt

output_dir=$bash_dir/output-test
src_dir=$bash_dir/../../src

python $src_dir/process_sum.py \
	--input-deg $deg_path \
	--cell-type $celltype_path \
	--output $output_dir \
	--version 3
