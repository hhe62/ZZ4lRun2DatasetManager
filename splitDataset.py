import glob
import subprocess
import json

############################
## USAGE
## set the variables below, and run "python splitDataset.py"
## fullPath should be strictly of the form /full path/* with only one "*" and it is at the end
## The data files in /full path/ will be splitted and copied into several folders


############################
## variables:
fullPath = "testSplit/original/*" #! Need to have the form of /full path/*
dir = fullPath.rsplit("/*",1)[0]
dataset = "ZZJJTo4L-EWK" #! Name of dataset to put in json file
plot_group = "zzjj4l-ewk" #! Name of plot_group to put in json file
split = 5 #! Number of subfolders
outputList = True #! Write a json file
outputname = "splitEWK.json" #! Name of output json file
turnoffWrite = True #! Turn off write permission of the original folder to avoid accidental modification
resumeWrite = False #! Recover write permission of the original folder at the end
############################

files = glob.glob(fullPath)

#! Turn off write permission of the folder to avoid accidental modification
if turnoffWrite:
    nowrite = subprocess.run("chmod -R u-w %s"%dir,shell=True,capture_output=True,text=True,check=True)
    print(nowrite.stdout)

#! Create folders
for n in range(0,split):
    temp_mkdir = subprocess.run("mkdir -p %s"%(dir+"_split"+str(n)),shell=True,capture_output=True,text=True,check=True)
    print(temp_mkdir.stdout)

#! Split and copy files to folders
for ind, file in enumerate(files):
    nd = ind % split
    temp_cp = subprocess.run("rsync -avh %s %s"%(file, dir+"_split"+str(nd)),shell=True,capture_output=True,text=True,check=True)
    print(temp_cp.stdout)

if outputList:
    obj = {}
    for n in range(0,split):
        obj[dataset+str(n)] = {}
        obj[dataset+str(n)]["file_path"] = dir+"_split"+str(n)+"/*"
        obj[dataset+str(n)]["plot_group"] = plot_group
    
    with open(outputname,'w') as output_file:
        json.dump(obj,output_file,indent=4)
        
if turnoffWrite and resumeWrite:
    #! Turn back on write permission of the folder 
    nowrite2 = subprocess.run("chmod -R u+w %s"%dir,shell=True,capture_output=True,text=True,check=True)
    print(nowrite2.stdout)
