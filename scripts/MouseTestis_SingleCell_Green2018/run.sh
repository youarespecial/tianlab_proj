data_dir=/home/disk/yangjing/tianlab/tools/scRef-master/Reference/L2/L2_zy/MouseTestis_SingleCell_Green2018


deg_path=$data_dir/GSE112393_MergedAdultMouseST25_DGE.txt
attr_path=$data_dir/GSE112393_MergedAdultMouseST25_PerCellAttributes.txt

celltype_path=$data_dir/cell_type.txt
bash_dir=$(cd `dirname $0`; pwd)
output_dir=$bash_dir/output
src_dir=$bash_dir/../../src

python $src_dir/process_sum.py \
	--input-deg $deg_path \
	--input-attr $attr_path \
	--cell-type $celltype_path \
	--output $output_dir \
	--version 1
