from requests import request
import hashlib
import time
import os

API_KEY = "6666666"
BASE_FILES = dict()

#Baseline
for fname in os.listdir('.'):
    if os.path.isfile(fname):
        try:
            md5 = hashlib.md5(open(fname,"rb").read()).hexdigest()
            BASE_FILES.update({fname:md5})
        except:
            pass

#Scan for new BASE_FILES
while True:
    time.sleep(5)
    for fname in os.listdir("."):
        try:
            if os.path.isfile(fname):
                md5 = hashlib.md5(open(fname,"rb").read()).hexdigest()
                if md5 not in BASE_FILES.values():
                    print("New MD5 : " + fname + '\nAnalyzing...')
                    
                    #Uploading File
                    url = "https://www.virustotal.com/vtapi/v2/file/scan"
                    params = {"apikey":API_KEY}
                    files = {"file":(fname,open(fname,"rb").read())}
                    response = request("POST", url, files=files, params=params).json()
                    resource = response["resource"]

                    #Retrieving File Report
                    url = "https://www.virustotal.com/vtapi/v2/file/report"
                    params = {"apikey":API_KEY,"resource":resource}
                    response = request("GET", url, params=params).json()
                    
                    #Calculate percentage
                    total = response["total"]                    
                    positives = response["positives"]
                    percentage = positives / total * 100
                    print ("Total: {} \nPositives: {} \nPercentage: {}".format(total,positives,percentage))
                    if (percentage >= 2):
                        os.remove(fname)
                        response2 = request("POST","http://localhost:8080/api/delete?delete="+fname)
                    elif (percentage < 2):
                        BASE_FILES.update({fname:md5})
                        response2 = request("POST","http://localhost:8080/api/add?add="+fname)

        except:
            pass


    











