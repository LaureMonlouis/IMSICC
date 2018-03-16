#!/usr/bin/python3.6
#-*- coding: utf-8 -*-
    
# Prendre chaque JSON de l'input et pour chacun, créer un nouveau objet JSON à ajouter à data_tmp.js au format GeoJSON.

import os
import json

fi = open("../../DB/db_json", "r")
fo = open("datas_tmp.js", "w")

d = fi.read()	# type str, identique à db_json : [{}, {}, ... ]

# Récupération des données db_json pour python = list

datas = json.loads(d) # type list, identique à db_json : [{}, {}, ... ]
# Chaque element de la list = un objet json

#nb = len(datas) # nombre d'elements json : 9927

# Initialisation variable datas dans le fichier output

fo.write("[\n")
#fo.write("var datas = [\n")

# Boucle pour remplir le fichier output avec les GeoJSON

for i, elem in enumerate(datas, start=1):

	# On élimine les entrées sans coordonnées GPS
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

		dico["geometry"]["radius"] = 800

		tmp = json.dumps(dico, indent=4)

		fo.write(tmp)
		fo.write(",\n")

# Fermeture de la variable datas dans le fichier output

fo.write("]")
#fo.write("];")

# Fermeture des fichiers

fi.close()
fo.close()
	
os.system("pause")


# import os
# import json
# os.chdir("C:/Users/Laure/Dropbox/IMSI/carte/prepare_data") 

# TODO : ajouter bloc try except ...