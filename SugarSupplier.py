'''
	Name : Vishnu H Nair
	Language : Python 2.7 
	Instructions : Compile and run this program in the same directory as the given "input.txt" .
				   The final output after sorting as per given in the question would be in "output.txt"
	Examples : If the input.txt is

	           Hiranandani Gardens
	           NITIE Bombay

               The output in output.txt would be

               Hiranandani Gardens
               NITIE Bombay

	Comments : I have made intermediate files to make the program easy which would be deleted after it's purpose
'''

import json
import urllib
import os

#Reading the contents of input.txt and changing the spaces(' ') to '+' to make the formatting for HTTP Request
with open("input.txt") as infile, open("formatted.txt", "w") as outfile :
    for line in infile :
        outfile.write(" ".join(line.split()).replace(' ', '+') + "\n")

#Storing the location names of input.txt into a list for future reference 
with open("input.txt", "r") as infile :
	input_list = [line.strip() for line in infile]


i=0
with open("formatted.txt") as infile, open("distances.txt", "w") as outfile :
	#HTTP Request to return the json file
    for line in infile :
        url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + line + "&destination=IIT+Bombay"
        response = urllib.urlopen(url)

		#Storing the json file into data
        data = json.loads(response.read())

        #Check if the route is accessible by road, if not store the distance as -1
        if data["status"] == "OK" :
            outfile.write(str(i) + " " + str(data["routes"][0]["legs"][0]["distance"]["value"]) + "\n")
        else :	
            outfile.write(str(i)+ " -1\n")

        i = i + 1

#Creating a list of tuple with the index and distance
with open("distances.txt") as infile :
    data_tuple = [tuple(map(int, i.split(" "))) for i in infile]

#Sorting the data_tuple with respect to distance
distance_tuple = sorted(data_tuple, key = lambda tup: tup[1])

#Printing the ascending order of distances with the non accessible locations at the end
with open("output.txt", "w") as outfile :
	for i in range(0, len(distance_tuple)) :
		if distance_tuple[i][1] != -1 :
			outfile.write(input_list[int(distance_tuple[i][0])] + "\n")

	for i in range(0,len(distance_tuple)) : 
		if distance_tuple[i][1] == -1 :
			outfile.write(input_list[int(distance_tuple[i][0])] + "\n")

#Deleting the temporary text files which are of no use now
os.remove("formatted.txt")
os.remove("distances.txt")
