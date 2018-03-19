#!/usr/bin/env python
import os
import sys
import re
import json

# Default output file name
output_filename="db_json.js"
if len(sys.argv)==2:
  # Output file name
  output_filename=sys.argv[1]

class Gpsloc:
  def  __init__(self):
    self.time=None
    self.lat=None
    self.lng=None
  def set(self,time,lat,lng):
    self.time=time
    self.lat=lat
    self.lng=lng
  def get(self):
    return self.time,self.lat,self.lng
  def getlat(self):
    return self.lat
  def getlng(self):
    return self.lng
  def gettime(self):
    return self.time

class BaseStation:
  def __init__(self):
    self.ARFCN=None
    self.BSIC=None
    self.MCC=None
    self.LAC=None
    self.CID=None
    self.cellStatus=None
  def set(self,ARFCN,BISC,MCC,LAC,CID,cellStatus,MNC,
      ARFCN_NEIGH,CHANNELS,
      PBCCH,NOM,RAC,SPGC,PAT,NCO,T3168,T3192,DRXMAX,CTRLACK,BSCVMAX,ALPHA,PCMEASCH,
      RXLVL,gpsloc,survey_time):
    self.ARFCN=ARFCN
    self.BSIC=BISC
    self.MCC=MCC
    self.LAC=LAC
    self.CID=CID
    self.cellStatus=cellStatus
    self.MNC=MNC
    self.ARFCN_NEIGH=ARFCN_NEIGH
    self.CHANNELS=CHANNELS
    self.PBCCH=PBCCH
    self.NOM=NOM
    self.RAC=RAC
    self.SPGC=SPGC
    self.PAT=PAT
    self.NCO=NCO
    self.T3168=T3168
    self.T3192=T3192
    self.DRXMAX=DRXMAX
    self.CTRLACK=CTRLACK
    self.BSCVMAX=BSCVMAX
    self.ALPHA=ALPHA
    self.PCMEASCH=PCMEASCH
    self.RXLVL=RXLVL
    self.gpsloc=gpsloc
    self.survey_time=survey_time

  def get(self):
    return self.ARFCN,self.BSIC,self.MCC,self.LAC,self.CID,self.cellStatus, \
      self.ARFCN_NEIGH, \
      self.CHANNELS, \
      self.PBCCH, \
      self.NOM, \
      self.RAC, \
      self.SPGC, \
      self.PAT, \
      self.NCO, \
      self.T3168, \
      self.T3192, \
      self.DRXMAX, \
      self.CTRLACK, \
      self.BSCVMAX, \
      self.ALPHA, \
      self.PCMEASCH;

  def get_dict(self):
    bs_dict={}
    bs_dict['arfcn']=self.ARFCN
    bs_dict['bsic']=self.BSIC
    bs_dict['mcc']=self.MCC
    bs_dict['lac']=self.LAC
    bs_dict['cellid']=self.CID
    bs_dict['mnc']=self.MNC
    bs_dict['cellStatus']=self.cellStatus
    bs_dict['neigh']=self.ARFCN_NEIGH
    bs_dict['channels']=self.CHANNELS
    bs_dict['pbcch']=self.PBCCH
    bs_dict['nom']=self.NOM
    bs_dict['rac']=self.RAC
    bs_dict['spgc']=self.SPGC
    bs_dict['pat']=self.PAT
    bs_dict['nco']=self.NCO
    bs_dict['t3168']=self.T3168
    bs_dict['t3192']=self.T3192
    bs_dict['drxmax']=self.DRXMAX
    bs_dict['ctrlack']=self.CTRLACK
    bs_dict['bscvmax']=self.BSCVMAX
    bs_dict['alpha']=self.ALPHA
    bs_dict['pcmeasch']=self.PCMEASCH
    bs_dict['lngabs']=self.gpsloc.getlng()
    bs_dict['latabs']=self.gpsloc.getlat()
    bs_dict['gp_time']=self.gpsloc.gettime()
    bs_dict['rxlev']=self.RXLVL
    bs_dict['surv_time']=self.survey_time
    return bs_dict

  def equal(self,otherbs):
    if ( 
    (self.ARFCN == otherbs.ARFCN) and
    (self.BSIC  == otherbs.BSIC) and 
    (self.LAC   == otherbs.LAC) and
    (self.CID== otherbs.CID) ):
      return True
    else: 
      return False

  def getCellstatus(self):
    return self.cellStatus
  def getARFCN(self):
    return self.ARFCN
  def getBSIC(self):
    return self.BSIC
  def getMCC(self):
    return self.MCC
  def getLAC(self):
    return self.LAC
  def getCID(self):
    return self.CID
    

