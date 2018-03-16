# IMSI CATCHERS' CATCHER

**TODO** :

- [x] Hardware
- [x] Software
- [x] Deliverable
- [ ] Report
- [ ] Presentation slides


## OVERVIEW

IMSI catchers, or stingrays, are electronic devices used to track and monitor mobile phone telecommunications. This project aims at building and testing our own IMSI catcher detector.

To do so, we will rely upon research protocols developed in the academic literature.  A short review of it is available later on in this document.

## IMSI CATCHERS

IMSI catchers refer to electronic devices whose goal is to intercept mobile phones communications. IMSI stands for International Mobile Subscriber Identity.  It is a unique 15 digits numbers stored in every SIM card and used by mobile networks providers to identify users trying to connect to their network.

IMSI catchers are based on a Man In The Middle (MITM) attack by acting as fake cellular base stations. Under their most basic form, they are used to force phones located in a given area to reveal their IMSIs. This enables an attacker to list all local phones and keep track of their locations. However, their capacities may vary greatly. More sophisticated IMSI catchers can also intercept communication, send fake sms/voice messages or launch DDOs attacks.

Their rely on weaknesses of the 2G protocol that will be described in further details later.

## DETECTING IMSI CATCHERS

Various protocols have been developed to detect IMSI catchers. They all rely on capturing communications between phones and (rogue) cellular base stations. Indeed, fake and legitimate base stations transmit a wide range of data, known as Broadcast Control Channel Properties (BCCH), about their own configuration that may be analyzed to distinguish legitimate ones from IMSI catchers.

As described by Ney and al (2017), possible IMSI catchers signatures are:
* Multiple location transmissions: legitimate stations are usually stationary. On the contrary, most common IMSI catchers are portable and reused by holders in different places. By looking if a station is discovered in several locations exhibiting the same attributes, one may gather strong evidence of IMSI catchers’ use.
*  Impermanence: IMSI catchers’ use are likely to be temporary. An attacker may wish to spy on a victim for a given period of time and then stops. Base stations that appear and disappear shortly afterwards are therefore potential rogue stations candidates.
* Anomalous configuration properties: IMSI catchers are believed to exhibit configuration properties that differ from legitimate stations.
    * Firstly, in order to track phones and intercept communications, they may interact with phones being targeted in unusual ways. For example, IMSI catchers may induce targets to transmit more frequently, prevent them from connecting to other nearby cells, use weak cipher modes or communicating using 2G instead of the more secured 3/4G protocols.
    * Secondly, they may also differ broadcast inappropriate attributes if not properly configured. Indeed, local base stations attributes are carefully chosen in order to increase the efficiency of the network. An attacker station may be revealed if it broadcasts configuration properties that differ from other cells in the same area. Examples are anomalous Location Area Identities (LAI) or unusual broadcast frequencies (ARFCNs).

## BUILDING AN IMSI CATCHERS' CATCHER

As described previously, the detection of IMSI catcher requires:
* The collection of base stations broadcasted properties (BCCH),
* The analysis of cells/phones interaction.

In order to do so, and following Ney et al (2017), this project aims at building a detector equipped with the following components:
* A GSM modem to collect network properties and BCCH.
* A bait rooted android phone to collect network packets and the list of base stations on which it camps.
* A GPS to record the GSM modem and bait phone location.
* A raspberry pi to driver the GSM modem, and store all collected data for offline post-processing.

The total cost is estimated to be approximatively 500€.

## REFERENCES

> SeaGlass, Enabling city-wide IMSI-Catcher Detection
> Proceedings on Privacy Enhancing Technologies, 2017
> Peter Ney, Ian Smith Gabriel Cadamuro and Tadayoshi Kohno
