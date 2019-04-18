bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..


# data_dir=xxxx
data_dir=$bash_dir
input=$/data_dir/xxxx

output_dir=$bash_dir/output

python $bash_dir/create_cell_meta.py \
    --input $input \
    --output $output_dir \
