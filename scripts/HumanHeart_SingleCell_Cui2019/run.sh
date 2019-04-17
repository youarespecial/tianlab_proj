bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..

# input="/home/disk/yangjing/tianlab/tools/scRef-master/Reference/yj31_38/4th_human/matrix_dealing/HumanPluripotentStemCell_SingleCell_Han2018"
data_dir=$bash_dir
input=$data_dir/merge.count_no.ERCC.xls
meta_path=$data_dir/cell_meta.txt

cell_typ_path=$data_dir/cell_type.txt
# key_name="Cell type"

output_dir=$bash_dir/output

python $proj_dir/src/create_cell_exp.py \
    --input $input \
    --cell-meta $meta_path \
    --output $output_dir



python $proj_dir/src/create_raw_sum.py \
    --input $input \
    --cell-meta $meta_path \
    --output $output_dir \
    --cell-typ $cell_typ_path
    # --key-name $key_name \