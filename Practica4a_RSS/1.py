#!/bin/bash

# -*- coding: utf-18 -*-

from lxml import etree
import re
import sys
import urllib

total_noticias = 0
total_imagenes = 0
total_palabra = 0
i = 0
termino = sys.argv[1]


class ParseRssNews():

	def start (self, tag, attrib):			# Etiquetas de inicio
		global total_noticias, total_imagenes, i

		if (tag == "item"):				
			total_noticias += 1	

		if (tag == "image"):
			total_imagenes += 1

		for k in attrib:
			if ((k == "type") and (attrib[k] == "image/jpeg")):
				total_imagenes += 1

			if (k == "url"):
				name = "0000%s.jpeg" % i
				i += 1
				image = urllib.URLopener()
				image.retrieve(attrib[k], name)


	def data(self, data):					# Texto
		global total_palabra

		total_palabra += data.count(termino)


	def close (self):						# Cierre de la lectura del fichero
		print ('Hay %s noticias' % total_noticias)
		print ('Hay %s imagenes' % total_imagenes)	
		print ('Hay %s apariciones del termino %s' % (total_palabra,termino))


parser = etree.XMLParser (target=ParseRssNews ())
etree.parse ('ultimas_noticias.xml', parser)

