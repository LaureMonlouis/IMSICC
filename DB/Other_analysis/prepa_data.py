#!/usr/bin/env python

#Name: prepa_data*.py

#######################################################
########Preparing raw data received from PI############
#######################################################
#
# GPS and GSM data are mixed
# Need to associate every GSM data with a GPS line (Position/Timestamp)
# Need to identify GSM data taken from the same survey
# Voila
# Can use a tuple as a key so easy
# And you append everything, so one id is associated with all ARFCN data + GPS + Time
#########################################################
#########################################################

import sys,os,re,json
print "Starting Reading Files And Formatting"

#Set some vars
file_to_send="db_json_test"

last_gps=["","","","",""]
last_gsm=["","","","",""]

#Final Dictionnary
final_dict={}

#################################
#####Define Some functions#######
#################################

def deg_to_abs(degcoord):
    abscoord=int(degcoord/100.) + ((degcoord%100)/60.)
    return abscoord

#################################
#######   MAIN    ###############
#################################


for line in sys.stdin:

    #Find the GPRMC lines that are complete
    if re.match(r"(.*)GPGGA*",line)!=None: 
        line_split=line.split(",")
        if line_split[0]=="$GPGGA"  and line_split[3]!="":
            last_gps=line_split
            #format the lat/lng
            last_gps[2]=deg_to_abs(float(last_gps[2]))
            last_gps[4]=deg_to_abs(float(last_gps[4]))

    #Find the CCLK lines
    if re.match(r"#CCLK*",line)!=None: 
        line_split=line.split(" ")
        last_gsm=line_split[1].replace("\n","")

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
                    temp_dict[x.split(":")[0]]=x.split(":")[1]

        #Build the unique ID
        temp_dict["id"]=str(temp_dict["bsic"]+temp_dict["mnc"]+temp_dict["lac"]+temp_dict["cellId"]).replace(" ","")

        #Append the GPS Data
        temp_dict['latabs']=last_gps[2]
        temp_dict['lngabs']=last_gps[4]
        temp_dict['gp_time']=last_gps[1]

        #Append the csurv time: seems that cclk not collected
        #temp_dict['csurv_time']=last_gps[2]

        #Test if exists or not. If not, create empty list and add the first dictionnary
        #If exists, simply append to the list. 
        if temp_dict['id'] in final_dict.keys():
            final_dict[temp_dict['id']].append(temp_dict)
        else:
            final_dict[temp_dict['id']]=[temp_dict]
print "Saving to Disk..."
#Save to DB (json style for now)
with open(file_to_send,'a') as f:
    json.dump(final_dict,f)

#Now print the table
#for keys in final_dict.keys():
#    for i in final_dict[keys]:
#        print ("%s %s %s" %(keys,i['rxLev'],i['bsic']))
#    
####################################
#######   REMARKS    ###############
####################################

#Coudl use more regex if want cleaner things
#Problem if the GPS is not the first data found (first csurv lines without GPS coordinates)
#Pour l'instant j'ai l'impression qu'on ne collectait plus le time de csurv. Donc pas d'id au niveau csurv. 
#Need to change the sign of lng
