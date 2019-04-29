bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..


# data_dir=xxx
data_dir=$bash_dir
input_path=$data_dir/testcef.txt

output_dir=$bash_dir/output

python $bash_dir/create_cell_meta.py \
    --input $input_path \
    --output $output_dir \
