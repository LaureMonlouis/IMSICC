# DELIVERABLE : DEV & USER GUIDE INTERFACE

## OBJECTIF

The final aim of the project is to provide an interactive map to users, cross-platform and easy to use.
This map displays Base Transceiver Station (BTS) found by our device. Severals research input and few tabs allow a user to get more information on BTS.

## TECHNOLOGIE

These are the different technologies used to create this web application :

* **HTML5** and **CSS3** is used for basic web application development,
* **BootStrap** (v4.0.0) is a library used to create responsive web application,
* **JavaScript** (v1.7) allow user - application interactions (searching BTS for instance),
* **MapBox** provides the maps used for our layers : [streets and satellite](https://www.mapbox.com/api-documentation/#maps) based on [OpenStreetMap](http://openstreetmap.fr/) data,
* **Leaflet** (v1.3.1) is the [javascript library](http://leafletjs.com/) that allows to create graphical objects such as map, markers (BTS), scale and control, etc.,
* **GeoJSON**, or [Geographic JSON](https://tools.ietf.org/html/rfc7946), is the data format used by Leaflet to display BTS markers on map.

## DEVELOPMENT

In order to develop this map, the following lines must be added to the html file.

```html
    <!-- leaflet -->
    
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css"
          integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
          crossorigin=""/>
    
    <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"
            integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw=="
            crossorigin="">
    </script>
	
	<!-- Bootstrap -->
	
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    
    <!-- Datas (GeoJSON) -->
    
	<script type="text/javascript" src="chemin/datas.js"></script>
	<script type="text/javascript" src="chemin/summary_db_json.js"></script>
```
As the map should be cross-platform, it is designed with bootstrap to get responsive page on all screens : xs for phones, sm for tablets, md for desktops and lg for larger desktops.

```html
	<div class="col-xs-8 col-sm-8 col-md-9 col-lg-9">
```
As a result, the application remains intuitive and easy to use on all platforms.

## WEB APPLICATION

The web application developped is in French as the project began in Rennes (France).

The application proposes severald tabs for users  :
* `Analyse` - this tab allows the user to do a static analysis on a specific area.
* `Live` - this tab allows the user to do a dynamic analysis around his own position.
* `Détails BTS` - this tab is `Analyse` tab related and displays informations on the complete set of BTS.

All files related to this application can be found in the repository `IMSICC/carte/`.

## ANALYSIS TAB

The file `index.html` open the application on the `Analyse` Tab in your favourite browser.
This page is separated into two main sections, a map section on the left and a user information section on the right. The last part is composed of a research box and a statistic box.

At the launch of the application, the map is automatically centred on Rennes.

### DATA

All data we gathered from now are around Rennes and Nantes.

Data used for the map are stored in a file called `datas.js`, with the specific GeoJSON format. This file is generated from another file, `db_json` (`IMSICC/DB/db_json`), containing all information about collected BTS, thanks to the script `prepare-data.py` inside the repository `carte/prepare_data/`.

Each GeoJSON object of this file corresponds to a different BTS with a unique CID. Here is an example of the GeoJSON representation of one BTS :

```json
{
    "type": "Feature",
    "id": 1,
    "properties": {
        "name": "BS1",
        "lac": 10300,
        "cid": 57179,
        "mcc": 208,
        "mnc": 1,
        "rxlvl": -101,
        "score": "valide"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [47.95907064102565, -1.4734134358974358]
    }
}
```

<!-- Attention à bien parler du score de chaque BTS avant justement ! -->

The value of the attribute `properties.score` depends on the score assigned to each BTS. Indeed, if this score is higher than a specific threshold, then `properties.score` takes the value "invalide", and "valide" otherwise.

Moreover, the value of `properties.score` defines weither the color of the BTS will be black (`properties.score == "valide"`) or red (`properties.score == "invalide"`).

### INTERACTING WITH THE MAP

As said before, the map is first centred on Rennes. To allow a fast use of the map, only the BTS contained inside the map bounds (as seen on the screen) are displayed, e.g. not all the BTS collected are loaded. Then, new set of BTS is automatically loaded each time the map moves and the former set of BTS is cleared.

This map allows basic map interactions such as zoom and zoom out, click and drag, switch the layer (streets or satellite).

Besides, we added some features to gives more information on BTS. When a user moves his mouse over a BTS marker, the inset on the bottom right corner is updated to display the following features :
* `CID` : cell ID,
* `Première apparition` : first time the BTS was collected,
* `Dernière apparition` : last time the BTS was collected,
* `ARFCN diffusé` : whether the ARFCN of the current BTS is proposed by his neighbours,
* `LAC réel` : whether at least some neighbours (of the current BTS) have the same LAC number,
* `Localisation constante` : whether all the records of one BTS show more or less the same localization,
* `Paramètres constants` : whether all the records of one BTS show the same parameters.

In addition, when a user clicks on a BTS on the map, a popup suggests him to follow a link to get more information on the BTS. This link will redirect him on the `Détails BTS` tab (explained later in this document).

### DO A RESEARCH

Different features allow to filter the BTS displayed on the map. Users can especially display all BTS from a given LAC, all BTS which belong to a specific operator or display only one BTS with its specific CID for instance. Besides, users can choose to display only valid or invalid BTS. To finish, the last selector allow users to pick a city among the list and the map will automatically *fly* to this city and display the BTS over there. 

In order to apply the filters, the user has to click on the button **Lancer la recherche**. Only some of the inputs may be fulfilled or all, the filters will take all the features that contains an actual value.

### STATISTIQUES

This small box contains two additional information :
* The total number of BTS collected within the current bounds of the map.
* The number of invalid BTS collected within the current bounds of the map.
These numbers does not depend on what BTS are displayed on the map (according the features put by users in the research box), they are constants within a given area.

## LIVE TAB

> The `Live` tab is currently empty. Allowing to execute a dynamic analysis while the device is moving could be the next step of this project. During the past six months, we choose to focus ourselves on the static analysis to be able to provide at least a useful and operational deliverable.

## BTS DETAILS TAB

The `Détails BTS` tab aims to present to users a whole set of BTS, e.g. all the BTS collected by the device.

### DATA

The displayed data come from the file `summary_db_json.js` (`IMSICC/DB/summary_db_json`). Values of this file are the result of detection rules applied to raw data to evaluate whether the BTS is valid or invalid.

<!-- Attention il faut avoir parlé des règles avant + rajouter un (cf. §...) -->

Here is an example of BTS characteristics after applying the detection rules :

```json
{
    "arfcn_present": true,
    "cellid": 869,
    "constant_location": true,
    "constant_parameters": true,
    "first_time": "2017/12/29,16:10:53",
    "lac": 6404,
    "lac_present": true,
    "last_time": "2017/12/29,16:13:40",
    "mcc": 208,
    "mnc": 1,
    "nb_arfcn": 1,
    "nb_bsic": 1,
    "nb_cellstatus": 0,
    "nb_lac": 1,
    "nb_mcc": 1,
    "nb_mnc": 1,
    "nb_neighb": 4.0,
    "neighb_issue": "None"
}
```

<!-- "nb_cellstatus": 0 On le garde ? Sinon changer le chiffre dans le § suivant -->

The seven first keys `arfcn_present`, `cellid`, `constant_location`, `constant_parameters`, `first_time`, `lac_present` and `last_time` are displayed in the map inset in the `Analyse` tab. Therefore, their meaning are explained in the paragraph *INTERACTING WITH THE MAP*. In addition, the eight remaining keys are helping values in case some previous keys has `false` as value.

### TABLE

All elements used to calculate the score of a BTS, therefore whether it is valid or invalid, are displayed in this table.

The `Search` input on the top of the table allow users to seek any strings among the first three columns of the table, e.g. filters can be applied on lines according BTS CID, first or last apparition in record. Besides, each columns of the table can be shown or hidden with the button next to the input, and sorted in ascending or descending order.