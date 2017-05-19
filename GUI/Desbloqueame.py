#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import gtk
import math
import subprocess

__author__ = "Diego Rodrigo Verdugo <diego-break-[at]hotmail.com>"
__version__ = 1.0
__date__ = "14 de Mayo de 2017"

class Coche():
	def __init__(self, tam, letras, movimiento, coordenada, principal=False):

		self.tam = tam 			#Tamaño del coche
		self.letras = letras	#Tupla con las letras (Mayuscula, Minuscula)
		self.movimiento = movimiento	#Horizontal 'H' o Vertical 'V'
		self.coordenada = [coordenada[0], coordenada[1]]	#lista con las coordenadas [x,y]
		self.principal = principal 		#True si el color tiene que ser rojo(coche principal), false si no

class Parking():
	
	def cargar_coches(self,n, niveles):
		#Devuelve una lista de objetos coche que corresponden al nivel n de la lista niveles
		#Number Of Color (noc)

		coches = []
		carga = niveles[n]
		for i in range(carga[0]):	#Al principio de cada nivel hay un int que corresponde al numero de coches en el nivel
			movimiento = carga[i+1][0]	#Corresponde al caracter 'H' o 'V'
			coordx = int(carga[i+1][1])	#Coordenada X
			coordy = int(carga[i+1][2])	#Coordenada Y (raw)
			coordenada = [coordx, coordy]	
			tam = int(carga[i+1][3])	#Tamaño del coche
			if i == 0: color = True		#El primer coche (i=0) es el principal
			else: color = False 		
			letras = (chr(ord('A')+i) , chr(ord('a')+i)) 	#Algoritmo para almacenar en una tupla una letra diferente al resto de coches
			coches.append(Coche(tam, letras, movimiento, coordenada, color))	#Crear el coche con estos datos y almacenarlo en la lista
			#print(tam, letras, movimiento, coordenada, color,)
		return coches 	#Lista con todos los coches creados

	def control_nivel(self):
		#Devuelve el livel maximo al que esta permitido jugar segun sus puntuaciones
		if 0 in self.records[1:]:	#Si no se ha pasado todos los niveles
			self.nivel_max = self.records.index(0,1) #El primer nivel sin pasarse es el maximo
		else:	#Si se ha pasado todos
			self.nivel_max = self.niveles[0]+1	#El nivel maximo corresponde con el numero total de niveles + 1

	def seleccion_nivel(self, widget,event = None, level= None):
		if(level == None): self.initconf(event)
		else: self.initconf(level)

	def elegir_principal(self, widget, principal):
		self.vehiculo_principal = "Principal"+str(principal)+".png"

	def reiniciar(self, widget, level = None):
		self.mainbox.remove(self.separador)
		self.separador = gtk.Fixed()
		self.mainbox.remove(self.menu_bar)
		#self.menu_barra()
		self.initconf(level)

	def cerrar(self, widget = None, event = None):
		return False

	def mostrar_ayuda(self, widget, event = None):
		st = """  Si ocurre algun problema durante la ejecucion de este juego siga los siguientes pasos:
		-> Revise que en la misma carpeta que este juego este la carpeta Templates, y que no este vacia   
		-> Compruebe que tiene instalado gtk2
		-> Si aun asi no funciona puede descargar la ultima version del juego en el siguiente enlace:
		"""
		win = gtk.Window()
		text = gtk.Label(st)
		win.set_title("Ayuda")
		win.set_resizable(False)
		link = gtk.LinkButton("https://github.com/DVRodri8/Game-Desbloqueame", "Mi GitHub")
		box = gtk.VBox()
		box.pack_start(text, False, False, 0)
		box.pack_start(link, False, False, 0)
		win.add(box)
		win.show_all()
		win.connect('destroy', self.cerrar)

	def estado(self, widget, data = None):
		print(self.records)
		#self.internal.imprimir()
		#print("El contador vale: {} \nY la lista de jugadas es:\n{}".format(self.contador, self.lista_jugadas))

	def go_principal(self, widget):
		self.main_window.remove(self.mainbox)
		self.initprincipal()
		self.main_window.show_all()

	def guardar_records(self, widget = None, data=None):

		fichero = open('records.uva', 'w')
		fichero.seek(0)
		for record in self.records:
			fichero.write(str(record)+'\n')
		fichero.close()

	def change_route(self, widget = None, event= None):
		if(self.ruta == "Coches"): self.ruta = "Barcos"
		else: self.ruta = "Coches" 

		self.mainbox.remove(self.menu_bar)
		self.menu_barra_inicio()

	def cerrar2(self, widget):
		self.win.destroy()

	def desbloquear(self, widget, event = None):
		if(self.money >= 800):
			self.money -= 800
			self.records[0] = self.money
			self.bloq = False
			self.elegir_principal(None, 5)
		else:
			win = gtk.Window()
			win.set_title("Bloqueado")
			win.set_resizable(False)
			win.set_default_size(300,300)
			label = gtk.Label("<span font = '16' foreground = 'green' background = 'white'> Este coche esta bloqueado\t\t\t\t\t\n Cada vez que lo quieras seleccionar tienes\t\n que pagar 800 monedas\t\t\t\t\t\t</span>")
			label.set_use_markup(True)
			label.show()
			win.add(label)
			win.connect('destroy', self.cerrar)
			win.show_all()
	def nuevo_principal(self, widget = None, event = None):
		
		self.win = gtk.Window()
		self.win.set_title("Vehiculos Principales")
		self.win.set_resizable(False)
		self.win.set_default_size(300,300)
		box = gtk.HBox()
		dinero = gtk.Label("Money: "+ str(self.money))
		dinero.show()
		box.pack_start(dinero, False, False, 5)
		
		if self.ruta == "Coches": x = 5
		else: x = 5
		
		for i in range(x):
			img = gtk.Image()
			img.set_from_file("./Templates/"+self.ruta+"/Principal{}.png".format(i+1))
			img.show()

			boton = gtk.Button()
			boton.set_size_request(200, 90)
			boton.set_image(img)
			if(i == 4 and not self.bloq): boton.connect('clicked', self.elegir_principal, i+1)
			else: boton.connect('clicked', self.desbloquear, i+1)
			boton.connect('clicked', self.cerrar2)

			box.pack_start(boton, False, False, 5)


		self.win.add(box)
		self.win.show_all()
		self.win.connect('destroy', self.cerrar)

	def felicitacion_especial(self):
		
		self.mainbox.remove(self.separador)
		self.separador = gtk.Fixed()
		self.mainbox.pack_start(self.separador)

		#music = pyglet.resource.media('./Templates/aplausos2.mp3')
		#music.play()
		#pyglet.app.run()

		gif = gtk.Image()
		gif.set_from_file("./Templates/"+self.ruta+"/fin.gif")
		gif.set_size_request(615,615)
		gif.show()
		self.separador.put(gif, 0,0)

		personaje = gtk.Image()
		personaje.set_from_file("./Templates/"+self.ruta+"/tutorial.png")
		personaje.show()
		if self.ruta == 'Coches': texto = gtk.Label("<span font = '18' foreground = 'black'>Gracias a ti hemos vuelto\na nuestro tiempo con Doc</span>")
		else: texto = gtk.Label("<span font = '18' foreground = 'black'>Gracias a ti hemos escapado\ny tenemos mucho ron</span>")

		texto.set_use_markup(True)
		texto.show()

		box = gtk.EventBox()
		box.add(personaje)
		box.connect('button-press-event', self.initmenu)
		box.set_visible_window(False)

		self.separador.put(box, 0, 0)
		self.separador.put(texto, 100, 140)

		subprocess.Popen(['aplay','-q', './Templates/Aplausos2.wav'])

		self.main_window.show_all()
	
	def fin_partida(self):
		
		#self.main_window.remove(self.separador)
		self.arrastrando = False
		if(self.contador < self.records[self.nivel_actual] or self.records[self.nivel_actual] == 0): self.records[self.nivel_actual] = self.contador
		self.money += 200
		self.records[0] = self.money
		if self.nivel_actual == 20: self.felicitacion_especial()
		else: self.felicitaciones()

	
	def actualizar_movimientos(self):
		if(self.contador < self.records[self.nivel_actual] or self.records[self.nivel_actual] == 0): color = "green"
		elif(self.contador == self.records[self.nivel_actual]): color = "orange"
		else: color = "red"
		self.info_movimientos.set_text('<span font = "22" foreground="{}"> {} </span>'.format(color, self.contador))
		self.info_movimientos.set_use_markup(True)

	def deshacer_jugada(self, widget, data = None):
		if self.contador != 0:
			ultima_jugada = self.lista_jugadas.pop()
			if ultima_jugada >= 'A' and ultima_jugada <= 'Z': deshacer = ultima_jugada.lower()
			else: deshacer = ultima_jugada.upper()
			self.internal.mover_coche(self.coches[ultima_jugada.lower()], deshacer)
			
			self.contador -= 1
			self.actualizar_movimientos()

			coche = self.coches[ultima_jugada.lower()]
			if coche.movimiento == 'H':
				if ultima_jugada >= 'A' and ultima_jugada <= 'Z': 
					self.tablero.move(self.widget[coche.letras[1].lower()], self.map[coche][0] + 96, self.map[coche][1])
					self.map[coche] = [self.map[coche][0] + 96, self.map[coche][1]]

				else: 
					self.tablero.move(self.widget[coche.letras[1].lower()], self.map[coche][0] - 96, self.map[coche][1])
					self.map[coche] = [self.map[coche][0] - 96, self.map[coche][1]]

			else:
				if ultima_jugada >= 'A' and ultima_jugada <= 'Z':
					self.tablero.move(self.widget[coche.letras[1].lower()], self.map[coche][0], self.map[coche][1]+96)
					self.map[coche] = [self.map[coche][0], self.map[coche][1]+96]

				else: 
					self.tablero.move(self.widget[coche.letras[1].lower()], self.map[coche][0], self.map[coche][1]-96)
					self.map[coche] = [self.map[coche][0], self.map[coche][1]-96]

	def presionar(self,widget, event, data):
		self.arrastrando = True
		self.dif_x = int(event.x_root) - self.map[data][0]
		self.dif_y = int(event.y_root) - self.map[data][1]
		self.anterior_x = int(event.x_root) - self.dif_x
		self.anterior_y = int(event.y_root) - self.dif_y
		#self.internal.imprimir()
		return gtk.TRUE

	def arrastrar(self, widget, event, data):
		if not self.arrastrando: return gtk.FALSE
		if (data.movimiento == 'H'):
			casilla_inicio = data.coordenada[0]
			lista_casillas = [25, 123, 221, 319, 417, 515, 613]
			dx = int(event.x_root) - self.dif_x
			casilla_actual = 0
			for i,casilla in enumerate(lista_casillas):
				if dx < casilla: 
					casilla_actual = i
					break
			if(self.anterior_x < dx): casilla_actual += 1
			
			#if(self.anterior < dx): 
			dy = self.map[data][1] #int(event.y_root) - self.dif_y

			if(casilla_actual > casilla_inicio): jugada = data.letras[1]
			elif(casilla_inicio == casilla_actual): jugada = None
			else: jugada = data.letras[0]
			#print(casilla_inicio, casilla_actual, dx)
			bandera = True
			if jugada is not None: 
				bandera = self.internal.mover_coche(data,jugada)
				if(bandera):
					self.contador += 1
					self.actualizar_movimientos()
					self.lista_jugadas.append(jugada)
					#print(self.contador, self.lista_jugadas)
			if(self.internal.terminado()): self.fin_partida()
			
			if(dx < 615 - data.tam*98 and dx > 25 and bandera):
				self.tablero.move(widget, dx, dy)
				self.map[data] = [dx, dy]
		else:
			lista_casillas = [75, 171, 267, 363, 461, 559, 657]
			casilla_inicio = data.coordenada[1]
			dx = self.map[data][0]
			dy = int(event.y_root) - self.dif_y
			for i,casilla in enumerate(lista_casillas):
				if dy < casilla: 
					casilla_actual = i
					break
			if(self.anterior_y < dy): casilla_actual += 1

			if(casilla_actual > casilla_inicio): jugada = data.letras[1]
			elif(casilla_inicio == casilla_actual): jugada = None
			else: jugada = data.letras[0]

			bandera = True
			if jugada is not None:
				bandera = self.internal.mover_coche(data,jugada)
				if(bandera):
					self.contador += 1
					self.lista_jugadas.append(jugada)
					self.actualizar_movimientos()

			if(dy < 655 - data.tam * 96  and dy > 75 and bandera):
				self.tablero.move(widget, dx, dy)
				self.map[data] = [dx, dy]	

		return gtk.TRUE
	
	def soltar(self, widget, event, data):
		self.arrastrando = False
		posx = self.map[data][0]
		posy = self.map[data][1]
		#print(posy)
		if(data.movimiento == 'H'):
			posx -= 25
			casillas = int(round(float(posx) / 98.0)+1)
			print(data.coordenada[0] , casillas)
			clave = data.coordenada[0] - casillas
			if clave < 0: 
				while(clave < 0):
					self.internal.mover_coche(data, data.letras[1])
					clave += 1
					self.contador -= 1
					self.actualizar_movimientos()
					self.lista_jugadas.pop()
			elif clave > 0: 
				while(clave > 0):	
					self.internal.mover_coche(data, data.letras[0])
					clave -= 1
					self.contador -= 1
					self.actualizar_movimientos()
					self.lista_jugadas.pop()

			posx = 96*(casillas-1) + 25
			self.tablero.move(widget, posx, posy)
			self.map[data] = [posx, posy]
		else:
			posy -= 76
			casillas = int(round(float(posy) / 96.0)+1)
			#print(data.coordenada[1] , casillas)
			if data.coordenada[1] < casillas: 
				self.internal.mover_coche(data, data.letras[1])
				self.contador -= 1
				self.actualizar_movimientos()
				self.lista_jugadas.pop()
			elif data.coordenada[1] > casillas: 
				self.internal.mover_coche(data, data.letras[0])
				self.contador -= 1
				self.actualizar_movimientos()
				self.lista_jugadas.pop()

			posy = 96*(casillas-1) + 75
			self.tablero.move(widget, posx, posy)
			self.map[data] = [posx, posy]
		return gtk.TRUE

	def menu_barra(self):

		self.agr = gtk.AccelGroup()
		self.main_window.add_accel_group(self.agr)

		self.menu_bar = gtk.MenuBar()
		self.mainbox.pack_start(self.menu_bar, False, False, 0)
		self.menu_bar.show()

		# Menu desplegable de Juego
		self.root_juego = gtk.MenuItem("Juego")
		self.root_juego.show()
		self.menu_juego = gtk.Menu()

		self.menu_juego_item1 = gtk.ImageMenuItem("Ayuda", self.agr)
		self.key, self.mod = gtk.accelerator_parse("F1")
		self.menu_juego_item1.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
		self.menu_juego_item1.connect("activate", self.mostrar_ayuda, "Help")
		self.menu_juego.append(self.menu_juego_item1)
		self.menu_juego_item1.show()

		self.menu_juego_item2 = gtk.ImageMenuItem("Deshacer jugada", self.agr)
		self.key, self.mod = gtk.accelerator_parse("<Control>Z")
		self.menu_juego_item2.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
		self.menu_juego_item2.connect("activate", self.deshacer_jugada, "Undo")
		self.menu_juego.append(self.menu_juego_item2)
		self.menu_juego_item2.show()

		self.menu_juego_item3 = gtk.ImageMenuItem("Guardar records", self.agr)
		self.key, self.mod = gtk.accelerator_parse("<Control>S")
		self.menu_juego_item3.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
		self.menu_juego_item3.connect("activate", self.guardar_records, "Save")
		self.menu_juego.append(self.menu_juego_item3)
		self.menu_juego_item3.show()

		self.root_juego.set_submenu(self.menu_juego)
		self.menu_bar.append(self.root_juego)

	def menu_barra_inicio(self):
		
		if(self.ruta == "Coches"): 
			tex = "Jugar en Modo Barcos"
			texto = "Cambiar coche principal"
		else: 
			tex = "Jugar en Modo Coches"
			texto = "Cambiar barco principal"

		self.agr = gtk.AccelGroup()
		self.main_window.add_accel_group(self.agr)

		self.menu_bar = gtk.MenuBar()
		self.mainbox.pack_start(self.menu_bar, False, False, 0)
		self.menu_bar.show()

		# Menu desplegable de Juego
		self.root_juego = gtk.MenuItem("Opciones")
		self.root_juego.show()
		self.menu_juego = gtk.Menu()

		self.menu_juego_item1 = gtk.ImageMenuItem("Ayuda", self.agr)
		self.key, self.mod = gtk.accelerator_parse("F1")
		self.menu_juego_item1.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
		self.menu_juego_item1.connect("activate", self.mostrar_ayuda, "Help")
		self.menu_juego.append(self.menu_juego_item1)
		self.menu_juego_item1.show()

		self.menu_juego_item2 = gtk.ImageMenuItem(tex, self.agr)
		self.key, self.mod = gtk.accelerator_parse("<Control>T")
		self.menu_juego_item2.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
		self.menu_juego_item2.connect("activate", self.change_route, "Apariencia")
		self.menu_juego.append(self.menu_juego_item2)
		self.menu_juego_item2.show()

		self.menu_juego_item3 = gtk.ImageMenuItem(texto, self.agr)
		self.key, self.mod = gtk.accelerator_parse("<Control>P")
		self.menu_juego_item3.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
		self.menu_juego_item3.connect("activate", self.nuevo_principal, "Apariencia")
		self.menu_juego.append(self.menu_juego_item3)
		self.menu_juego_item3.show()

		self.menu_juego_item4 = gtk.ImageMenuItem("Guardar records", self.agr)
		self.key, self.mod = gtk.accelerator_parse("<Control>S")
		self.menu_juego_item4.add_accelerator("activate", self.agr, self.key, self.mod, gtk.ACCEL_VISIBLE)
		self.menu_juego_item4.connect("activate", self.guardar_records, "Save")
		self.menu_juego.append(self.menu_juego_item4)
		self.menu_juego_item4.show()
	

		self.root_juego.set_submenu(self.menu_juego)
		self.menu_bar.append(self.root_juego)

	def insertar_detalle(self):

		detalle = gtk.Image()
		detalle.set_from_file("./Templates/"+ self.ruta +"/detalle.png")
		detalle.show()
		
		detalle2 = gtk.Image()
		detalle2.set_from_file("./Templates/"+ self.ruta +"/detalle.png")
		detalle2.show()

		detalle3 = gtk.Image()
		detalle3.set_from_file("./Templates/"+ self.ruta +"/detalle.png")
		detalle3.show()

		detalle4 = gtk.Image()
		detalle4.set_from_file("./Templates/"+ self.ruta +"/detalle.png")
		detalle4.show()

		self.caja_derecha.put(detalle, 200,563)
		self.caja_derecha.put(detalle2, 0,563)
		self.caja_derecha.put(detalle3, 0,600)
		self.caja_derecha.put(detalle4, 200,600)

	def insertar_botonera(self):
		self.boton_reinicio = gtk.Button("Reiniciar")
		self.boton_undo = gtk.Button("Deshacer jugada            ")
		self.boton_menu = gtk.Button("Volver al menu niveles")
		self.boton_reinicio.set_size_request(200,40)
		self.boton_undo.set_size_request(200,40)
		self.boton_menu.set_size_request(200,40)
		self.boton_reinicio.connect('clicked', self.reiniciar, self.nivel_actual)
		self.boton_menu.connect('clicked', self.initmenu)
		self.boton_undo.connect('clicked', self.deshacer_jugada)
		img_undo = gtk.Image()
		img_undo.set_from_file("./Templates/undo.png")
		img_undo.show()
		self.boton_undo.set_image(img_undo)
		self.caja_derecha.put(self.boton_reinicio, 10, 470)
		self.caja_derecha.put(self.boton_undo, 10, 520)
		self.caja_derecha.put(self.boton_menu, 10, 570)

	def insertar_decorado(self):
		calavera = gtk.Image()
		calavera.set_from_file("./Templates/" + self.ruta + "/decorado.png")
		calavera.show()
		self.caja_derecha.put(calavera, 30, 200)

	def insertar_informacion(self):
		c_move = gtk.Image()
		c_move.set_from_file("./Templates/Mov.png")
		c_move.show()
		self.caja_derecha.put(c_move, 0, 60)

		c_reco = gtk.Image()
		c_reco.set_from_file("./Templates/Reco.png")
		c_reco.show()
		self.caja_derecha.put(c_reco, 0, 120)

		self.info_nivel = gtk.Label()
		self.info_nivel.set_text('<span font="20" foreground="orange"> <i>      Nivel {}      </i></span>'.format(self.nivel_actual))
		self.info_nivel.set_use_markup(True)
		self.info_movimientos = gtk.Label('<span font = "22" foreground="green" > 0 </span>')
		self.info_movimientos.set_use_markup(True)
		if self.records[self.nivel_actual] == 0: reco = "n/a"
		else: reco = self.records[self.nivel_actual] 
		self.info_records = gtk.Label("<span font = '22' foreground='black'> {} </span>".format(reco))
		self.info_records.set_use_markup(True)

		self.tablero.put(self.info_nivel, 190, 10)
		self.caja_derecha.put(self.info_movimientos, 188, 73)
		self.caja_derecha.put(self.info_records, 195, 130)

	def poner_fondo(self):
		self.fondo = gtk.Image()
		self.fondo.set_from_file("./Templates/"+ self.ruta +"/fondo.png")
		self.box_fondo = gtk.EventBox()
		self.box_fondo.set_visible_window(False)
		self.box_fondo.add(self.fondo)
		self.tablero.put(self.box_fondo, 0, 50)
		self.box_fondo.set_size_request(615, 615)

	def cargar_escenario(self):
		self.mainbox.remove(self.separador)
		self.mainbox.remove(self.menu_bar)

		self.separador = gtk.HBox()
		self.mainbox.pack_end(self.separador, False, True)
		self.caja_derecha = gtk.Fixed()
		self.tablero = gtk.Fixed()
		self.separador.pack_start(self.tablero, False, True)
		self.separador.pack_start(self.caja_derecha, False, True, 10)
		self.main_window.add(self.mainbox)

		self.nivel_actual = 1

		self.insertar_decorado()
		self.insertar_botonera()
		self.insertar_informacion()
		self.insertar_decorado()
		self.insertar_detalle()
		self.poner_fondo()

		self.boton_menu.set_sensitive(False)
		self.boton_reinicio.set_sensitive(False)
		self.boton_undo.set_sensitive(False)

	def next_msg(self, widget = None, event = None):
		
		mensajes_mcfly = ["<span font = '18' foreground = 'black'>Hola, soy Marty McFly,\nnecesito tu ayuda para\nencontrarme con Doc y poder\nregresar a nuestro tiempo</span>", "<span font = '18' foreground = 'black'>Para ello hay que despejar\nel camino de nuestro coche\nhasta la puerta del garaje.</span>","<span font='18' foreground = 'black'>Parece ser que estos coches\ndel futuro no tienen la capacidad\nde girar así que sólo podrás\nmoverlos hacia delante\no hacia atrás.</span>","<span font = '18' foreground = 'black'>A tu derecha tienes\ninformacion y opciones, ademas,\npuedes cambiar el aspecto\ndesde el menu principal</span>"]
		mensajes_sparrow = ["<span font = '18' foreground = 'black'>Maldita sea, nuestro barco\nha sido bloqueado… y\nse está acabando el ron!!\nAyúdame a salir del puerto</span>", "<span font = '18' foreground = 'black'>Para ello hay que mover\ntodos los barcos que bloquean\nnuestro paso.\nEspera un momento…</span>","<span font='17.7' foreground = 'black'>¡Estos barcos no tienen timón!\nSólo podrás moverlos hacia\ndelante o hacia atrás.\nBuena suerte</span>","<span font = '18' foreground = 'black'>A tu derecha tienes\ninformacion y opciones, ademas,\npuedes cambiar el aspecto\ndesde el menu principal</span>"]

		if(self.ruta == 'Coches'): next_msg = mensajes_mcfly[self.actual_msg]
		else: next_msg = mensajes_sparrow[self.actual_msg]

		self.info_nivel.set_text("")
		self.texto_tuto.set_text(next_msg)
		self.texto_tuto.set_use_markup(True)
		if(self.actual_msg < 3): self.actual_msg += 1

	def felicitaciones(self):

		personaje = gtk.Image()
		personaje.set_from_file("./Templates/"+self.ruta+"/tutorial.png")
		personaje.show()
		if self.ruta == 'Coches': texto = gtk.Label("<span font = '18' foreground = 'black'>Gracias a ti estamos\nmas cerca de Doc</span>")
		else: texto = gtk.Label("<span font = '18' foreground = 'black'>Gracias a ti estamos\nmas cerca de escapar</span>")

		texto.set_use_markup(True)
		texto.show()

		box = gtk.EventBox()
		box.add(personaje)
		box.connect('button-press-event', self.initmenu)
		box.set_visible_window(False)

		self.tablero.put(box, 0, 50)
		self.tablero.put(texto, 100, 160)

		self.boton_reinicio.set_sensitive(False)
		self.boton_undo.set_sensitive(False)
		self.boton_menu.set_sensitive(False)

		self.main_window.show_all()

	def tutorial(self, widget = None):
		
		self.view = True

		self.cargar_escenario()
		personaje = gtk.Image()
		personaje.set_from_file("./Templates/"+self.ruta+"/tutorial.png")
		personaje.show()

		self.actual_msg = 0

		box = gtk.EventBox()
		box.add(personaje)
		box.connect('button-press-event', self.next_msg)
		box.set_visible_window(False)

		self.tablero.put(box,0,50)

		if(self.ruta == "Coches"):personaje = "Mcfly"
		else: personaje = "Sparrow" 
		
		self.info_nivel.set_text('<span font = "20" foreground = "Orange">Bienvenido al tutorial pulsa sobre {} para comenzar</span>'.format(personaje))
		self.info_nivel.set_use_markup(True)
		self.tablero.move(self.info_nivel, 10, 5)
		
		self.texto_tuto = gtk.Label()

		box2 = gtk.EventBox()
		box2.add(self.texto_tuto)
		box2.connect('button-press-event', self.next_msg)
		box2.set_visible_window(False)

		boton_skip = gtk.Button("Salir del tutorial")
		boton_skip.set_size_request(200, 40)
		boton_skip.connect('clicked', self.initmenu)

		self.tablero.put(boton_skip, 60, 550)

		self.tablero.put(box2, 100,140)

		self.main_window.show_all()

	def initconf(self, level = 1):
		
		self.map = {}
		self.coches = {}
		self.widget = {}

		self.nivel_actual = level
		
		self.mainbox.remove(self.separador)
		self.internal = Game()
		self.separador = gtk.HBox()
		self.mainbox.pack_end(self.separador, False, True)
		#self.mainbox.remove(self.menu_bar)
		self.menu_barra()
		
		self.caja_derecha = gtk.Fixed()
		
		self.insertar_botonera()
		self.insertar_decorado()
		
		self.tablero = gtk.Fixed()
		self.separador.pack_start(self.tablero, False, True)
		self.separador.pack_start(self.caja_derecha, False, True, 10)
		self.main_window.add(self.mainbox)

		self.insertar_informacion()
		self.poner_fondo()

		self.contador = 0
		self.lista_jugadas = []
		nivel = self.cargar_coches(level, self.niveles)
		for coche in nivel:
			self.insertar_coche(coche)
		
		self.insertar_detalle()

	def initmenu(self, widget = None, event = None):
		
		if(self.records[1] == 0 and self.view == False): self.tutorial()
		else:

			self.mainbox.remove(self.separador)
			self.separador = gtk.Fixed()
			#self.menu_barra()
			self.mainbox.remove(self.menu_bar)
			img = gtk.Image()
			img.set_from_file("./Templates/Niv.png")
			img.show()
			img.set_size_request(910, 660)
			eb = gtk.EventBox()
			eb.add(img)
			eb.set_visible_window(False)
			self.separador.add(eb)
			self.control_nivel()

			i = 1
			for posy in range(140, 670, 125):
				for pos in range(160,670,125):
					if( i <= 20 ):
						if(i < self.nivel_max): ruta_img = 'Tick50.png'
						elif(i == self.nivel_max): ruta_img = 'Alfa.png'
						else: ruta_img = 'Candado50.png'

						box2 = gtk.EventBox()
						nivel = gtk.Label()
						if(i >= 10): tex = ""
						else: tex = " "
						tex += str(i)+" "
						nivel.set_size_request(100,100)
						nivel.set_text('<span font="65" foreground = "White" background = "black">{}</span>'.format(tex))
						nivel.set_use_markup(True)
						self.separador.put(nivel, pos, posy)
						
						img = gtk.Image()
						img.set_from_file("./Templates/"+ ruta_img)
						img.show()
						img.set_size_request(90,98)
						box2.set_visible_window(False)
						box2.add(img)
						if(i <= self.nivel_max): box2.connect('button-press-event', self.seleccion_nivel, i)
						self.separador.put(box2, pos+5, posy-1)
						i+=1
						
			self.mainbox.pack_end(self.separador, False, False, 0)
			

			img_menu = gtk.Image()
			img_menu.set_from_file("./Templates/Volver.png")
			img_menu.show()
			boton_menu = gtk.Button(" ")
			boton_menu.set_size_request(200, 40)
			boton_menu.connect('clicked', self.go_principal)
			boton_menu.set_image(img_menu)
			self.separador.put(boton_menu, 600, 35)
			self.main_window.show_all()

	def initprincipal(self, widget = None):
		
		self.separador = gtk.HBox()
		self.mainbox = gtk.VBox()
		self.mainbox.pack_end(self.separador, False, False, 0)
		self.main_window.add(self.mainbox)
		self.menu = gtk.Fixed()
		self.separador.pack_start(self.menu, False, False, 0)
		fondo = gtk.Image()
		fondo.set_from_file("./Templates/prin.png")
		fondo.show()
		self.menu.put(fondo, 0,0)
		
		img_jugar = gtk.Image()
		img_jugar.set_from_file("./Templates/jugar.png")
		img_jugar.show()

		img_tutorial = gtk.Image()
		img_tutorial.set_from_file("./Templates/tutorial.png")
		img_tutorial.show()

		img_acerca = gtk.Image()
		img_acerca.set_from_file("./Templates/acerca.png")
		img_acerca.show()

		boton_jugar = gtk.Button(" ")
		boton_tutorial = gtk.Button(" ")
		boton_acerca = gtk.Button(" ")

		boton_jugar.set_image(img_jugar)
		boton_tutorial.set_image(img_tutorial)
		boton_acerca.set_image(img_acerca)

		boton_jugar.connect("clicked", self.initmenu)
		boton_tutorial.connect("clicked", self.tutorial)
		boton_acerca.connect("clicked", self.mostrar_ayuda)

		self.menu.put(boton_jugar, 523, 172)
		self.menu.put(boton_tutorial, 148, 464)
		self.menu.put(boton_acerca, 32, 554)

		boton_jugar.set_size_request(234,55)
		boton_acerca.set_size_request(234,55)
		boton_tutorial.set_size_request(234,55)

		self.menu_barra_inicio()

	def __init__(self, niveles, records):
		
		self.bloq = True
		self.niveles = niveles
		self.records = records
		self.money = self.records[0]
		self.internal = Game()
		self.ruta = "Coches"
		#Creacion de la ventana principal, se conectan sus eventos y se setean sus propiedades
		self.main_window = gtk.Window()
		self.main_window.set_title("¡Desbloqueame!")
		self.main_window.set_resizable(False)
		self.main_window.set_icon_from_file("./Templates/icono.ico")
		self.main_window.connect("destroy", gtk.main_quit)
		self.main_window.move(200,0)

		self.view = False
		self.vehiculo_principal = "Principal1.png"
		self.arrastrando = False
		self.initprincipal()		

		self.main_window.show_all()
		
	def insertar_coche(self, coche):
		self.internal.insertar_coche(coche)
		img = gtk.Image()
		img.show()
		ruta_v = ""
		if(coche.principal): ruta_v = self.vehiculo_principal
		elif (coche.movimiento == 'H'):
			if(coche.tam == 2): ruta_v = "H2.png"
			else: ruta_v = "H3.png"
		elif(coche.tam == 2): ruta_v = "V2.png"
		else: ruta_v = "V3.png"
		img.set_from_file("./Templates/"+ self.ruta + "/" + ruta_v)
		self.box = gtk.EventBox()
		self.box.add(img)
		self.box.set_events((gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK))
		self.box.connect("button_press_event", self.presionar, coche) 
		self.box.connect("button_release_event", self.soltar, coche)
		self.box.connect("motion_notify_event", self.arrastrar, coche)
		self.box.set_visible_window(False)
		self.tablero.put(self.box, 25 + 96*(coche.coordenada[0]-1), 75 + 96 * (coche.coordenada[1] - 1))
		self.map[coche] = [25 + 96*(coche.coordenada[0]-1), 75 + 96 * (coche.coordenada[1] - 1)]
		self.coches[coche.letras[1]] = coche
		self.widget[coche.letras[1]] = self.box
		self.main_window.show_all()

