#!/bin/bash

# -*- coding: utf-18 -*-

from lxml import etree
import re
import sys
import urllib
import feedparser		# libreria para rss remotos

total_noticias = 0
total_imagenes = 0
total_palabra = 0
t = 0

termino = sys.argv[1]

rss_url = "http://ep00.epimg.net/rss/tags/ultimas_noticias.xml"

d = feedparser.parse(rss_url)

for i in range(0,len(d.entries) - 1):
	e = d.entries[i]
	for j in e:
		if j == "title":
			total_noticias += 1						# contamos las noticias
			total_palabra += (e.title).count(termino)			# buscamos la palabra en las noticias

		if j == "summary":
			total_palabra += (e.summary).count(termino)			# buscamos la palabra en la descripicion de las noticias

		if j == "author":
			total_palabra += (e.author).count(termino)			# buscamos la palabra en los autores

		if j == "content":
			for k in range(0, len(e.content)):
				total_palabra += (e.content[k].value).count(termino)			# buscamos en el contenido

		if j == "enclosures":									# contamos el numero de imagenes y las descargo
			for k in range(0, len(e.enclosures) - 1):
				if e.enclosures[k].href:
					total_imagenes += 1
					name = "0000%s.jpeg" % t
					t += 1
					image = urllib.URLopener()
					image.retrieve(e.enclosures[k].href, name)

if d.feed.image.href:
	total_imagenes += 1


print ('Hay %s noticias' % total_noticias)
print ('Hay %s imagenes' % total_imagenes)
print ('Hay %s apariciones del termino %s' % (total_palabra,termino))
