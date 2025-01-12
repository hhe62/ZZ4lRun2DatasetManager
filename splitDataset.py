import glob
import subprocess
import json
import sys

############################
## USAGE
## set the variables below, and run "python splitDataset.py"
## or use "python splitDataset.py path dataset plotgroup"
## fullPath should be strictly of the form /full path/* with only one "*" and it is at the end
## The data files in /full path/ will be splitted and copied into several folders
############################

## variables:

#fullPath = "/hdfs/store/user/hhe62/ZZ4l2018AnalysisJobs_2022-10-26/2022-10-26-ZZJJTo4L-EWK-ZZ4l2018-loosePreselectionTo4lmass-v1/*" #! Need to have the form of /full path/*
fullPath = "/hdfs/store/user/hhe62/ZZ4l2018AnalysisJobs_2022-10-26/2022-10-26-zz4l-powheg-ZZ4l2018-loosePreselectionTo4lmass-v1/*"
if len(sys.argv)>1:
    fullPath = sys.argv[1]
dir = fullPath.rsplit("/*",1)[0]

#! Name of dataset to put in json file
dataset = "zz4l-powheg" #"ZZJJTo4L-EWK"
if len(sys.argv>2):
    dataset = sys.argv[2] 

#! Name of plot_group to put in json file
plot_group = "qqZZ_powheg" #"zzjj4l-ewk" 
if len(sys.argv>3):
    plot_group = sys.argv[3] 

split = 12 #! Number of subfolders
outputList = True #! Write a json file
outputname = "split%s.json"%dataset #! Name of output json file
turnoffWrite = False #! Turn off write permission of the original folder to avoid accidental modification
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
    temp_cp = subprocess.run("cp %s %s"%(file, dir+"_split"+str(nd)),shell=True,capture_output=True,text=True,check=True)
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

print("Dataset splitting done.")
