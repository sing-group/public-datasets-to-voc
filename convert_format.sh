#!/bin/bash
 
echo "Choose an option:"
echo "1) BMP to TIFF"
echo "2) BMP to JPG"
echo "3) PNG to JPG"
echo "4) TIF to JPG"

read option 

case $option in
    1)
        mogrify -format tiff *.bmp
        rm *.bmp
    ;;
    2)
        mogrify -format jpg *.bmp
        rm *.bmp
    ;;
    3)
        mogrify -format jpg *.png
        rm *.png
    ;;
    4)
        mogrify -format jpg *.tif
        rm *.tif
    ;;
    *)
        echo "Incorrecto"
    ;;
esac
