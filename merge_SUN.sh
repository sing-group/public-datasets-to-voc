#!/bin/bash

dir1="sundatabase_positive_part1"
dir2="sundatabase_positive_part2"

images_output="JPEGImages" 

[ ! -d $dir1/$images_output ] && mkdir -p $dir1/$images_output


for d  in $(ls $dir1);
do
    if [[ $d == *"case"* ]]; then
        cp $dir1/$d/* $dir1/$images_output;
        break;
    fi
done

for d  in $(ls $dir2);
do
    if [[ $d == *"case"* ]]; then
        echo $d;
        cp $dir2/$d/* $dir1/$images_output;
        break;
    fi
done
