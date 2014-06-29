#!/usr/bin/python
# -*- coding: utf8 -*-

import android
import os
import time
import datetime
droid=android.Android()
droid.webViewShow('file:///storage/sdcard0/sl4a/scripts/blank.html')
droid.addOptionsMenuItem("Off","off",None,"ic_menu_revert")
droid.eventPost("status","Recherche satellite")
droid.startLocating(22000,5)
time.sleep(5)
while True:
    response=droid.eventWait(1000).result
    time.sleep(1)
    if response==None:
        continue
    if response['name']=="location":
        break
    if response['name']=="off":
        droid.stopLocating()
        exit()
droid.eventPost("status","Creation fichier kml")
fn="map"+datetime.datetime.now().strftime("%d%m%H%M")+".kml"
os.chdir('/sdcard/download')
fic=open(fn,'a')
fic.write('<?xml version="1.0" encoding="UTF-8"?>\n')
fic.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
fic.write('<Document>\n')
fic.write('<name>Paths</name>\n')
fic.write('<description></description>\n')
fic.write('<Style id="yellowLineGreenPoly">\n')
fic.write('<LineStyle>\n')
fic.write('<color>7f00ffff</color>\n')
fic.write('<width>4</width>\n')
fic.write('</LineStyle>\n')
fic.write('<PolyStyle>\n')
fic.write('<color>7f00ff00</color>\n')
fic.write('</PolyStyle>\n')
fic.write('</Style>\n')
fic.write('<Placemark>\n')
fic.write('<name>Absolute Extruded</name>\n')
fic.write('<description></description>\n')
fic.write('<styleUrl>#yellowLineGreenPoly</styleUrl>\n')
fic.write('<LineString>\n')
fic.write('<extrude>1</extrude>\n')
fic.write('<tessellate>1</tessellate>\n')
fic.write('<altitudeMode>absolute</altitudeMode>\n')
fic.write('<coordinates>\n')
fic.close()
lat=0.0
lon=0.0
compteur=0
compteurEchec=0
droid.eventPost("status","Tracking en cours")
while True:
    response=droid.eventWait(1000).result
    time.sleep(1)
    if response==None:
        continue
    if response['name']=='location':
        loc = droid.readLocation().result
        if loc == {}:
            loc = droid.getLastKnownLocation().result
        if loc != {}:
            try:
                n = loc['gps']
            except KeyError:
                try:
                    n = loc['network']
                except KeyError:
                    droid.eventPost("status","lecture gps echoue:"+str(compteurEchec))
                    compteurEchec+=1
                    continue
            try:
                lat = n['latitude']
                lon = n['longitude']
            except KeyError:
                droid.eventPost("status","cle gps/network non trouve:"+str(compteurEchec))
                compteurEchec+=1
                continue
            compteurEchec=0
            fic=open(fn,'a')
            fic.write(str(lon)+','+str(lat)+',0\n')
            fic.close()
            droid.eventPost("echo","Point numero:"+str(compteur))
            droid.eventPost("status","tracking en cours")
            compteur+=1
        else:
            droid.eventPost("status","lecture location echoue:"+str(compteurEchec))
            compteurEchec+=1
        continue
    if response['name']=="off":
        droid.stopLocating()
        fic=open(fn,'a')
        fic.write('</coordinates>\n')
        fic.write('</LineString>\n')
        fic.write('</Placemark>\n')
        fic.write('</Document>\n')
        fic.write('</kml>\n')
        fic.close()
        break

