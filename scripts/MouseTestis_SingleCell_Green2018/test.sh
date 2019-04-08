data_dir=./scripts/MouseTestis_SingleCell_Green2018

deg_path=$data_dir/deg.txt
attr_path=$data_dir/attr.txt

celltype_path=$data_dir/cell_type.txt
output_dir=$data_dir/test-output

python src/process_sum.py \
	--input-deg $deg_path \
	--input-attr $attr_path \
	--cell-type $celltype_path \
	--output $output_dir \
	--version 1
