#!/usr/bin/python3.6
#-*- coding: utf-8 -*-
    
# Prendre chaque JSON de l'input et pour chacun, créer un nouveau objet JSON à ajouter à data_tmp.js au format GeoJSON.

import os
import json
import pandas as pd

fo = open("../datas.js", "w")

# Load from json to pandas dataframe

db_final = json.load(open("../../DB/db_json"))
db_final = pd.DataFrame.from_dict(db_final, orient='columns')

# Drop missing values

db_final = db_final[db_final['cellid'].notna() & db_final["latabs"].notna() & db_final["surv_time"].notna() & db_final["cellid"]!=0]
db_final = db_final.reset_index()

# Drop duplicates and replace latabs, lngabs with average longitude/latitude

db_final[['latabs','lngabs']] = db_final[['latabs','lngabs']].groupby(db_final['cellid']).transform('mean')

db_final = db_final.drop_duplicates(subset='cellid')

datas = db_final.to_dict(orient='records')

# Initialization datas (output file)

fo.write("var datas = [\n")

# Loop to add GeoJSON (output file)

Boucle pour remplir le fichier output avec les GeoJSON

for i, elem in enumerate(datas, start=1):

	# Drop missing values
	
	if(elem['latabs'] != "" and elem['lngabs'] != ""):
	
		dico = dict()

		dico["type"] = "Feature"

		dico["id"] = i

		dico["properties"] = {}
		dico["properties"]["name"] = "BS" + str(i)
		dico["properties"]["lac"] = elem['lac']
		dico["properties"]["cid"] = elem['cellid']
		dico["properties"]["mcc"] = elem['mcc']
		dico["properties"]["mnc"] = elem['mnc']
		dico["properties"]["rxlvl"] = elem['rxlev']
		dico["properties"]["score"] = "valide"

		dico["geometry"] = {}
		dico["geometry"]["type"] = "Point"
		dico["geometry"]["coordinates"] = [elem['latabs'], elem['lngabs']]

		tmp = json.dumps(dico, indent=4)

		fo.write(tmp)
		fo.write(",\n")

# Close datas (output file)

fo.write("];")

# Close file

fo.close()
	
os.system("pause")
