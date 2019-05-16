bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..

input_txt=
data_dir=
output_dir=$bash_dir/output
pmid=

python $proj_dir/src/filter_exp.py \
    --input $input_txt \
    --output $output_dir \
    --data-dir $data_dir \
    --pmid-li $pmid


