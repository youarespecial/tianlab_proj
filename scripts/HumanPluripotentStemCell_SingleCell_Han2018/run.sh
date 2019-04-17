bash_dir=$(cd `dirname $0`; pwd)


# data_dir="/home/disk/yangjing/tianlab/tools/scRef-master/Reference/yj31_38/4th_human/matrix_dealing/HumanPluripotentStemCell_SingleCell_Han2018"
data_dir=$bash_dir
annot_path=$data_dir/anno_all.csv

celltype_path=$data_dir/cell_type.txt

output_dir=$bash_dir/output
# src_dir=$bash_dir/../../src

python $bash_dir/process.py \
	--input $data_dir \
	--output $output_dir \
	--anno-all $annot_path \
	--cell-type $celltype_path \
