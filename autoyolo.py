import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import argparse
import subprocess
import shlex
import re
import csv

command = "!./darknet detector test data/obj.data cfg/yolov3_custom.cfg yolov3_custom_4000.weights pic.jpeg -thresh 0.05"


			 		# test if list dir is all images –– may be that you are reading folder (./Asymptomatic/..)
yolo_arg = shlex.split(command)  	# generate sequence of args for subprocess.popen or maybe use subprocess.run 
									# if easeir?

print(yolo_arg)

class Image():

	number_of_corona  = 0	# consider inherited class variables here? for super(PictureBook).__init__....
	number_of_disease1 = 0
	number_of_disease2 = 0

	def __init__(self, index, filename):
		self.index = index
		self.filename = filename
		self.corona = 0	#class variable for number of corona points	
		self.disease1 = 0	#class variable similar
		self.disease2 = 0
		self.coronalist = []
		self.d1list = []
		self.d2list = []

	def getIndex(self):
		return self.index

	# def add_data(self, string, type):
	# 	if type == 0:
	# 		disease = self.corona
	# 		length = Image.number_of_corona
	# 	elif type == 1:
	# 		disease = self.disease1
	# 	elif type == 2:
	# 		disease = self.disease2
	# 		length = Image.number_of_disease2
	# 	else:
	# 		 print("exception: type neither 0, 1, nor 2")

	# 	parsed_values = [int(value) for value in string.split() if value.isdigit()]
	# 	if(len(parsed_values) == 0):
	# 		return 0

	# 	disease.append(parsed_values[0])
	# 	print(length)
	# 	print(Image.number_of_disease1)
	# 	if len(disease) > length:
	# 		length += 1
	# 		print("length %d" %length)
	# 		print(Image.number_of_disease1)

	# TODO: lot of redundant code——use decorator somewhere here when u get the chance
	# @corona_decorator?
	def add_corona(self, string, type):
		parsed_values = [int(value[:-1]) for value in string.split() if value[:-1].isdigit()]
		print(parsed_values)
		# parsed_values = int(re.search(r'\d+', string).group())
		self.coronalist.append(parsed_values[0])
		self.corona += parsed_values[0]
		# if len(self.corona) > Image.number_of_corona:
		# 	Image.number_of_corona = len(self.corona)


		
	def add_d1(self, string, type):
		parsed_values = [int(value[:-1]) for value in string.split() if value[:-1].isdigit()]
		print(parsed_values)
		# parsed_values = int(re.search(r'\d+', string).group())
		self.d1list.append(parsed_values[0])
		self.disease1 += parsed_values[0]
		# if len(self.disease1) > Image.number_of_disease1:
			# Image.number_of_disease1 = len(self.disease1)
		# TODO: create array to add digits of disease1
	def add_d2(self, string, type):
		parsed_values = [int(value[:-1]) for value in string.split() if value[:-1].isdigit()]
		print(parsed_values)
		# parsed_values = int(re.search(r'\d+', string).group())

		self.d1list.append(parsed_values[0])
		self.disease2 += parsed_values[0]
		# if len(self.disease1) > Image.number_of_disease1:
		# 	Image.number_of_disease1 = len(self.disease1)

		''' TODO: create array to add digits of disease2
		make sure to change Image.number_of_corona as well
		'''
	def get_corona(self):
		return self.corona




	def getd1(self):
		return self.disease1

	def getd2(self):
		return self.disease2

	def present_data(self):
		print(f'corona: {self.corona}', end = ", ")
		print(f'disease1: {self.disease1}', end = ", ")
		print(f'disease2: {self.disease2}', end = ", ")
		print(self.coronalist)
		print(self.d1list)
		print(self.d2list)

		print(self.filename, end="\n\n")
		print(self.index)


		

parser = argparse.ArgumentParser(prog="dataparse", usage = '%(prog)s [-h] path', 
								description = "Collect percentages for data and make table")

parser.add_argument('Path', metavar='path', type=str, help="path of folder")

parser.add_argument('--program', metavar='program comman', type=str, 
					help="path of executable YOLO")

arguments = parser.parse_args()

