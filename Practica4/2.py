#!/bin/bash

# -*- coding: utf-18 -*-

from lxml import etree
import re
import sys
import urllib

total_noticias = 0
total_imagenes = 0
total_palabra = 0
j = 0
termino = sys.argv[1]

tree = etree.parse('ultimas_noticias.xml')

# Root element
rss = tree.getroot()

# Los elementos funcionan como listas
# First child
channel = rss[0] # channel indica el numero de las etiquetas de segundo nivel


for e in channel:
	if (e.tag == "item"):  # comprobamos que son noticias
		total_noticias += 1
	
		for i in e:
			if (i.tag != "enclosure"): # comprobamos que no sea una url
				total_palabra += ((i.text).encode('utf-8')).count(termino)	# codificamos a utf-8 el texto y buscamos la 													palabra			
			else: 
				if (i.get('type') == "image/jpeg"): # comprobamos que son imagenes
					total_imagenes += 1 
				
				name = "0000%s.jpeg" % j # descargamos las imagenes
				j += 1
				image = urllib.URLopener()
				image.retrieve(i.get('url'), name)
					
				
	 	
	if (e.tag == "image"): # comprobamos si hay mas imagenes
		total_imagenes += 1
	
	
print ('Hay %s noticias' % total_noticias)  
print ('Hay %s imagenes' % total_imagenes)
print ('Hay %s apariciones del termino %s' % (total_palabra,termino))

