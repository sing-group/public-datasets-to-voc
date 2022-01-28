#!/bin/bash

images_dir="JPEGImages";
mask_dir="Mask";

[ ! -d $images_dir ] && mkdir $images_dir;
[ ! -d $mask_dir ] && mkdir $mask_dir;

for dir in $(ls $1);
do
    for f in $(ls $1/$dir);
    do
        if [[ $f == *"mask"* ]]; then
            cp $1/$dir/$f $mask_dir/$f;
        else
            cp $1/$dir/$f $images_dir/$f;
        fi
    done
done