def deg_to_abs(degcoord):
  abscoord=int(degcoord/100.) + ((degcoord%100)/60.)
  return abscoord

#
# decode_gps(gps_line)
#
# return time,latitude and longitude from GGA raw line
#
gpsre="^\$GPGGA,([0-9]+\.[0-9]+),"
gpsre+="([0-9]+\.[0-9]+),"
gpsre+="([SN]),"
gpsre+="([0-9]+\.[0-9]+),"
gpsre+="([EW])"
gpspat=re.compile(gpsre)

def decode_gps(gps_mo):
  gp_time=float(gps_mo.group(1))
  gp_lat=float(gps_mo.group(2))
  gp_lng=float(gps_mo.group(4))
  gp_ew=gps_mo.group(5)
  gp_ns=gps_mo.group(3)
 
  latabs=deg_to_abs(gp_lat)
  lngabs=deg_to_abs(gp_lng)

  if (gp_ns=="S"):
    latabs=-latabs
  if (gp_ew=="W"):
    lngabs=-lngabs

  newgpsloc=Gpsloc()
  newgpsloc.set(gp_time,latabs,lngabs)
  return newgpsloc

surveyre='^Survey start at #CCLK: "([^"]+)"$'

gsmre="^arfcn: ([0-9]+) "
gsmre+="bsic: ([0-9]+) "
gsmre+="rxLev: (-[0-9]+) "
gsmre+="ber: ([0-9]+\.[0-9]+) "
gsmre+="mcc: ([0-9]+) "
gsmre+="mnc: ([0-9]+) "
gsmre+="lac: ([0-9]+) "
gsmre+="cellId: ([0-9]+) "
gsmre+="cellStatus: ([^ ]+) "
gsmre+="numArfcn: (\d+) "
gsmre+="arfcn: ((\d+ )*)"
gsmre+="numChannels: ([0-9]+) "
gsmre+="array: ((\d+ )*)"
gsmre+="pbcch: ([0-9]+) "
gsmre+="nom: ([0-9]+) "
gsmre+="rac: ([0-9]+) "
gsmre+="spgc: ([0-9]+) "
gsmre+="pat: ([0-9]+) "
gsmre+="nco: ([0-9]+) "
gsmre+="t3168: ([0-9]+) "
gsmre+="t3192: ([0-9]+) "
gsmre+="drxmax: ([0-9]+) "
gsmre+="ctrlAck: ([0-9]+) "
gsmre+="bsCVmax: ([0-9]+) "
gsmre+="alpha: ([0-9]+) "
gsmre+="pcMeasCh: ([0-9]+)"
gsmpat=re.compile(gsmre)

