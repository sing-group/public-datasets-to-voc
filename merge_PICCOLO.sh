#!/bin/bash

mask_output="Masks"
images_output="JPEGImages"

[ ! -d $mask_output ] && mkdir -p $mask_output
[ ! -d $images_output ] && mkdir -p $images_output

for p in "train/masks/*" "validation/masks/*" "test/masks/*"
do
   cp -r $p $mask_output
done

for p in "train/polyps/*" "validation/polyps/*" "test/polyps/*"
do
   cp -r $p $images_output
done

