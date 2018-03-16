import sys, os, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy.distance
import math 

# Import Json data
db=json.load(open('db_json'))

#List the columns available
n=0
for i in db:
    while n==0:
        print "Available Columns before selection: \n"
        print db[i][0].keys()
        n=n+1
