import os
import sys
from skimage import io
import argparse

import xml.etree.cElementTree as ET

from skimage.measure import label, regionprops


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="Directory name to process")
parser.add_argument("-p", "--path", help="Directory name to locate the images")
args = parser.parse_args()

annotations_output="Annotations"
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
    if entry.endswith('txt'):
        image_name = os.path.splitext(entry)[0]  + ".jpg"
        image = io.imread(os.path.join("JPEGImages", image_name)) / 255.0
        annotation = ET.Element("annotation")
        folder = ET.SubElement(annotation, "folder").text = "JPEGImages"
        filename = ET.SubElement(annotation, "filename").text = image_name
        path = ET.SubElement(annotation, "path").text = args.path + image_name
        source = ET.SubElement(annotation, "source")
        ET.SubElement(source, "database").text = "LDPolypVideo"

        h, w, d = image.shape
        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = str(w)
        ET.SubElement(size, "height").text = str(h)
        ET.SubElement(size, "depth").text = str(d)

        segmented = ET.SubElement(annotation, "segmented").text = "0"

        object = ET.SubElement(annotation, "object")
        ET.SubElement(object, "name").text = "polyp"
        ET.SubElement(object, "pose").text = "Unspecified"
        ET.SubElement(object, "truncated").text = "0"
        ET.SubElement(object, "difficult").text = "0"
        
        bounding_box = open(os.path.join("bounding-box", entry)).readlines()[1:]
        if bounding_box:
            bbox = [i.split(' ') for i in bounding_box] 
    
            for b in bbox:
                xmin=b[0]
                ymin=b[1]
                xmax=b[2]
                ymax=b[3]
            
                bndbox = ET.SubElement(object, "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(xmin)
                ET.SubElement(bndbox, "ymin").text = str(ymin)
                ET.SubElement(bndbox, "xmax").text = str(xmax)
                ET.SubElement(bndbox, "ymax").text = str(ymax)
        
        tree = ET.ElementTree(annotation)
        output = os.path.join(annotations_output, (os.path.splitext(entry)[0] + ".xml"))
        tree.write(output)
        