class Game():

	#Objeto Parking es el tablero, en el init se crea una lista bidimensional con los caracteres del tablero
	#Para que sea mas intuitivo a la hora de trabajar con el tablero, cada sublista corresponde al eje X
	#y cada caracter dentro de la sublista pertenece al eje Y
	def __init__(self):

		self.tablero =[ [-1,-1,-1,-1,-1,-1,-1,-1],
						[-1, 0, 0, 0, 0, 0, 0,-1],
						[-1, 0, 0, 0, 0, 0, 0,-1],
						[-1, 0, 0, 0, 0, 0, 0,-1],
						[-1, 0, 0, 0, 0, 0, 0,-1],
						[-1, 0, 0, 0, 0, 0, 0,-1],
						[-1, 0, 0, 0, 0, 0, 0,-1],
						[-1,-1,-1,-2,-1,-1,-1,-1]]


	def insertar_coche(self, car):
		#Mete en el tablero los caracteres del coche que se pase por parametro
		
		#Unicode del color que se completa con el numero de color del objeto coche para decidir el color
		#La parte del unicode '\u2502' corresponde a '|'

		if car.movimiento == 'H':

			i = 0
			while i < car.tam:
				self.tablero[car.coordenada[0]+i][car.coordenada[1]] = car.letras[0]
				i+=1

		else: #Vertical

			i = 0
			while i < car.tam:
				self.tablero[car.coordenada[0]][car.coordenada[1]+i] = car.letras[0]
				i+=1

	def borrar_coche(self, car):
		#Reemplaza los caracteres de un coche por espacios en blanco

		if car.movimiento == 'H':
			
			i = 0
			while i < car.tam:
				
				self.tablero[car.coordenada[0]+i][car.coordenada[1]] = 0
				i+=1

		else: #Vertical

			i = 0
			while i < car.tam:
				self.tablero[car.coordenada[0]][car.coordenada[1]+i] = 0
				i+=1

	def mover_coche(self, car, jugada):
		#Comprueba que puede moverse el coche, si es asi borra el coche, modifica sus coordenadas y lo inserta de nuevo
		#Si el coche no se puede mover imprime por consola un mensaje de error
		#Tambien debuelve True si se ha logrado hacer el movimiento y False si no

		if car.movimiento == 'H':
			if jugada >= 'a' and jugada <= 'z':	
				if self.tablero[car.coordenada[0]+car.tam][car.coordenada[1]] == 0 or self.tablero[car.coordenada[0]+car.tam][car.coordenada[1]] == -2:
					
						self.borrar_coche(car)
						car.coordenada[0]+=1
						self.insertar_coche(car)
						return True
				else:
					#print("Movimiento imposible:",jugada)
					return False
			else: #Mayuscula
				if self.tablero[car.coordenada[0]-1][car.coordenada[1]] == 0:
					self.borrar_coche(car)
					car.coordenada[0]-=1
					self.insertar_coche(car)
					return True
				else:
					#print("Movimiento imposible:",jugada)
					return False	
		else:	#Vertical
			if jugada >= 'a' and jugada <= 'z':	
				if self.tablero[car.coordenada[0]][car.coordenada[1]+car.tam] == 0:
					self.borrar_coche(car)
					car.coordenada[1]+=1
					self.insertar_coche(car)
					return True
				else:
					#print("Movimiento imposible:",jugada)
					return False
			else:	#Mayuscula
				if self.tablero[car.coordenada[0]][car.coordenada[1]-1] == 0:
					self.borrar_coche(car)
					car.coordenada[1]-=1
					self.insertar_coche(car)
					return True
				else:
					#print("Movimiento imposible:",jugada)
					return False

	def imprimir(self):
		i = 1
		j = 1
		while(i < 7):
			j = 1
			while(j < 8):
				print(self.tablero[j][i],' ',  end = '')
				j+=1
			print()
			i+=1

	def terminado(self):
		#Devuelve True si has terminado y False si no
		#Comrprueba que en la ultima casilla del eje X en la posicion de la puerta siga o no el caracter de la puerta

		#print(self.tablero[1][3])
		if(self.tablero[7][3] != -2):
			return True
		else:
			return False