def decode_gsm(gsm_mo,gpsloc,survey_time):
  mo_idx=1
  ARFCN=int(gsm_mo.group(mo_idx))    ;mo_idx+=1
  BSIC=int(gsm_mo.group(mo_idx))     ;mo_idx+=1
  RXLVL=int(gsm_mo.group(mo_idx))    ;mo_idx+=1
  BER=float(gsm_mo.group(mo_idx))    ;mo_idx+=1
  MCC=int(gsm_mo.group(mo_idx))      ;mo_idx+=1
  MNC=int(gsm_mo.group(mo_idx))      ;mo_idx+=1
  LAC=int(gsm_mo.group(mo_idx))      ;mo_idx+=1
  CID=int(gsm_mo.group(mo_idx))      ;mo_idx+=1
  cellStatus=gsm_mo.group(mo_idx)    ;mo_idx+=1 # 9

  # Cope with arfcn variable length array
  NUMARFCN=int(gsm_mo.group(mo_idx))         ;mo_idx+=1 # 10
  ARFCN_NEIGH={}
  arfcnfr=gsm_mo.group(mo_idx).strip().split(" ")   ;mo_idx+=2 # 11
  if (NUMARFCN!=0):
    # Check against broken lines
    if (NUMARFCN!=len(arfcnfr)):
      dbg_str="".join("Parsing error numArfcn %i != %i\n"%(NUMARFCN,len(arfcnfr)))
      sys.stderr.write(dbg_str)
      return None
    for arfcn_idx in range(0,NUMARFCN):
      ARFCN_NEIGH[arfcn_idx]=int(arfcnfr[arfcn_idx])

  # Cope with numChannels variable length array
  NUMCHANNELS=int(gsm_mo.group(mo_idx))      ;mo_idx+=1
  CHANNELS={}
  channelsr=gsm_mo.group(mo_idx).strip().split(" ") ;mo_idx+=2
  if (NUMCHANNELS!=0):
    # Check against broken lines
    if (NUMCHANNELS!=len(channelsr)):
      dbg_str="".join("Parsing error numchannel %i != %i\n"%(NUMCHANNELS,len(channelsr)))
      sys.stderr.write(dbg_str)
      return None
    for channel_idx in range(0,NUMCHANNELS):
      CHANNELS[channel_idx]=int(channelsr[channel_idx])

  PBCCH=int(gsm_mo.group(mo_idx))      ; mo_idx+=1
  NOM=int(gsm_mo.group(mo_idx))        ; mo_idx+=1
  RAC=int(gsm_mo.group(mo_idx))        ; mo_idx+=1
  SPGC=int(gsm_mo.group(mo_idx))       ; mo_idx+=1
  PAT=int(gsm_mo.group(mo_idx))        ; mo_idx+=1
  NCO=int(gsm_mo.group(mo_idx))        ; mo_idx+=1
  T3168=int(gsm_mo.group(mo_idx))      ; mo_idx+=1
  T3192=int(gsm_mo.group(mo_idx))      ; mo_idx+=1
  DRXMAX=int(gsm_mo.group(mo_idx))     ; mo_idx+=1
  CTRLACK=int(gsm_mo.group(mo_idx))    ; mo_idx+=1
  BSCVMAX=int(gsm_mo.group(mo_idx))    ; mo_idx+=1
  ALPHA=int(gsm_mo.group(mo_idx))      ; mo_idx+=1
  PCMEASCH=int(gsm_mo.group(mo_idx))   ; mo_idx+=1
  

  newbs=BaseStation()
  newbs.set(ARFCN,BSIC,MCC,LAC,CID,cellStatus,MNC,
            ARFCN_NEIGH,
            CHANNELS,
            PBCCH,NOM,RAC,SPGC,PAT,NCO,T3168,T3192,DRXMAX,CTRLACK,BSCVMAX,
            ALPHA,PCMEASCH,RXLVL,gpsloc,survey_time)
  return newbs


def parse_file(bs_flat,infile):
  #
  # Populate <bs>, list of BaseStation, associated
  # with the list of <gpsloc>.
  # 
  gpsloc=None
  survey_time=None

  for iline in infile:
    imo=re.match(surveyre,iline)
    if None!=imo:
      survey_time=imo.group(1)

    imo=re.match(gpspat,iline)
    if None!=imo:
      gpsloc=decode_gps(imo)
      continue

    # Wait to have at least one GPS coordinate before grabing GSM data
    if (gpsloc==None):
      continue
    # Wait to have at least one survey time before grabing GSM data
    if (survey_time==None):
      continue

    imo=re.match(gsmpat,iline)
    if None!=imo:
      bs=decode_gsm(imo,gpsloc,survey_time)
      if (bs==None):
        sys.stderr.write("".join("Droping malformed line '%s'\n"%(iline)))
        continue

  #    print bs.get_dict()
      bs_flat.append(bs.get_dict())
      continue

  dbg_msg=""
  if None==survey_time:
    dbg_msg+="Strange, no 'Survey ... CCLK...' pattern found.\n"
  if None==gpsloc:
    dbg_msg+="Strange, no GPS data found.\n"

  if None!=dbg_msg:
    sys.stderr.write(dbg_msg)
  
bs_flat=[]
for root,dirs,files in os.walk("../Data/raw_data",topdown=False):
  for name in files:
    if os.path.join(root,name).endswith("out.txt"):
      fname=os.path.join(root,name)
      print "Parsing %s"%(fname)
      try:
        with open(fname) as infile:
          parse_file(bs_flat,infile)
      except:
        print "Problem loading file %s"%fname
        continue

with open(output_filename,"w") as f:
  print "Writing JSON database into %s"%(output_filename)
  json.dump(bs_flat,f)

