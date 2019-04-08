data_dir=./scripts/MouseEmbryo_SingleCell_Dong2018

deg_path=$data_dir/counts_matrix.txt
attr_path=$data_dir/m_cell_annot.txt

celltype_path=$data_dir/m_cell_type.txt
output_dir=$data_dir/test-output

python src/process_sum.py \
	--input-deg $deg_path \
	--input-attr $attr_path \
	--cell-type $celltype_path \
	--output $output_dir \
	--version 2
