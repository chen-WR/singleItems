### Provide a origin folder for this script to recursivly going through all files and subfolders
### For each file that is not dir, file goes to byte array and reading multiple byte from those array, and hash it
### compare other files to the hashmap and if it already exists, move the file to duplicated folder that is created

# Non english path potential fix:  img = cv2.imdecode(np.fromfile('测试目录/test.jpg', dtype=np.uint8), cv2.IMREAD_UNCHANGED)

import os 
from os import path
import shutil 
import sys
import cv2
import numpy as np

def checkDuplicate(folderpath,hashmap={}):
	global remaining
	remaining += len([path.isfile(path.join(folderpath,file)) for file in os.listdir(folderpath)])
	with os.scandir(folderpath) as streams:
		for entry in streams:
			if entry.is_file():
				with open(entry.path,'rb') as f:
					byte = bytearray(f.read())
					code = hash(str(byte[0:len(byte):200]))
				if not hashmap.get(code):
					hashmap[code] = entry.path
				else:
					if not express:
						file_format = checkImageOrVideo(entry.path)
						if file_format == "image":
							showImage(hashmap[code],entry.path)
						elif file_format == "video":
							showVideo(hashmap[code],entry.path)
						else:
							print("Format not supported to show")
						if manual:
							ans = input("Move the duplicate, Enter Key to continue, n to not move? >>>>>")
							if not ans:
								shutil.move(entry.path,path.join(new_path,entry.name))
								print(f"Duplicate file found: {entry.name}")
						elif not manual:
							shutil.move(entry.path,path.join(new_path,entry.name))
							print(f"Duplicate file found: {entry.name}")
					else:
						shutil.move(entry.path,path.join(new_path,entry.name))
						print(f"Duplicate file found: {entry.name}")
				remaining -= 1
				print(f"Remain: {remaining}") 	
			elif entry.is_dir():
				checkDuplicate(entry.path,hashmap)

def checkImageOrVideo(file):
	video_format = ["WEBM","MPG","MP2","MPEG","MPE","MPV","OGG","MP4","M4P","M4V","AVI","WMV","MOV","QT","FLV","SWF","AVCHD"]
	image_format = ["rgb","pbm","pgm","ppm","tiff","rast","xbm","jpeg","jpg","bmp","png","webp","exr"]
	extension = file.split(".")[1]
	if extension.lower() in image_format:
		return "image"
	elif extension.upper() in video_format:
		return "video"
	else:
		return None

def showImage(origin,duplicate):
	title1,title2 = origin.split("\\")[-1],duplicate.split("\\")[-1]
	pic1,pic2 = cv2.imread(origin),cv2.imread(duplicate)
	try:
		pic1 = cv2.resize(pic1,(400,400))
	except Exception as e:
		print(e)
		pic1 = None
		error_list.append(origin)
	try:	
		pic2 = cv2.resize(pic2,(400,400))
	except Exception as e:
		print(e)
		pic2 = None
		error_list.append(duplicate)
	if pic1 is not None and pic2 is not None:
		try:
			picture = np.concatenate((pic1,pic2),axis=1)
			cv2.imshow(f"{title1} VS {title2}",picture)
		except ValueError:
			cv2.imshow(f"origin: {title1}",pic1)
			cv2.imshow(f"duplicate: {title2}",pic2)
		if manual:
			cv2.waitKey(0)
		elif not manual:
			cv2.waitKey(500)
		cv2.destroyAllWindows()

def showVideo(origin,duplicate):
	title1,title2 = origin.split("\\")[-1],duplicate.split("\\")[-1]
	cap1,cap2 = cv2.VideoCapture(origin),cv2.VideoCapture(duplicate)
	duration1,duration2 = (int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)) // int(cap1.get(cv2.CAP_PROP_FPS))),(int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)) // int(cap2.get(cv2.CAP_PROP_FPS)))  
	cap1.set(1,duration1//2)
	cap2.set(1,duration2//2)
	ret1, frame1 = cap1.read()
	ret2, frame2 = cap2.read()
	try:
		frame1 = cv2.resize(frame1,(400,400))
	except Exception as e:
		print(e)
		frame1 = None
		error_list.append(origin)
	try:	
		frame2 = cv2.resize(frame2,(400,400))
	except Exception as e:
		print(e)
		frame2 = None
		error_list.append(duplicate)
	if frame1 is not None and frame2 is not None:
		try:
			picture = np.concatenate((frame1,frame2),axis=1)
			cv2.imshow(f"{title1} VS {title2}",picture)
		except ValueError:
			cv2.imshow(f"origin: {title1}",frame1)
			cv2.imshow(f"duplicate: {title2}",frame2)
		if manual:
			cv2.waitKey(0)
		elif not manual:
			cv2.waitKey(500)
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
	remaining = 0
	error_list = []
	express = input("Express: Speed through each file and move it? y/n >>>>")
	user_check = input("User check each file different, ignored if express? y/n >>>>")
	express = True if express == "y" else False
	manual = True if user_check == "y" else False
	base_dir = path.dirname(folder)
	new_path = path.join(base_dir,duplicate_folder)
	os.mkdir(new_path) if not path.exists(new_path) else None
	checkDuplicate(folder)
	for error in error_list:
		print(error)