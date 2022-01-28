import os
import sys
import argparse

import xml.etree.cElementTree as ET
from skimage import io
from skimage.measure import label, regionprops

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="Directory name to process")
parser.add_argument("-p", "--path", help="Directory name to locate the images")
args = parser.parse_args()

annotations_output="Annotations"
images_output="JPEGImages"

try:
    os.mkdir(annotations_output)
except OSError:
    print ("%s directory exists" % annotations_output)
else:
    print ("Successfully created the directory %s" % annotations_output)


if args.dir and os.path.isdir(args.dir) is False:
    print('Enter the name of an existing directory')
    sys.exit()

entries = os.listdir(args.dir)

for entry in entries:
    print("Procesing " + entry)
    
    image = io.imread(os.path.join(args.dir, entry)) / 255.0
    annotation = ET.Element("annotation")
    folder = ET.SubElement(annotation, "folder").text = images_output
    image_name = entry.split("_")[0] + ".jpg"

    filename = ET.SubElement(annotation, "filename").text = image_name 
    path = ET.SubElement(annotation, "path").text = args.path + image_name
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "CVC-PolypHD"

    h, w = image.shape
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(w)
    ET.SubElement(size, "height").text = str(h)
    ET.SubElement(size, "depth").text = "3"
    
    segmented = ET.SubElement(annotation, "segmented").text = "0"

    object = ET.SubElement(annotation, "object")
    ET.SubElement(object, "name").text = "polyp"
    ET.SubElement(object, "pose").text = "Unspecified"
    ET.SubElement(object, "truncated").text = "0"
    ET.SubElement(object, "difficult").text = "0"

    label_img = label(image, connectivity=image.ndim)

    props = regionprops(label_img)

    boxes = [(x.area, x.bbox, x.filled_image) for x in props if x.label != 0]  # label 0 is air
    boxes = sorted(boxes, key=lambda x: -x[0])

    for i in range(len(boxes)):
        ymin, xmin, ymax, xmax = boxes[i][1]
        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(xmin)
        ET.SubElement(bndbox, "ymin").text = str(ymin)
        ET.SubElement(bndbox, "xmax").text = str(xmax)
        ET.SubElement(bndbox, "ymax").text = str(ymax)
    tree = ET.ElementTree(annotation)
    output = os.path.join(annotations_output, (image_name.split(".")[0] + ".xml"))
    tree.write(output)
       
