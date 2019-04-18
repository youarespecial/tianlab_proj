bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..


# data_dir="/home/disk/yangjing/tianlab/tools/scRef-master/Reference/yj31_38/4th_human/matrix_dealing/HumanPluripotentStemCell_SingleCell_Han2018"
data_dir=$bash_dir
anno_path=$data_dir/anno_all.csv

celltype_path="$data_dir/cell_type.txt"
# key_name="Cell type"
output_dir=$bash_dir/output

python $bash_dir/create_cell_meta.py \
    --anno $anno_path \
    --cell-typ $cell_typ_path \
    --output $output_dir \
    # --key-name $key_name \
