import os
import sys
import argparse
import json
import xml.etree.cElementTree as ET

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

with open('kavsir_bboxes.json') as f:
  data = json.load(f)


for image_name in data:
    print(image_name, ":", data[image_name])
    
    annotation = ET.Element("annotation")
    folder = ET.SubElement(annotation, "folder").text = images_output
    filename = ET.SubElement(annotation, "filename").text = image_name + ".jpg"
    path = ET.SubElement(annotation, "path").text = args.path + image_name + ".jpg"
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Kvasir-SEG"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(data[image_name]["width"])
    ET.SubElement(size, "height").text = str(data[image_name]["height"])
    ET.SubElement(size, "depth").text = "3"
    segmented = ET.SubElement(annotation, "segmented").text = "0"
 
    object = ET.SubElement(annotation, "object")
    ET.SubElement(object, "name").text = "polyp"
    ET.SubElement(object, "pose").text = "Unspecified"
    ET.SubElement(object, "truncated").text = "0"
    ET.SubElement(object, "difficult").text = "0"
    
    for bbox in data[image_name]["bbox"]:
        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(bbox["xmin"])
        ET.SubElement(bndbox, "ymin").text = str(bbox["ymin"])
        ET.SubElement(bndbox, "xmax").text = str(bbox["xmax"])
        ET.SubElement(bndbox, "ymax").text = str(bbox["ymax"])
    
    tree = ET.ElementTree(annotation)
    output = os.path.join("Annotations", (image_name + ".xml"))
    tree.write(output)
