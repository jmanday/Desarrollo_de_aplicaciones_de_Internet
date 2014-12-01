#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import web
from web import form
from web.contrib.template import render_mako
import pymongo
from bson.objectid import ObjectId
from pymongo import Connection

urls = ( '/', 'index',
	 '/login', 'sirve_login',
	 '/registro', 'sirve_registro',
	 '/busqueda', 'busqueda',
	 '/logout', 'logout',
	 '/rss', 'RSS',
	 '/(.*)', 'error'
       )

# Para poder usar sesiones con web.py
web.config.debug = False

app = web.application(urls, globals())

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

#Conexion local
ip = '127.0.0.1'
conexion = pymongo.Connection(ip)

# Creando/obteniendo un objeto que referencie a la base de datos.
db = conexion['bdregistro'] #base de datos a usar

# Coleccion con registros de los usuarios
datos = db['usuarios']

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

#Formulario RSS
form_rss = form.Form (
	form.Textbox ('enlace_rss', form.notnull, description='RSS:'),
	form.Button ('Buscar'),

	validators = [
		form.Validator("Formato de enlace rss no valido.", lambda i: rss.match(i.enlace_rss))
	]

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

			resul = datos.find_one({"nombre": usuario, "Password": passwd}) #buscamos al usuario

			if(str(resul) == "None"):
				r.password.set_value("")
				men = "El usuario o el password no son validos."
				return plantillas.login(reg=r ,mensaje=men)
			else:
				sesion.usuario=usuario
				ses = sesion.usuario
				return plantillas.bienvenido(nombre = ses)


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
			registro_usuario = {"nombre": i.nombre, "apellidos": i.apellidos, "dni": i.dni, "email": i.correo, "fecha_nac": i.dia + i.mes + i.anio, "direccion": i.direccion, "Password": i.passw, "numero_visa": i.numero_visa}
			datos.insert(registro_usuario) #inserto los datos del usuario en la base de datos
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
			dni_pas = i.dni
			res = []

			resul = datos.find_one({"dni": dni_pas}, {"nombre":1, "apellidos":1, "_id":0 }) #buscamos al usuario

			if str(resul) == "None":
				return 'No existe ningun usuario con ese dni.'
			else:
				return "Nombre: " + resul["nombre"] + "\n" + "Apellidos: " + resul["apellidos"] + "\n"


class RSS:
	def GET (self):
		r=form_rss()
		web.header('Content-Type', 'text/html; charset=utf-8')
		return plantillas.rss(reg=r, mensaje = '')



if __name__ == "__main__":
    app.run()
