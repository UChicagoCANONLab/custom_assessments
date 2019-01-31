#Jean Salac
#Sequence Question Generator for Scratch 3. Run with the following command: python sequenceQnGen.py scratchStudioURL

import sys
import json
import requests
from pprint import pprint
import copy
import re
import random
import time
from bs4 import BeautifulSoup
import scratchAPI as sa
import navJson as nj

#Scratch Project Class.
class Project(object):
	ID = ''
	blocks = ''
	questions = ''
	username = '' #Scratch username
	lenQ7 = 4 #Num blocks in q7 script. Default is 4

	def __init__(self, ID):
		self.ID = ID
		self.blocks = {}
		self.questions = []
		self.username = ''
		self.lenQ7 = 4

	def __str__(self):
		return "Project's Name: "+ self.ID
	def __repr__(self):
		return "Project's Name: "+ self.ID

#Project Constructor
def make_project(name):
	project = Project(name)
	return project

#Question Constructor
class Question(object):
	ID = '' #Question's ID 
	scripts = [] #Scripts that are part of the question
	scrBlks= [] #Question scripts converted to Scratchblocks syntax


	def __init__(self, ID):
		self.ID = ID
		self.scripts = []
		self.scrBlks = []

	def __str__(self):
		return "Question ID: "+ self.ID
	def __repr__(self):
		return "Question ID: "+ self.ID

#Question Constructor
def make_question(name):
	question = Question(name)
	return question

#Custom question functions. TODO: Add excluded opcodes
#Question 3: Find 1 green flag script, 1 spriteClicked, or 1 keyPressed from their code. Hard-code 1 spriteClicked script.
#Check if 3-4 blocks long, including the hat block, and no excluded blocks.
#def custom_q3(Question, Project):


#Question 6: Find a "When Green Flag". No loops, conditionals, variables, play sound.
#Check if 4 blocks long, including the GF block, and no excluded blocks.
#Takes in project and adds custom question to project
#def custom_q6(Project):


#Question 7: Find a spriteClicked or GreenFlag. No loops, conditionals, variables, play sound.
#Check if 2-4 blocks long, including the GF block, and no excluded blocks.
#Takes in project and adds custom question to project
#def custom_q7(Project):


def main():

	#Create a global lists of projects
	projects = []
	#Create a csv of all Scratch usernames and project IDs
	studentInfo = open('students.csv','w+')

	#Take in Scratch Studio URL
	studioURL = sys.argv[1]

	#Convert studio URL to the one necessary for scraping Scratch usernames and project IDs.
	#Pull projects until page number does not exist

	#Initialize studio URL and requests
	pageNum = 1
	studio_api_url = sa.studio_to_API(studioURL,pageNum)
	r = requests.get(studio_api_url, allow_redirects=True)

	#While the studio API URL exists, pull all the projects
	while(r.status_code == 200):
		studio_html = r.content
		studio_parser = BeautifulSoup(studio_html, "html.parser")


		for project in studio_parser.find_all('li'):
			#Find the span object with owner attribute
			span_string = str(project.find("span","owner"))
			
			#Pull out scratch username
			scratch_username = span_string.split(">")[2]
			scratch_username = scratch_username[0:len(scratch_username)-3]
			
			#Get project ID
			proj_id = project.get('data-id')

			#Read json file from URL. Convert Scratch URL to Scratch API URL, then read file.
			apiURL = sa.create_API_URL(proj_id)
			json_stream = requests.get(apiURL, allow_redirects=True)
			json_filename = scratch_username+".json"
			open(json_filename, 'wb').write(json_stream.content)
			json_data= open(json_filename, "r")
			data = json.load(json_data)
			json_data.close()

			#Print to students.csv
			studentInfoLine = scratch_username+","+"https://scratch.mit.edu/projects/"+proj_id+"/"
			print>>studentInfo, studentInfoLine


			#Create a project object for this project
			newProject = make_project(proj_id)
			newProject.username = scratch_username

			#Add project blocks 
			projInfo = data['targets']
			for item in projInfo:
				blocks = item['blocks']
				for blockName in blocks:
					blockInfo=blocks[blockName]
					#Add to projects' blocks dictionary: key=blockName, value=blockInfo
					newProject.blocks[blockName] = blockInfo
				

			#Add project to the global list of projects
			projects.append(newProject)

		pageNum+=1
		studio_api_url = sa.studio_to_API(studioURL,pageNum)
		r = requests.get(studio_api_url, allow_redirects=True)

	#List of projects with candidate code for each question
	q1_cands = [] #Check if 2-4 blocks long, including the hat block, and no excluded blocks. 1 green flag script, 1 spriteClicked, or 1 keyPressed
	q6_cands = [] #Check if exactly 4 blocks long, including the GF block, and no excluded blocks. Green flag only
	q7_cands = [] #Check if 2-4 blocks long, including the GF block, and no excluded blocks. spriteClicked or green flag

	#Find projects with candidate code
	for project in projects:
		greenFlags= nj.find_blocks(project.blocks,'event_whenflagclicked')
		spriteClickeds = nj.find_blocks(project.blocks,'event_whenthisspriteclicked')
		keyPresseds = nj.find_blocks(project.blocks,'event_whenkeypressed')

		#If there are any green flag blocks in the project
		if len(greenFlags) > 0:
			for block in greenFlags:
				gfScript=nj.create_script(project.blocks, block)
				if len(gfScript)==4:
					q6_cands.append(project)
					break
				if len(gfScript)>=2 and len(gfScript)<=4:
					q1_cands.append(project)
					q7_cands.append(project)
					break
			
		#If there are any sprite clicked blocks in the project
		if len(spriteClickeds) > 0:
			for block in spriteClickeds:
				spriteScript=nj.create_script(project.blocks, block) 
				if len(spriteScript)>=2 and len(spriteScript)<=4:
					if project not in q1_cands:
						q1_cands.append(project)
					if project not in q7_cands:
						q7_cands.append(project)
					break

		#If there are any key pressedblocks in the project
		if len(keyPresseds) > 0:
			for block in keyPresseds:
				keyScript=nj.create_script(project.blocks, block) 
				if len(keyScript)>=2 and len(keyScript)<=4:
					if project not in q1_cands:
						q1_cands.append(project)
					break


	for project in q1_cands:
		print(project.username)

	for project in q6_cands:
		print(project.username)

	for project in q7_cands:
		print(project.username)


if __name__ == '__main__':
	main()