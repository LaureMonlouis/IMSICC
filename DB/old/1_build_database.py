#!/usr/bin/env python

#Name: import_raw*.py

#######################################################
########Preparing raw data received from PI############
#######################################################
# Import raw Data into a json DB
# Need to be run on ALL FILES if we need a unique if (cf below)

# Remarks:
    # Every GSM Modem Line is an Entry without any aggregation
    # Aggregation would be make using the SQL Database Later
    # Id is a simple incremental number, one for each observation

# Questions & To Do:
    # Get the Date from the files name. No way to do better?
    # Le fichier 17_12_22 a un format different. On est bon apres?

#########################################################
#########################################################
import sys,os,re,json

#Set some vars
file_to_send="db_json"

last_gps=["","","","",""]
last_gsm=["","","","",""]

#Final Dictionnary
final_dict=[]

#################################
#####Define Some functions#######
#################################

def deg_to_abs(degcoord):
    abscoord=int(degcoord/100.) + ((degcoord%100)/60.)
    return abscoord

#################################
#######   MAIN    ###############
#################################

#User friendly:
print "Starting Reading Files in Data/raw_data/ And Formatting \n!!!Warning will overwrite db_json.!!!"
#raw_input("Do you want to overwrite db_json or choose another file? y/n")
#
#if raw_input=="n":
#    file_to_send=raw_input("Type a new filename")
#else if raw_input!="y":
#    raw_input("Do you want to overwrite db_json or choose another file? y/n")
#    
#

raw_input("Press Enter to Go On")

#Initialize the id variable (Maybe it was for SQL DB?)
id=0

#Loop over files in Data/raw_data 
for root, dirs, files in os.walk("../Data/raw_data", topdown=False):
    for name in files:
	if os.path.join(root, name).endswith("out.txt"):
            try:
                with open(os.path.join(root,name)) as f:
                    print os.path.join(root,name)
                    for line in f:
                            #Find the GPRMC lines that are complete
                            if re.match(r"(.*)GPGGA*",line)!=None: 
                                line_split=line.split(",")
                                if line_split[0]=="$GPGGA"  and line_split[3]!="":
                                    last_gps=line_split
                                    #format the lat/lng
                                    last_gps[2]=deg_to_abs(float(last_gps[2]))
                                    last_gps[4]=deg_to_abs(float(last_gps[4]))

                            #Find the CCLK lines
                            if re.match(r"(.*)CCLK*",line)!=None: 
                                line_split=line.split(" ")
                                #Deal with the 17_12_22 format
                                if  len(line_split)<4:
                                    last_gsm=line_split[1].replace("\n","")
                                else:
                                    last_gsm=line_split[4].replace("\n","")

                            #Build the dictionnary of ARNs
                            temp_dict={}

                            if re.search(r"cellId",line)!=None:
                                line_prep=""
                                for word in line.split(" "):
                                    if re.match(r"[aA-zZ]*:",word)!=None:
                                        word=","+word
                                    line_prep=line_prep +" "+ word
                                for x in line_prep.split(','):
                                    if x!=" ":
                                        #Just check the problem with the second arfcn
                                        if x.split(":")[0]=="arfcn" and x.split(":")[0] in temp_dict.keys():
                                            temp_dict["oth_arfcn"]=x.split(":")[1]
                                        else:
                                            temp_dict[x.split(":")[0]]=x.split(":")[1].strip()

                                #Append the GPS Data
                                temp_dict['latabs']=last_gps[2]
                                temp_dict['lngabs']=last_gps[4]
                                temp_dict['gp_time']=last_gps[1]

                                #Append the csurv time: seems that cclk not collected
                                temp_dict['surv_time']=last_gsm
                                
                                #Change array keys (problem with postgre)
                                #temp_dict["array_2"] =temp_dict.pop("array")

                                #Lower case all array keys for postgre compatibilty
                                for a in temp_dict.keys():
                                    temp_dict[a.lower()]=temp_dict.pop(a)

                                #Append to the dictionnary
                                id+=1
                                #final_dict[str(id)]=temp_dict
                                final_dict.append(temp_dict)
            except:
                print "Problem loading file %s" %(os.path.join(root, name))
                continue
print "Saving to db/db_json ..."

#Save to DB (json style for now)
with open(file_to_send,'w') as f:
    json.dump(final_dict,f)

