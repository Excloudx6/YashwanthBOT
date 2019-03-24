import urllib.request
import os
import json

dir_name="dat"
try:
    os.mkdir(dir_name)
    print("Created directory '%s'"%dir_name)
except:
    print("Data directory exists")

ndir=dir_name+"/"

facts="https://raw.githubusercontent.com/bebe-morse/YashwanthBOT/master/dat/facts.txt"
trivia="https://raw.githubusercontent.com/bebe-morse/YashwanthBOT/master/dat/trivia.txt"
anagram="https://raw.githubusercontent.com/bebe-morse/YashwanthBOT/master/dat/wordlist.txt"
swears="https://raw.githubusercontent.com/bebe-morse/YashwanthBOT/master/dat/swears.txt"
food="https://raw.githubusercontent.com/bebe-morse/YashwanthBOT/master/dat/foodIU.txt"

urls=[facts,trivia,anagram,swears,food]
def write_file(url, path):
    try:
        urllib.request.urlretrieve(url, path)
        print(chop + " has successfully been written inside %s\n"%dir_name)
    except:
        print("Could not write " + chop + " to %s\n"%dir_name)
for url in urls:
    
    chop=url.split("/")[-1]
    path=ndir+chop
    print("Writing " + chop + ". Please be patient\n")
    try:
        with open(path, "r") as f:
            print(chop + " already exists inside %s\n"%dir_name)
    except:
        write_file(url, path)
        
jsonsfiles=["stats.txt", "statsbackup.txt", "jobs.txt"]
plaintextfiles=["currentnumber.txt", "dailyreps.txt", "dailynegreps.txt", "claimedusers.txt"]
for jf in jsonsfiles:
    path=ndir+jf
    print("Writing " + jf + ". Please be patient\n")
    try:
        with open(path, "r") as f:
            print(jf + " already exists\n")
    except:
        try:
            with open(path, "w") as f:
                f.write(json.dumps({}))
            print(jf+" has been written to %s\n"%dir_name)
        except:
            print("Could not write " + jf + " to %s\n"%dir_name)

for ptf in plaintextfiles:
    path=ndir+ptf
    print("Writing " + ptf + ". Please be patient\n")
    try:
        with open(path, "r") as f:
            print(ptf + " already exists\n")
    except:
        try:
            with open(path, "w") as f:
                f.write("")
            print(ptf+" has been written to %s\n"%dir_name)
        except:
            print("Could not write " + ptf + " to %s\n"%dir_name)
input("Set-up complete. Enter any key to exit")