file_path = arguments.Path   
print(file_path)

files = [f for f in os.listdir(file_path) if os.path.isfile( file_path + "/" + f ) and (os.path.splitext( file_path + "/" + f )[1] == ".jpg" or  os.path.splitext( file_path + "/" + f )[1] == ".jpeg"  or  os.path.splitext( file_path + "/" + f )[1] == ".png" or os.path.splitext( file_path + "/" + f )[1] == ".JPG")]

print("\n".join(files))
print("\n\n\n\n\n lenght of files: {} \n\n\n\n".format(len(files)))

number_files = len(files)

image_data = []
os.mkdir('./Collected_dataR')



def formatBar(Image, num):

	index = Image.getIndex() + 1
	bar = 25 * ["*"]
	

	percent = (index / num) * 100 
	substitute = int( (percent // 4) ) -1 
	print("substitue {}".format(substitute))

	if substitute >= 0: 
		bar[0 : substitute] = substitute * ["-"]
		bar[substitute] = ">"
		print("[{}]   {}% completed".format( "".join(bar), percent ))
	else:
		print("[{}]   {}% completed".format("".join(bar), percent ))



for i in enumerate(files):
	image_data.append(Image(i[0], i[1]))
	yolo_arg[len(yolo_arg) - 3] = file_path + '/' + i[1]
	argument = " ".join(yolo_arg)

	print(argument)
	test = subprocess.run(argument, shell=True, stdout=subprocess.PIPE)
 
	for line in str(test.stdout).split("\n"):
		if line.startswith('Coronavirus: '):
			print(line)
			image_data[i[0]].add_corona(line, 0)
		elif line.startswith('Non-COVID GGO: '):
			image_data[i[0]].add_d1(line, 1)
		elif line.startswith('COVID-DQ:'):
			image_data[i[0]].add_d2(line, 2)

	image_data[i[0]].present_data()

	formatBar( image_data[i[0]], number_files )



	# with open(f'../../Collected_data/final{i[0]}.csv', 'w', newline = '') as roshan:

	# 	w = csv.writer(roshan)

	# 	w.writerow([image_data[ i[0] ].get_corona, image_data[ i[0] ].getd1, image_data[ i[0] ].getd2 ])



	# running = subprocess.run(yolo_arg, args, shell=True, stdout=subprocess.PIPE, text=True) 		# run command for each image and store



with open('../Collected_dataR/final.csv', 'w', newline = '') as r:

	w = csv.writer(r)
	w.writerow(["Name", "Coronavirus", "Non-COVID GGO", "COVID-DQ"])

	for t in image_data:
		
		w.writerow([t.filename, t.corona, t.disease1, t.disease2])



#pipe stdout from YOLO to dataparse

# coronavirus = []
# disease1 = []

# disease2 = []


# def addData(diseaseArr, line):
# 	# TODO: fix instance where there are no parsed_values... or not I guess?
# 	parsed_values = [int(value) for value in line.split() if value.isdigit()]

# 	diseaseArr.append(parsed_values[0])


# for line in sys.stdin:
# 	if line.startswith('Coronavirus: '):
# 		# print(line)
# 		addData(coronavirus, line)
# 	elif line.startswith('disease1: '):
# 		addData(disease1, line)
# 	elif line.startswith('disease2: '):
# 		addData(disease2, line)



# #do the data stuff here



# if __name__ == "__main__":

# 	hi = Image(0, "hello")
# 	hi.add_corona("123", 0)
# 	hi.add_corona("1566", 0)
# 	hi.add_corona("6245", 0)
# 	hi.add_corona("32512", 0)

# 	hi.add_d1("1342", 1)
# 	hi.add_d1("h5 5", 1)
# 	hi.add_d1("j7ju 67", 1)


# 	hi.add_d2("13", 2)
# 	hi.add_d2("46", 2)
# 	hi.add_d2("u 77", 2)

# 	print("corona %s" %hi.corona)
# 	print("disease1 %s" %hi.disease1)
# 	print("disease2 %s" %hi.disease2)
# 	print(Image.number_of_disease1)
# 	print(Image.number_of_corona)
# 	print(Image.number_of_disease2)





