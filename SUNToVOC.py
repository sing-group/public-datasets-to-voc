import os
import sys
import argparse
from skimage import io

import xml.etree.cElementTree as ET
from skimage.measure import label, regionprops

parser = argparse.ArgumentParser()
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

entries = os.listdir("annotation_txt")
for entry in entries:
    print("Processing " + entry)
    with open(os.path.join("annotation_txt", entry)) as f:
        for line in f:
            # Format
            # Filename min_Xcoordinate,min_Ycoordinate,max_Xcorrdinate,max_Ycoordinate,class_id
            image_name=line.split(" ")[0]
            coord=line.split(" ")[1]
            image_dir=entry.split(".")[0]
            min_Xcoordinate=coord.split(",")[0]
            min_Ycoordinate=coord.split(",")[1]
            max_Xcorrdinate=coord.split(",")[2]
            max_Ycoordinate=coord.split(",")[3]
            #class_id=coord.split(",")[4]
            image = io.imread(os.path.join(image_dir, image_name)) / 255.0
            h, w, d = image.shape
            
            annotation = ET.Element("annotation")
            folder = ET.SubElement(annotation, "folder").text = images_output
            filename = ET.SubElement(annotation, "filename").text = image_name
            path = ET.SubElement(annotation, "path").text = args.path + image_name
            source = ET.SubElement(annotation, "source")
            ET.SubElement(source, "database").text = "SUN"
            
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
            
            bndbox = ET.SubElement(object, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(min_Xcoordinate)
            ET.SubElement(bndbox, "ymin").text = str(min_Ycoordinate)
            ET.SubElement(bndbox, "xmax").text = str(max_Xcorrdinate)
            ET.SubElement(bndbox, "ymax").text = str(max_Ycoordinate)
            
            tree = ET.ElementTree(annotation)
            output = os.path.join(annotations_output, (image_name.split(".")[0] + ".xml"))
            tree.write(output)
