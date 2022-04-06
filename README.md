# Conversion of Public Colonoscopy Image Datasets to the PASCAL VOC format

> This repository was created from the following paper: A. Nogueira-Rodríguez; M. Reboiro-Jato; D. Glez-Peña; H. López-Fernández (2022) [**Performance of Convolutional Neural Networks for Polyp Localization on Public Colonoscopy Image Datasets**](https://doi.org/10.3390/diagnostics12040898). *Diagnostics*. Volume 12(4), 898.
>
> Please, cite it if you find it useful for your research.

## Motivation

In [this work](https://doi.org/10.3390/diagnostics12040898), we performed the biggest systematic evaluation of a polyp localization model trained using a private dataset to date, testing it on ten public colonoscopy image datasets: CVC-ClinicDB, CVC-ColonDB, CVC-PolypHD, CVC-ClinicVideoDB, ETIS-Larib, Kvasir-SEG, PICCOLO, SUN, KUMC, and LDPolypVideo. As a result of performing such an evaluation, we have published a set of scripts for converting the public datasets into the PASCAL VOC format for polyp localization.

## Datasets conversion

First, you need to download the original datasets. We have collected the information about them in [this repository](https://github.com/sing-group/deep-learning-colonoscopy/blob/master/README.md#public-datasets).

There are datasets that require a previous split of the images into subfolders (by using `separate_folder_*` scripts) or a union of folders (by using `merge_*` scripts) to later transform them into VOC format.

When we need to change the format of the images of the public datasets to JPEG, you can use the `convert_format.sh` script.

> **Note**: This conversion removes the existing images.

As detailed below, each dataset has a script to transform it into VOC format, allowing to indicate the directory of the public dataset and an output path where the images will be saved.

These scripts will create inside the folder where the command is launched an `Annotations` folder with the information of each image, including the bounding box. Sometimes it is neccessary to rename the images directory to  `JPEGImages`. As a result, a directory that contains both the annotations and the images is obtained.

### CVC-ColonDB and CVC-ClinicDB

First, run `convert_format.sh` selecting option 2 from the directory where the original images are stored. 
```bash
./convert_format.sh
```

Then run:

```bash
python3 CVC-ToVOC.py -d gtpolyp -p "/path/to/locate/images/JPEGImages/" -db "CVC-ClinicDB"
python3 CVC-ToVOC.py -d gtpolyp -p "/path/to/locate/images/JPEGImages/" -db "CVC-ColonDB"
mv bbdd JPEGImages
```
### CVC-ClinicVideoDB

First, split the images into subfolders with:

```bash
./separate_folder_ClinicVideo.sh
```
Then, run `convert_format.sh` selecting option 3 from the directory where the original images are stored.
```bash
./convert_format.sh
```

Finally run:
```bash
python3 ClinicVideoToVoc.py -d Mask -p "/path/to/locate/images/JPEGImages/"
```

### CVC-PolypHD

First, split the images into subfolders with:

```bash
./separate_folder_PolypHD.sh 
```
Then, run `convert_format.sh` selecting option 2 from the directory where the original images are stored.
```bash
./convert_format.sh
```

 Finally run:
```bash
python3 PolypHDToVOC.py -d Mask -p "/path/to/locate/images/JPEGImages/"
```
### ETIS-Larib
First, run `convert_format.sh` selecting option 4 from the directory where the original images are stored. 
```bash
./convert_format.sh
```

Then run:
```bash
python3 ETIS-LaribToVOC.py -d "Ground Truth" -p "/path/to/locate/images/JPEGImages/"
mv ETIS-LaribPolypDB JPEGImages
```
### Kvasir-SEG
Simply run the following command in the directory where the file `kavsir_bboxes.json` is located:
```bash
python3 KvasirToVOC.py  -d '.' -p "/path/to/locate/images/JPEGImages/"
```
### PICCOLO

First, merge the dataset subfolders with:

```bash
merge_PICCOLO.sh
```
Then, run `convert_format.sh` selecting option  4 from the directory where the original images are stored.
```bash
./convert_format.sh
```

Finally run:
```bash
python3 PICCOLOToVOC.py -d Mask -p "/path/to/locate/images/JPEGImages/"
```
### KUMC

Simply run:

```bash
./KUMCToVOC.sh 
```

### SUN
Run the following commands in the directory where the `sundatabase_positive_part1` and `sundatabase_positive_part2` directories are located:
```bash
./merge_SUN.sh
python3 SUNToVOC.py -p "/path/to/locate/images/JPEGImages/"
```
### LDPolypVideo

Run the following commands:

```bash
merge_and_rename_LDPolypVideo.sh
python3 LDPolypVideoToVOC.py -d bounding-box -p "/path/to/locate/images/JPEGImages/"