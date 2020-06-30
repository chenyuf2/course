import csv
import numpy as np
import json
with open('UIUC Courses.csv', 'r') as infile:
    data = infile.readlines()
    new_data = []
    firstLine = True
    for line in data:
        if (firstLine):
            firstLine = False
        else:
            line = line.strip().split(",")
            if line[2] != "NULL":
                new_data.append(line)
    new_data = np.array(new_data)
all_courses = new_data[:,0]

courses=[]
weights={}

engineering_course_title=["AE", "BIOE", "BIOP", "CEE", "CS", "CSE", "ECE", "ENG", "IE", "INFO", "ME", "MSE", "NPRE", "PHYS", "SE", "TAM", "TE"]
for i in range(0,len(all_courses)):
    temp = all_courses[i]
    weight = len(new_data[i][2].split())
    weights[all_courses[i]]=weight
    # if temp[0:2] in engineering_course_title or temp[0:3] in engineering_course_title or temp[0:4] in engineering_course_title or temp[0:4] == "MATH":
    #     courses.append(all_courses[i])
    courses.append(all_courses[i])
print(len(courses))


data={}
data["nodes"]=[]
for i in range(0,len(courses)):
    data["nodes"].append({"name":courses[i], "weight":weights[courses[i]]})
courses_dictionary={}
for i in range(len(courses)):
    courses_dictionary[courses[i]] = i
dict = {}
link_dict={}
link_dict["links"]=[]
for i in range(len(new_data)):
    if new_data[i][0] not in dict and new_data[i][0] in courses_dictionary:
        dict[new_data[i][0]] = new_data[i][2].split()
        source_index = courses_dictionary[new_data[i][0]]
        temp = new_data[i][2].split()
        for j in range(0,int(len(temp)/2)):
            if temp[2*j]+" "+temp[2*j+1] in courses_dictionary.keys():
                target_index = courses_dictionary[temp[2*j]+" "+temp[2*j+1]]
                link_dict["links"].append({"source":source_index, "target":target_index, "weight":weights[new_data[i][0]]})
            else:
                length = len(courses_dictionary.keys())
                courses_dictionary[temp[2*j]+" "+temp[2*j+1]] = length
                data["nodes"].append({"name":temp[2*j]+" "+temp[2*j+1], "weight":1})
                link_dict["links"].append({"source":source_index, "target":length, "weight":weights[new_data[i][0]]})
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
with open('link.json', 'w') as outfile:
    json.dump(link_dict, outfile)
final_dict={"nodes": data["nodes"], "links": link_dict["links"]}
with open('graphFile.json', 'w') as outfile:
    json.dump(final_dict, outfile)
