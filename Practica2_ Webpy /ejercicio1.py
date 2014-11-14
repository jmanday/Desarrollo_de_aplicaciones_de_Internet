import web
        
urls = (
    '/(.*)', 'hola' # en el caso de que sea la expresion regular /(.*) llamamos a la clase hello
)

app = web.application(urls, globals())

class hola:        
    def GET(self, name):
        if not name: 
            name = 'Mundo'	
        return 'Hola, ' + name + '!'


if __name__ == "__main__":
    app.run()
