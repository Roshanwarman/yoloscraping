import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import argparse
import subprocess
import shlex

command = "./darknet detector test data/obj.data cfg/yolov3_custom.cfg 3000.weights pic.jpeg"


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
		self.corona = []	#class variable for number of corona points	
		self.disease1 = []	#class variable similar
		self.disease2 = []

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
		parsed_values = [int(value) for value in string.split() if value.isdigit()]
		self.corona.append(parsed_values[0])
		if len(self.corona) > Image.number_of_corona:
			Image.number_of_corona = len(self.corona)


		
	def add_d1(self, string, value):
		parsed_values = [int(value) for value in string.split() if value.isdigit()]
		self.disease1.append(parsed_values[0])
		if len(self.disease1) > Image.number_of_disease1:
			Image.number_of_disease1 = len(self.disease1)
		# TODO: create array to add digits of disease1
	def add_d2(self, string, value):
		parsed_values = [int(value) for value in string.split() if value.isdigit()]
		self.disease2.append(parsed_values[0])
		if len(self.disease1) > Image.number_of_disease1:
			Image.number_of_disease1 = len(self.disease1)
		''' TODO: create array to add digits of disease2
		make sure to change Image.number_of_corona as well
		'''


parser = argparse.ArgumentParser(prog="dataparse", usage = '%(prog)s [-h] path', 
								description = "Collect percentages for data and make table")

parser.add_argument('Path', metavar='path', type=str, help="path of folder")

parser.add_argument('--program', metavar='program comman', type=str, 
					help="path of executable YOLO")

arguments = parser.parse_args()

file_path = arguments.Path   
print(file_path)
# print("\n".join(os.listdir(file_path)))





files = [f for f in os.listdir(file_path) if os.path.isfile( file_path + "/" + f ) ]

print("\n".join(files))

number_files = len(files)

image_data = []

for i in enumerate(files):
	#	(i, file_i)
	image_data.append(Image(i[0], i[1]))
	yolo_arg[len(yolo_arg) - 1] = file_path + '/' + i[1]
	print(yolo_arg)

	# a = ['ls', '-l']

	test = subprocess.run(yolo_arg, shell=True, capture_output=True, text=True)
	print(test.stdout)











	# running = subprocess.run(yolo_arg, args, shell=True, stdout=subprocess.PIPE, text=True) 		# run command for each image and store




''' 
		Each Image is represented by an Image object which contains relevant information
		such as the maximum number of corona datapoints, etc..
'''







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





