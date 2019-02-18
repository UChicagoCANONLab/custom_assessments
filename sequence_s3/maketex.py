import os
import pandas as pd

def all_users(filename):

	df = pd.read_csv(filename, header=None)
	names = df.iloc[:,0]

	return names.tolist()

def create_assessment(custom_directory, user, q3, q6, q7, img_dir, img_list):

	custom_am = open("custom_assessments/"+user+".tex", "w")
	assessment = []
	n_questions = user + " has custom questions for: "

	# Header
	hf = open(custom_directory+"header.tex")
	header = hf.readlines()
	for h in header:
		if "Scratch Username: " in h:
			username = h.split("Scratch Username: ")
			line = "Scratch Username: " + user + " " + username[1]
		else:
			line = h
		assessment.append(line)

	# Question 1 and 2
	q12f = open(custom_directory+"q12.tex")
	q12lines = q12f.readlines()
	for line in q12lines:
		assessment.append(line)

	# Question 3
	q3f = open(custom_directory+"q3.tex")
	q3lines = q3f.readlines()
	if user in q3:
		n_questions += " Q3"
		q3lines = custom_question(q3lines, user, img_dir, img_list)
	for line in q3lines:
		assessment.append(line)

	# Question 4 and 5
	q45f = open(custom_directory+"q45.tex")
	q45lines = q45f.readlines()
	for line in q45lines:
		assessment.append(line)

	# Question 6
	q6f = open(custom_directory+"q6.tex")
	q6lines = q6f.readlines()
	if user in q6:
		n_questions += " Q6"
		q6lines = custom_question(q6lines, user, img_dir, img_list)
	for line in q6lines:
		assessment.append(line)

	# Question 7
	q7f = open(custom_directory+"q7.tex")
	q7lines = q7f.readlines()
	if user in q7:
		n_questions += " Q7"
		q7lines = custom_question(q7lines, user, img_dir, img_list)
	for line in q7lines:
		assessment.append(line)

	for l in assessment:
		custom_am.write(l)
	print(n_questions)

	custom_am.close()
	hf.close()
	q12f.close()
	q3f.close()
	q45f.close()
	q6f.close()
	q7f.close()

def custom_question(qlines, user, img_directory, img_list):

	input_img = {}

	for i in img_list:
		img = i.split("_")
		if img[0] == user:
			c = i[len(i)-5]
			input_img[c] = [i]

	cust_q = []

	img_counter = 0
	for l in qlines:
		gen_img = str(img_counter) + ".png"
		if gen_img in l:
			if str(img_counter) in input_img:
				img = input_img[str(img_counter)]
				lines = l.split("{")
				lines = lines[1].split("}")
				cust_img = user + "_" + lines[0]
				newl = l.replace(lines[0], cust_img)
				cust_q.append(newl)
				img_counter += 1
		else:
			cust_q.append(l)

	return cust_q

all_students = all_users("students.csv")
q3_students = all_users("q3_custom.csv")
q6_students = all_users("q6_custom.csv")
q7_students = all_users("q7_custom.csv")
custom_directory = "custom_scratch3/"
img_directory = "cropped_img_files"
img_list = os.listdir(img_directory)
if '.DS_Store' in img_list:
	imgs.remove('.DS_Store')
for student in all_students:
	create_assessment(custom_directory, student, q3_students, 
		q6_students, q7_students, img_directory, img_list)
