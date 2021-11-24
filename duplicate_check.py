### Provide a origin folder for this script to recursivly going through all files and subfolders
### For each file that is not dir, file goes to byte array and reading multiple byte from those array, and hash it
### compare other files to the hashmap and if it already exists, move the file to duplicated folder that is created

import os 
from os import path
import shutil 
import sys
import cv2
import numpy as np

def checkDuplicate(folderpath,hashmap={}):
	global count,remaining
	all_files = len([path.isfile(path.join(folderpath,file)) for file in os.listdir(folderpath)])
	remaining += all_files
	print(f"Adding {all_files} files from directory >>>>>>>>>> total: {remaining}")
	with os.scandir(folderpath) as streams:
		for entry in streams:
			if entry.is_file():
				with open(entry.path,'rb') as f:
					byte = bytearray(f.read())
					code = hash(str(byte[0:len(byte):200]))
				if not hashmap.get(code):
					hashmap[code] = entry.path
				else:
					check = checkImageOrVideo(entry.path)
					if check == "image":
						showImage(hashmap[code],entry.path)
					elif check == "video":
						showVideo(hashmap[code],entry.path)
					else:
						print("Format not supported to show")
					ans = input("Move the duplicate, Enter Key to continue, n to not move? >>>>>")
					if not ans:
						shutil.move(entry.path,path.join(new_path,entry.name))
						count += 1
						print(f"Duplicate file found: {entry.name}")
				remaining -= 1
				print(f"Remain: {remaining}") 	
			elif entry.is_dir():
				checkDuplicate(entry.path,hashmap)

def checkImageOrVideo(file):
	video_format = ["WEBM","MPG","MP2","MPEG","MPE","MPV","OGG","MP4","M4P","M4V","AVI","WMV","MOV","QT","FLV","SWF","AVCHD"]
	image_format = ["rgb","gif","pbm","pgm","ppm","tiff","rast","xbm","jpeg","jpg","bmp","png","webp","exr"]
	extension = file.split(".")[1]
	if extension.lower() in image_format:
		return "image"
	elif extension.upper() in video_format:
		return "video"
	else:
		return None

def showImage(origin,duplicate):
	pic1,pic2 = cv2.imread(origin),cv2.imread(duplicate)
	try:
		picture = np.concatenate((origin,duplicate),axis=1)
		cv2.imshow("left is origin, right is duplicate",picture)
	except ValueError:
		cv2.imshow("origin",pic1)
		cv2.imshow("duplicate",pic2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def showVideo(origin,duplicate):
	cap1,cap2 = cv2.VideoCapture(origin),cv2.VideoCapture(duplicate)
	duration1,duration2 = (int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)) // int(cap1.get(cv2.CAP_PROP_FPS))),(int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)) // int(cap2.get(cv2.CAP_PROP_FPS)))  
	cap1.set(1,duration1//2)
	cap2.set(1,duration2//2)
	ret1, frame1 = cap1.read()
	ret2, frame2 = cap2.read()
	try:
		picture = np.concatenate((frame1,frame2),axis=1)
		cv2.imshow("left is origin, right is duplicate",picture)
	except ValueError:
		cv2.imshow("origin",frame1)
		cv2.imshow("duplicate",frame2)
	cv2.waitKey(0)
	cap1.release()
	cap2.release()
	cv2.destroyAllWindows()

try:
	folder = sys.argv[1]
except IndexError:
	folder = None
	print("Argument 1 of directory required")

try:
	duplicate_folder = sys.argv[2]
except IndexError:
	duplicate_folder = "duplicated"
	print("No duplicate folder name provided, default will be used")

if folder is not None:
	count = 0
	remaining = 0
	base_dir = path.dirname(folder)
	new_path = path.join(base_dir,duplicate_folder)
	os.mkdir(new_path) if not path.exists(new_path) else None
	checkDuplicate(folder)
	print("Total duplicate file: ",count)

