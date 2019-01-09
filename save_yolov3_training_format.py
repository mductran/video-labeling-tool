import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from xml.dom import minidom
from PIL import Image

def get_boxes_from_xmldoc(xmldoc):
	folder = str(xmldoc.getElementsByTagName('folder')[0].firstChild.data)
	filename = str(xmldoc.getElementsByTagName('filename')[0].firstChild.data)
	filepath = folder + filename
	
	objs = xmldoc.getElementsByTagName('object')
	boxes = []
	for obj in objs:
		class_name = obj.getElementsByTagName('name')[0]
		class_name = class_name.firstChild.data
		class_label = str(class_list[class_name])
		bndbox = obj.getElementsByTagName('bndbox')[0]
		xmin = str(bndbox.getElementsByTagName('xmin')[0].firstChild.data)
		xmax = str(bndbox.getElementsByTagName('xmax')[0].firstChild.data)
		ymin = str(bndbox.getElementsByTagName('ymin')[0].firstChild.data)
		ymax = str(bndbox.getElementsByTagName('ymax')[0].firstChild.data)
		
		boxes.append([xmin, ymin, xmax, ymax, class_label])
	return filepath, boxes

def get_class_list():
	with open('class_list.txt', 'r') as f:
		class_list = f.readlines()
		class_list = [c.strip() for c in class_list]
	class_list = dict(zip(class_list, range(len(class_list))))
	return class_list
	
if __name__ == "__main__":
	class_list = get_class_list()
	for filename in glob.glob('annotations_xml/*.xml'):
		xmldoc = minidom.parse(filename)
		filepath, boxes = get_boxes_from_xmldoc(xmldoc)
		with open('annotations_yolov3.txt', 'a+') as f:
			lines = [','.join(box) for box in boxes]
			lines = ' '.join(lines)
			lines = ' '.join([filepath, lines]) + '\n'
			f.write(lines)