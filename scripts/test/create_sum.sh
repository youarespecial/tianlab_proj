bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..

exp_raw=/home/disk/yangjing/tianlab/tools/scRef-master/yj31_38/5_fyh_checkadd/deal_mat/30595452/GSE123139/out_raw_exp.txt
output_dir=$bash_dir/output

python $proj_dir/src/create_sum.py \
    --input $exp_raw \
    --output $output_dir \


