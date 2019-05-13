bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..


<<<<<<< HEAD
# data_dir=xxx
data_dir=$bash_dir
input_path=$data_dir/testcef.txt
=======
# data_dir=xxxx
data_dir=$bash_dir
input=$/data_dir/xxxx
>>>>>>> 6413a416859e4f1769499f603e018e97094713a5

output_dir=$bash_dir/output

python $bash_dir/create_cell_meta.py \
<<<<<<< HEAD
    --input $input_path \
=======
    --input $input \
>>>>>>> 6413a416859e4f1769499f603e018e97094713a5
    --output $output_dir \
