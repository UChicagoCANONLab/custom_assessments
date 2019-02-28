#!/usr/bin/python
from subprocess import call
import os
import json
import re
# import crop_img

scratch_projects = ["https://scratch.mit.edu/studios/5831048/",
"https://scratch.mit.edu/studios/5831042/",
"https://scratch.mit.edu/studios/5830937/",
"https://scratch.mit.edu/studios/5831053/",
"https://scratch.mit.edu/studios/5831055/",
"https://scratch.mit.edu/studios/5831059/",
"https://scratch.mit.edu/studios/5831066/",
"https://scratch.mit.edu/studios/5831076/",
"https://scratch.mit.edu/studios/5752419/"]

project_names = ["SES_Class 3A_(304-21)",
"SES_Class_3B_(305-21)",
"SES_Class_3C_(307-22)",
"SES_Class_4A_(302-24)",
"SES_Class_4B_(309-24)",
"SES_Class_4C_(300-23*)",
"SES_Class_5A_(311-23)",
"SES_Class_5B_(312-23)",
"GP_3rd"]

i = 0
lsp = len(scratch_projects)

for i in range(lsp):
	project = scratch_projects[i]
	# call(["python", "sequenceQnGen.py", project])

	call(["python3", "parse_json.py"])

	img_directory = "img_files/"

	directory = "scripts/"
	files = os.listdir(directory)
	if '.DS_Store' in files:
		files.remove('.DS_Store')

	c = 0
	filedir = {}
	for filename in files:
		filedir[c] = filename
		if filename[-3:] == ".js":
			call(["node", directory + filename])
			old_name = img_directory + "scratchblocks.png"
			new_name = img_directory + filename[:-3] + ".png"
			if "script" not in filename:
				new_name = img_directory + filename[:-3] + "_script0" + ".png"
			os.rename("..//../Downloads/scratchblocks.png", "img_files/scratchblocks.png")
			os.rename(old_name, new_name)
			call(["python3", "crop_img.py", new_name, img_directory])
			1/0
			c += 1

	writedir = open(project_names[i] + "_filedirectory.json", "w")
	writedir.write(json.dumps(filedir))

	call(["python3", "maketex.py"])

	files = os.listdir('.')
	if '.DS_Store' in files:
		files.remove('.DS_Store')

	i = 0
	for filename in files:
		if filename[-3:] == "tex":
			call(["pdflatex", filename])
			i += 1

	# Clean up
	files = os.listdir('.')
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	pdflist = ["pdfunite"]
	for filename in files:
		if filename[-3:] == "pdf":
			pdflist.append(filename)

	pdflist.append(project_names[i] + ".pdf")

	file_extensions = ["tex", "aux", "log", "pdf"]
	archive = "archive/"
	for filename in files:
		file_type = filename[-3:]
		if file_type in file_extensions:
			os.rename(filename, archive + filename)

	dir1 = 'json_files/'
	files = os.listdir('./' + dir1)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		os.rename(dir1 + filename, archive + filename)

	dir2 = 'user_json_files/'
	files = os.listdir('./' + dir2)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		os.rename(dir2 + filename, archive + filename)

	dir3 = 'scripts/'
	files = os.listdir('./' + dir3)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		if filename[-3:] == ".js":
			os.rename(dir3 + filename, archive + filename)

	dir4 = 'cleaned_json/'
	files = os.listdir('./' + dir4)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		os.rename(dir4 + filename, archive + filename)

	break
