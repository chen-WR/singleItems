import os 
from os import path
import shutil 
import sys

def checkDuplicate(folderpath,hashmap={}):
	global count
	global remaining
	all_files = len([path.isfile(path.join(folderpath,file)) for file in os.listdir(folderpath)])
	remaining += all_files
	print(f"Adding {all_files} files from directory >>>>>>>>>> total: {remaining}")
	with os.scandir(folderpath) as streams:
		for entry in streams:
			if entry.is_file():
				with open(entry.path,'rb') as f:
					byte = bytearray(f.read())
					code = hash(str(byte[0:len(byte):200]))
					# code = hash(str(byte[0:100])) + hash(str(byte[(len(byte)//2)-100:(len(byte)//2)+100])) + hash(str(byte[(len(byte)-100):len(byte)]))
				if not hashmap.get(code):
					hashmap[code] = entry.name
				else:
					shutil.move(entry.path,path.join(new_path,entry.name))
					count += 1
					print(f"Duplicate file found: {entry.name}")
				remaining -= 1
				print(f"Remain: {remaining}") 	
			elif entry.is_dir():
				checkDuplicate(entry.path,hashmap)




try:
	folder = sys.argv[1]
except IndexError:
	folder = None
	print("Argument 1 of directory required")

if folder is not None:
	count = 0
	remaining = 0
	base_dir = path.dirname(folder)
	new_path = path.join(base_dir,"duplicated")
	os.mkdir(new_path) if not path.exists(new_path) else None
	checkDuplicate(folder)
	print("Total duplicate file: ",count)