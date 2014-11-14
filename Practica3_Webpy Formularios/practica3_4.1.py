#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import re #Expresiones regulares
from web import form 
from web.contrib.template import render_mako
from random import randint
import dbm


urls = ( '/', 'index',
	 '/login', 'sirve_login',
	 '/registro', 'sirve_registro',
	 '/busqueda', 'busqueda',
	 '/logout', 'logout',
	 '/(.*)', 'error'
       )
       
# Para poder usar sesiones con web.py
web.config.debug = False

app = web.application(urls, globals())

db = dbm.open('cache', 'c')


#Plantillas Mako
plantillas = render_mako(
       directories=['templates/'],
       input_encoding='utf-8',
       output_encoding='utf-8'
       )
       
#Inicializamos la variable session a cadena vacía porque inicialmente no hay ningún usuario que haya iniciado sesion
sesion = web.session.Session(app,
	  web.session.DiskStore('sessions'),
	  initializer={'usuario':''})

#Formulario Login
login = form.Form(
	form.Textbox('username', form.notnull, description = 'Usuario'),
	form.Password('password',  form.notnull, description = 'Contrasenia'),
    form.Button('Login', description = 'Login'),
)

#Formulario busqueda
buscar = form.Form(
	form.Textbox('dni', form.notnull, description = 'Introduce DNI'),
    form.Button('Buscar'),
)

#Expresiones regulares para validacion
email = re.compile(r'\w+@([a-z]+\.)+[a-z]+')
visa = re.compile(r'(\d){4}\-(\d){4}\-(\d){4}\-(\d){4}|(\d){16}')

#Formulario de registro
registro = form.Form(
	form.Textbox('nombre', maxlength="22", description="Nombre:"),
	form.Textbox('apellidos', maxlength="22", description="Apellidos:"),
	form.Textbox('dni', maxlength="9", size="9", description="DNI:"),
	form.Textbox('correo', maxlength="25", size="15", description="Correo Electronico:"),
	form.Dropdown('dia', range(1,32), description="Dia:"),
	form.Dropdown('mes', range(1,12), description="Mes:"),
	form.Dropdown('anio', range(1930,2013), description="Anio:"),
	form.Textarea('direccion', maxlength="55", size="35", description="Direccion:"),	
	form.Password('passw', maxlength="17", size="12", description="Password:"),
	form.Password('passw2', maxlength="17", size="12", description="Repetir:"),
	form.Radio('forma_pago', ['contra reembolso', 'visa'], description="Forma de pago:"),
	form.Textbox('numero_visa', maxlength="19", size="20", description="Numero Visa"),
    form.Checkbox('check',
		form.Validator("Debe aceptar las clausulas.", lambda i: "check" not in i), description="Acepto las clausulas"), 
	form.Button('Aceptar'),
	
	
    validators = [
		form.Validator('El campo nombre no puede estar vacio.', lambda i: len(str(i.nombre))>0),
		form.Validator('El campo apellidos no puede estar vacio.', lambda i: len(str(i.apellidos))>0),
		form.Validator('El campo dni no puede estar vacio.', lambda i: len(str(i.dni))>0),
		form.Validator('El campo correo no puede estar vacio.', lambda i: len(str(i.correo))>0),
		form.Validator('El campo direccion no puede estar vacio.', lambda i: len(str(i.direccion))>0),
		form.Validator('El campo numero visa no puede estar vacio.', lambda i: len(str(i.numero_visa))>0),
		form.Validator('Fecha Incorrecta.', lambda x: not(
			(int(x.dia)==31 and int(x.mes)==2) or 
			(int(x.dia)==30 and int(x.mes)==2) or 
			(int(x.dia)==29 and int(x.mes)==2 and int(x.anio)%4!=0) or 
			(int(x.dia)==31 and (int(x.mes)==4 or int(x.mes)==6 or int(x.mes)==9 or int(x.mes)==11))
		)),  
		form.Validator("Formato de correo no valido.", lambda i: email.match(i.correo)),
		form.Validator("Formato de numero de visa no valido.", lambda i: visa.match(i.numero_visa)),
		form.Validator("El password debe contener mas de 7 caracteres.", lambda i: len(str(i.passw))>7),
		form.Validator("El password debe contener mas de 7 caracteres.", lambda i: len(str(i.passw2))>7),
		form.Validator('El password no coindice.', lambda i: i.passw == i.passw2)
		]
)

class error:
	def GET(self, url):
		sesion.kill()
		usuario = sesion.usuario
		web.header('Content-type','text/html; charset=utf-8')
		return u'Esta url: ' + unicode(url) + u' no esta funcionando ' + unicode(usuario)
		

class index:
	def GET(self):
		web.header('Content-Type', 'text/html; charset=utf-8')
		return plantillas.index(mensaje='')
		

class sirve_login:
	def GET (self):
		r=login()
		web.header('Content-Type', 'text/html; charset=utf-8')
		return plantillas.login(reg=r ,mensaje='')

	def POST (self):
		r=login()
		
		if not r.validates():
			web.header('Content-Type', 'text/html; charset=utf-8')
			return plantillas.login(reg=r ,mensaje='')
		
		else:
			i = web.input()
			usuario  = i.username
			passwd = i.password
				
			if (passwd in db.keys()):
				sesion.usuario=usuario
				ses = sesion.usuario
				return plantillas.bienvenido(nombre = ses)
			else:
				r.password.set_value("")
				men = "El usuario o el password no son validos."
				return plantillas.login(reg=r ,mensaje=men)
			
				
			
class logout:
	def GET(self):
		usuario = sesion.usuario
		sesion.kill()
		men='Adios ' + usuario
		return plantillas.index(mensaje=men)
		

class sirve_registro:
	def GET (self):
		r=registro()
		web.header('Content-Type', 'text/html; charset=utf-8')
		return plantillas.registro(reg=r)

	def POST (self):
		r=registro()
		if not r.validates():
			web.header('Content-Type', 'text/html; charset=utf-8')
			return plantillas.registro(reg=r)
		
		else:
			i = web.input()
			nombre  = i.nombre
			dni = i.dni
			passwd=i.passw
			
			# insertamos un usuario			
			db[dni] = nombre
			db[passwd] = nombre
			
			return 'Usuario correctamente creado'


class busqueda:
	def GET (self):
		r=buscar()
		web.header('Content-Type', 'text/html; charset=utf-8')
		return plantillas.busqueda(reg=r)
		
	def POST(self):
		r=buscar()
		
		if not r.validates():
			web.header('Content-Type', 'text/html; charset=utf-8')
			return plantillas.busqueda(reg=r)
		
		else:
			i = web.input()
			pas = i.dni
			
			if (pas in db.keys()):
				res = db[pas]
				return res
			else:
				return 'No existe ningun usuario con ese dni.'

			
if __name__ == "__main__":
    app.run()
