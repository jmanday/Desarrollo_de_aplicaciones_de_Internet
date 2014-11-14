import web
        
urls = (
    '/', 'pagina'
)

app = web.application(urls, globals())

class pagina:
	def GET(self):
		raise web.seeother('/static/periodico/index.html')


if __name__ == "__main__":
    app.run()

