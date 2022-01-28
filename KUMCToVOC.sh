#!/bin/bash
 
 process(){
    #remove white spaces in bndbox
    $(sed -i 's/>\s*/>/g' $path);
    
    sed  -i "2s/.*/\t<folder>JPEGImages<\/folder>/" $path;
    sed  -i "3s/.*/\t<filename>${image_name%.*}.jpg<\/filename>/" $path;
    sed  -i "4s/.*/\t<path>\/media\/alba\/Data2\/datasets\/KUMC\/JPEGImages\/${image_name%.*}.jpg<\/path>/" $path;
}


read_val_or_test(){

    for dir in $(ls $annotation);
    do 
        for f in $(ls $annotation/$dir); 
        do 
            path=$annotation_output/$suffix${dir}_$f
            image_name=$suffix${dir}_$f
            
            mv $annotation/$dir/$f $path;
            
            process
        done
    done


    for dir in $(ls $images);
    do
        for f in $(ls $images/$dir); 
        do
            path=$images_output/$suffix${dir}_$f
            mv $images/$dir/$f $path;
        done
    done

}

read_train() {

    for f in $(ls $annotation); 
    do 
        path=$annotation_output/$suffix$f
        image_name=$suffix$f
        
        mv $annotation/$f $path;
            
        process
    done

    for f in $(ls $images); 
    do
        path=$images_output/$suffix$f
        mv $images/$f $path;
    done

}

train="train2019"
train_annotation="$train/Annotation"
train_image="$train/Image"

val="val2019"
val_annotation="$val/Annotation"
val_image="$val/Image"

test="test2019"
test_annotation="$test/Annotation"
test_image="$test/Image"

annotation_output="Annotations"
images_output="JPEGImages"

[ ! -d $annotation_output ] && mkdir -p $annotation_output
[ ! -d $images_output ] && mkdir -p $images_output

annotation=$val_annotation
images=$val_image

suffix="v"

echo "Processing " $annotation " and " $images
read_val_or_test

rm -r $val

annotation=$test_annotation
images=$test_image
suffix="t"

echo "Processing " $annotation " and " $images
read_val_or_test

rm -r $test

annotation=$train_annotation
images=$train_image
suffix="tr"

echo "Processing " $annotation " and " $images
read_train

rm -r $train

$(sed -i -e 's/hyperplastic/polyp/g' $annotation_output/*)
$(sed -i -e 's/adenomatous/polyp/g' $annotation_output/*)
$(sed -i -e 's/Unknown/KUMC/g' $annotation_output/*)
