bash_dir=$(cd `dirname $0`; pwd)
proj_dir=$bash_dir/../..

### input_dir is directory  fname can be multiple.
input_dir=xxx
fname1=xxx
fname2=xxx
fname3=xxx

sep=","

output_dir=$bash_dir/output

python $proj_dir/src/merge_multi_file.py \
    --input $input_dir \
    --fnames $fname1 $fname2 $fname3 \
    --sep $sep \
    --output $output_dir
