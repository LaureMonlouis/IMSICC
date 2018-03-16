#!/usr/bin/python3.6
#-*- coding: utf-8 -*-
    
# Prendre chaque entrée de datas_tmp.json pour agréger les données et écrire le résultat dans ../datas.js.

import os
import json
from math import fabs

fi = open("datas_tmp.js", "r")
fo = open("../datas.js", "w")

d = fi.read()	# type str, identique à db_json : [{}, {}, ... ]

nb = len(d)

d = d[:(nb-3)]

d = d + "\n]"

# Récupération des données db_json pour python = list

datas = json.loads(d) # type list
# Chaque element de la list = un objet GeoJSON

# Initialisation variable datas dans le fichier output

fo.write("var datas =\n")

# Boucle pour remplir le fichier output avec les GeoJSON

result = list()
result_cids = list()

for i, elem in enumerate(datas):

	# Pour plusieurs cid identiques, on ne garde que l'entrée avec le rxlevel le plus proche de 0		
	
	# common_cids est une liste des entrées avec le même cid
	common_cids = [tmp for tmp in datas if tmp['properties']['cid'] == elem['properties']['cid']]

	# rxlevels est une liste des rxlevels des entrées contenues dans common_cids et min_rxlevel est le minimum de cette liste
	rxlevels = [fabs(x['properties']['rxlvl']) for x in common_cids]
	min_rxlevel = min(rxlevels)
		
	# Si elem a le rxlevel minimum, alors il est ajouté dans result
	# A condition que la paire (dic, rxlvl) n'existe pas déjà
	if((fabs(elem['properties']['rxlvl']) == min_rxlevel) and (elem['properties']['cid'] not in result_cids)):
		result_cids.append(elem['properties']['cid'])
		result.append(elem)

print(len(result))
print(len(result_cids))
fo.write(json.dumps(result, indent=4))
fo.write(";")

# Fermeture des fichiers

fi.close()
fo.close()
	
os.system("pause")


# import os
# import json
# os.chdir("C:/Users/Laure/Dropbox/IMSI/carte/prepare_data") 

# TODO : ajouter bloc try except ...