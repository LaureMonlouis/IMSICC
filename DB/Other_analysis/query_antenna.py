#!/usr/bin/env python 
import json
import sys
import psycopg2
import pandas as pd

# Define database parameters here
dbname = "imsi"
user = "cb"
password = "imsi"

# Query Definition
cellid=str(sys.argv[1])

print "\n#########Analysing cellid %s######\n" %str(cellid)

# Connect to Database
conn_string = "dbname=%s user=%s password=%s" % (dbname, user, password)
conn= psycopg2.connect(conn_string)
df = pd.read_sql('select * from imsi', con=conn)

# Print Summary Stats on Antenna 
df=df[df['cellid']==cellid]

    #Dates seens
df['date']=df['surv_time'].str.split(',').str[0].str.replace('"','')
last_recorded=max(df['date'])
first_recorded=min(df['date'])
print "First Seen on %s, Last seen on %s" %((first_recorded),last_recorded)
    
    #Some stats
df["latabs"]=df["latabs"].apply(pd.to_numeric, errors='coerce')
df["lngabs"]=df["lngabs"].apply(pd.to_numeric, errors='coerce')
[average_lat,average_lng]=df[["latabs","lngabs"]].mean()
[std_lat,std_lng]=df[["latabs","lngabs"]].std()

print "\nChecking for Weird Location Records:\n\tAverage and Std of its recorded lat and long: (Lat:%f,%f, Long:%f,%f)" %(average_lat,std_lat,average_lng,std_lng) 

    #Some Stats on other parameters
print "\nChecking for changes in various parameters:"
change=0
for x in ["bsic","arfcn","mcc","mnc","lac"]:
    if len(df[x].unique())>1:
        print "Duplicates values of %s detected" %(x)
if change==0:
    print "\tNo changes detected between different records."
    
    #Print to OSM
    print "\n"
