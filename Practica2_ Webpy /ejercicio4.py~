import web
from web import form

urls = ('/', 'index')
app = web.application(urls, globals())

login = form.Form(
    form.Textbox('username', web.form.notnull, description = 'Usuario'),
    form.Password('password',  web.form.notnull, description = 'Contrasenia'),
    form.Button('Login', description = 'Login'),
)

class index: 
    def GET(self): 
        form = login()
        # Hay que hacer una copia del formuario (linea superior)
        # O los cambios al mismo serian globales
        return """<html><body>
        <form name="input" action="/" method="post">
        %s
        </form>
        </body></html>
        """ % (form.render())

    def POST(self): 
        form = login() 
        if not form.validates(): 
		return """<html><body>
		<form name="input" action="/" method="post">
		%s
		</form>
		</body></html>
		""" % (form.render())
        else:
	     return "Bienvenido %s" %(form.d.username)
if __name__=="__main__":
    app.run()