def leer_niveles():
	#Lee el fichero niveles y almacena en la proposicion 0 el numero de niveles,
	#en las siguientes,almacena listas con un nivel en cada una
	#Llena la lista nivel_x con un nivel y lo añade a la lista niveles, hasta que se acaba el fichero

	try:
		fichero = open('niveles.txt', 'r')
		num_niveles = int(fichero.readline())
		i = 0
		niveles = [num_niveles]
		while i < num_niveles:
			nivel_x =[int(fichero.readline())]	#Al principio de cada nivel en el fichero esta el numero de coches de ese nivel
			num_coches = nivel_x[0]
			c = 0
			while c < num_coches:
				nivel_x.append(fichero.readline().replace('\n',''))
				c += 1
			niveles.append(nivel_x)
			nivel_x = []
			i += 1	 
	except:
		print('Error de lectura en el fichero de niveles')#Almacena en la primera posicion el tiempo jugado, y en las demas 
	finally:
		fichero.close()

	return niveles

def leer_records(niveles):
	#Almacena en la primera posicion el tiempo jugado, y en las demas la mejor puntuacion de cada partida
	#almacena un 0 si no se ha jugado a ese nivel

	fichero = open('records.uva', 'a+')
	fichero.seek(0)
	records = fichero.read()
	fichero.close()
	if len(records) == 0:		#Vacio, primera vez que se juega
		records = [200]
		for i in range(niveles[0]):
			records.append(0)

	else:
		records = records.split('\n')
		if '' in records:
			records.remove('')
		
		for i,numero in enumerate(records):
			if i == 0:
				records[i] = float(numero)
			else:	
				records[i] = int(numero)
		
		nuevos = len(niveles) - len(records)
		while nuevos > 0:
		 	records.append(0)
		 	nuevos-= 1

	return records

niveles = leer_niveles()
records = leer_records(niveles)

park = Parking(niveles, records)

gtk.main()
