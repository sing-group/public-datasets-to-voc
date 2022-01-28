#!/bin/bash

annotations() {
    for dir in $(ls $annotations_input); 
    do 
        for f in $(ls $annotations_input/$dir); 
        do 
            cp $annotations_input/$dir/$f $annotations_output/${dir}_$f; 
        done
    done
}

images(){
    for dir in $(ls $images_input); 
    do 
        for f in $(ls $images_input/$dir); 
        do 
            cp $images_input/$dir/$f $images_output/${dir}_$f; 
        done 
    done
}

annotations_output="bounding-box" 
images_output="JPEGImages" 

[ ! -d $annotations_output ] && mkdir -p $annotations_output
[ ! -d $images_output ] && mkdir -p $images_output

annotations_input="Test/Annotations"
images_input="Test/Images"

annotations
images

annotations_input="TrainValid/Annotations"
images_input="TrainValid/Images"

annotations
images
