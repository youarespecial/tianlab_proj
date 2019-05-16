bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..

. ~/.bashrc

input_txt=/home/disk/yangjing/yj_proj/NSC_cl/location_human.txt
data_dir=/home/disk/yangjing/yj_proj/NSC_cl
output_dir=$bash_dir/output-pmid
pmid=26060301

python3 $proj_dir/src/filter_exp.py \
    --input $input_txt \
    --output $output_dir \
    --data-dir $data_dir \
#    --pmid-li $pmid


