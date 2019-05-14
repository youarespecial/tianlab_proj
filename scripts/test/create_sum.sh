bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..

exp_raw=/home/ningshengma/personal/tianlab_proj/scripts/HumanHeart_SingleCell_Cui2019/output/exp_raw.txt
output_dir=$bash_dir/output

python $proj_dir/src/create_sum.py \
    --input $exp_raw \
    --output $output_dir \


