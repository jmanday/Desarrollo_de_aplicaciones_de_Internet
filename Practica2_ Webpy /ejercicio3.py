import web
        

urls = (
    '/imagen', 'sirve_imagen',
    '/pagina', 'sirve_pagina',
    '/img/(.+)', 'sirve_imagen_h'
)


app = web.application(urls, globals())


def notfound():
	raise web.notfound("La pagina web no existe")

app.notfound = notfound



class sirve_imagen:
	def GET(self):
		web.header('Content-Type', 'image/jpeg')
		f = open("static/img/images.jpg")
		dato = f.read()
		f.close()
		return dato


class sirve_imagen_h:
	def GET(self, name):
		f = open("static/img/"+name)
		dato = f.read()
		f.close()
		return dato

class sirve_pagina:
	def GET(self):
		web.header('Content-Type', 'text/html')
		f = open("static/html/ejercicio.html")
		dato = f.read()
		f.close()
		return dato

if __name__ == "__main__":
    app.run()
