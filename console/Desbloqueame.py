#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	Author: Diego Rodrigo Verdugo
#	Version: 0.2
#

from __future__ import print_function
from os import system as comando
import sys
import time
import datetime

class Coche:
	def __init__(self, tam, letras, movimiento, coordenada, color=False, num_of_color = 4):

		self.tam = tam 			#Tamaño del coche
		self.letras = letras	#Tupla con las letras (Mayuscula, Minuscula)
		self.movimiento = movimiento	#Horizontal 'H' o Vertical 'V'
		self.coordenada = [coordenada[0], coordenada[1]]	#lista con las coordenadas [x,y]
		self.color = color 		#True si el color tiene que ser rojo(coche principal), false si no
		self.num_of_color = num_of_color	#Numero correspondiente al color de los coches no principales

class Parking:
	#Objeto Parking es el tablero, en el init se crea una lista bidimensional con los caracteres del tablero
	#Para que sea mas intuitivo a la hora de trabajar con el tablero, cada sublista corresponde al eje X
	#y cada caracter dentro de la sublista pertenece al eje Y
	def __init__(self):

		self.tablero =[ [u'\u250C',u'\u251C',u'\u2502',u'\u2502',u'\u251C',u'\u2502',u'\u2502',u'\u251C',u'\u2502',u'\u2502',u'\u251C',u'\u2502',u'\u2502',u'\u251C',u'\u2502',u'\u2502',u'\u251C',u'\u2502',u'\u2502',u'\u2514'],
						[u'\u252C\u2500\u2500\u2500\u2500','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ',u'\u2534\u2500\u2500\u2500\u2500'],
						[u'\u252C\u2500\u2500\u2500\u2500','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ',u'\u2534\u2500\u2500\u2500\u2500'],
						[u'\u252C\u2500\u2500\u2500\u2500','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ',u'\u2534\u2500\u2500\u2500\u2500'],
						[u'\u252C\u2500\u2500\u2500\u2500','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ',u'\u2534\u2500\u2500\u2500\u2500'],
						[u'\u252C\u2500\u2500\u2500\u2500','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ',u'\u2534\u2500\u2500\u2500\u2500'],
						[u'\u252C\u2500\u2500\u2500\u2500','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ',u'\u2534\u2500\u2500\u2500\u2500'],
						[u'\u2510',u'\u2524',u'\u2502',u'\u2502',u'\u2524',u'\u2502',u'\u2502',u'\u2593',u'\u2593',u'\u2593',u'\u2524',u'\u2502',u'\u2502',u'\u2524',u'\u2502',u'\u2502',u'\u2524',u'\u2502',u'\u2502',u'\u2518']]
		
		self.ejeY = len(self.tablero[0])

		self.ejeX = len(self.tablero)
		
	def imprimir_tablero(self):
		#Recorre el tablero para imprimirlo por consola

		columnas=0
		while(columnas<self.ejeY):
			filas=0
			while(filas<self.ejeX):
				print (self.tablero[filas][columnas], end='')
				filas+=1
			print()
			columnas+=1

	def ampliar_tablero(self, cantidad_eje_X = 0, cantidad_eje_Y = 0):
		#Amplia el tablero en tantas casillas como se le indique por parametros

		#Amplia el eje X
		self.ejeX += cantidad_eje_X
		while cantidad_eje_X > 0:
			self.tablero.insert(-1, [u'\u252C\u2500\u2500\u2500\u2500','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ','     ',u'\u2534\u2500\u2500\u2500\u2500'],)
			cantidad_eje_X -=1

		#Amplia el eje Y
		self.ejeY += cantidad_eje_Y*3
		while cantidad_eje_Y > 0:
			for i in range(self.ejeX):
				if i == 0:	#Corresponde al lateral derecho
					self.tablero[i].insert(-1, u'\u251C')
					self.tablero[i].insert(-1, u'\u2502')
					self.tablero[i].insert(-1, u'\u2502')
				elif i == self.ejeX - 1: #Corresponde al lateral izquierdo
					self.tablero[i].insert(-1, u'\u2524')
					self.tablero[i].insert(-1, u'\u2502')
					self.tablero[i].insert(-1, u'\u2502')
				else:	#Corresponde al centro del tablero
					self.tablero[i].insert(-1, '     ')
					self.tablero[i].insert(-1, '     ')
					self.tablero[i].insert(-1, '     ')
			cantidad_eje_Y -= 1

	def insertar_coche(self, car):
		#Mete en el tablero los caracteres del coche que se pase por parametro

		partes_sup_H = [u'\u250C', u'\u2500',u'\u2510']
		partes_inf_H = [u'\u2514',u'\u2500',u'\u2518']
		partes_sup_V = [u'\u250C', u'\u2500', u'\u2510']
		partes_inf_V = [u'\u2514',u'\u2500' , u'\u2518']
		
		#Unicode del color que se completa con el numero de color del objeto coche para decidir el color
		#La parte del unicode '\u2502' corresponde a '|'
		color = u'\u2502\033[4'+str(car.num_of_color)+'m'

		if car.movimiento == 'H':

			i = 0
			while i < car.tam:
				if i == 0:	#Parte de la izquierda del coche
					self.tablero[car.coordenada[0]][car.coordenada[1]] = partes_sup_H[0]+partes_sup_H[1]*4
					self.tablero[car.coordenada[0]][car.coordenada[1]+2] = partes_inf_H[0]+partes_inf_H[1]*4
					#Parte central, aqui se elige el color rojo para el coche principal
					if car.color:	
						self.tablero[car.coordenada[0]][car.coordenada[1]+1] = u'\u2502\033[41m'+car.letras[0]+'      '
					#Si no es el coche principal se colorea del color seleccionado
					else:			
						self.tablero[car.coordenada[0]][car.coordenada[1]+1] = color+car.letras[0]+'      '
				#Parte de la derecha del coche
				elif i == car.tam - 1:	
					self.tablero[car.coordenada[0]+i][car.coordenada[1]] = partes_sup_H[1]*4+partes_sup_H[2]
					self.tablero[car.coordenada[0]+i][car.coordenada[1]+2] = partes_inf_H[1]*4+partes_inf_H[2]
					self.tablero[car.coordenada[0]+i][car.coordenada[1]+1] = car.letras[1]+u'\033[0m\u2502' #Fin de colorear
				#Parte central del coche
				else:	
					self.tablero[car.coordenada[0]+i][car.coordenada[1]] = partes_sup_H[1]*5
					self.tablero[car.coordenada[0]+i][car.coordenada[1]+1] = '     '
					self.tablero[car.coordenada[0]+i][car.coordenada[1]+2] = partes_sup_H[1]*5
				i+=1

		else: #Vertical

			i = 0
			saltos = 3*car.tam -1
			while i <= saltos:
				#Parte superior del coche
				if i == 0:	
					self.tablero[car.coordenada[0]][car.coordenada[1]] = partes_sup_V[0]+partes_sup_V[1]*3+partes_sup_V[2]
				#Primera casilla dentro del coche, lugar de la letra mayuscula
				elif i == 1:
					self.tablero[car.coordenada[0]][car.coordenada[1]+1] = color+' '+car.letras[0]+' '+u'\033[0m\u2502' #Fin de colorear
				#Ultima casilla dentro del coche, lugar de la letra minuscula
				elif i == saltos-1:
					self.tablero[car.coordenada[0]][car.coordenada[1]+i] = color+' '+car.letras[1]+' '+u'\033[0m\u2502' #Fin de colorear
				#Parte inferior del coche
				elif i == saltos:
					self.tablero[car.coordenada[0]][car.coordenada[1]+i] = partes_inf_V[0]+partes_inf_V[1]*3+partes_inf_V[2]
				#Centro del coche
				else:
					self.tablero[car.coordenada[0]][car.coordenada[1]+i] = color+'   '+u'\033[0m\u2502' #Fin de colorear
				i+=1

	def borrar_coche(self, car):
		#Reemplaza los caracteres de un coche por espacios en blanco

		if car.movimiento == 'H':
			
			i = 0
			while i < car.tam:
				
				self.tablero[car.coordenada[0]+i][car.coordenada[1]] = '     '
				self.tablero[car.coordenada[0]+i][car.coordenada[1]+1] = '     '
				self.tablero[car.coordenada[0]+i][car.coordenada[1]+2] = '     '
				
				i+=1

		else: #Vertical

			i = 0
			saltos = 3*car.tam -1
			while i <= saltos:
				self.tablero[car.coordenada[0]][car.coordenada[1]+i] = '     '
				i+=1

	def mover_coche(self, car, jugada):
		#Comprueba que puede moverse el coche, si es asi borra el coche, modifica sus coordenadas y lo inserta de nuevo
		#Si el coche no se puede mover imprime por consola un mensaje de error
		#Tambien debuelve True si se ha logrado hacer el movimiento y False si no

		if car.movimiento == 'H':
			if jugada >= 'a' and jugada <= 'z':	
				if self.tablero[car.coordenada[0]+car.tam][car.coordenada[1]] == '     ' or self.tablero[car.coordenada[0]+car.tam][car.coordenada[1]] == u'\u2593':
					self.borrar_coche(car)
					car.coordenada[0]+=1
					self.insertar_coche(car)
					return True
				else:
					print("Movimiento imposible:",jugada)
					return False
			else: #Mayuscula
				if self.tablero[car.coordenada[0]-1][car.coordenada[1]] == '     ':
					self.borrar_coche(car)
					car.coordenada[0]-=1
					self.insertar_coche(car)
					return True
				else:
					print("Movimiento imposible:",jugada)
					return False	
		else:	#Vertical
			if jugada >= 'a' and jugada <= 'z':	
				if self.tablero[car.coordenada[0]][car.coordenada[1]+car.tam*3] == '     ':
					self.borrar_coche(car)
					car.coordenada[1]+=3
					self.insertar_coche(car)
					return True
				else:
					print("Movimiento imposible:",jugada)
					return False
			else:	#Mayuscula
				if self.tablero[car.coordenada[0]][car.coordenada[1]-1] == '     ':
					self.borrar_coche(car)
					car.coordenada[1]-=3
					self.insertar_coche(car)
					return True
				else:
					print("Movimiento imposible:",jugada)
					return False

	def terminado(self):
		#Devuelve True si has terminado y False si no
		#Comrprueba que en la ultima casilla del eje X en la posicion de la puerta siga o no el caracter de la puerta

		if self.tablero[self.ejeX-1][9] != u'\u2593':
			return True
		else:
			return False

def menu():
	print(
				"""\033[35m
		 ****************************\033[36m
		|----------------------------|
		|            \033[32mMENU            \033[36m|
		|----------------------------|
		|                            |
		|     1. Jugar               |
		|     2. Tiempo jugado       |
		|     3. Cambiar colores     |
		|                            |\033[35m
		 ****************************\033[0m""")

def cargar_coches(n, niveles, noc):
	#Devuelve una lista de objetos coche que corresponden al nivel n de la lista niveles
	#Number Of Color (noc)

	coches = []
	carga = niveles[n]
	for i in range(carga[0]):	#Al principio de cada nivel hay un int que corresponde al numero de coches en el nivel
		num_of_color = noc 		#Numero que indica el color
		movimiento = carga[i+1][0]	#Corresponde al caracter 'H' o 'V'
		coordx = int(carga[i+1][1])	#Coordenada X
		coordy = int(carga[i+1][2])	#Coordenada Y (raw)
		coordy += (coordy-1)*2		#Coordenada Y tratada para que corresponda con el tablero
		coordenada = [coordx, coordy]	
		tam = int(carga[i+1][3])	#Tamaño del coche
		if i == 0: color = True		#El primer coche (i=0) es el principal
		else: color = False 		
		letras = (chr(ord('A')+i) , chr(ord('a')+i)) 	#Algoritmo para almacenar en una tupla una letra diferente al resto de coches
		coches.append(Coche(tam, letras, movimiento, coordenada, color, num_of_color))	#Crear el coche con estos datos y almacenarlo en la lista
	return coches 	#Lista con todos los coches creados

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

	fichero = open('records.txt', 'a+')
	fichero.seek(0)
	records = fichero.read()
	fichero.close()
	if len(records) == 0:		#Vacio, primera vez que se juega
		records = [0.0]
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
	
def control_nivel(records, niveles):
	#Devuelve el livel maximo al que esta permitido jugar segun sus puntuaciones
	if 0 in records:	#Si no se ha pasado todos los niveles
		nivel_max = records.index(0,1) #El primer nivel sin pasarse es el maximo
	else:	#Si se ha pasado todos
		nivel_max = niveles[0]	#El nivel maximo corresponde con el numero total de niveles

	return nivel_max

def menu_niveles(records, nivel_max, nivel_totales):
	#Imprime un menu con los niveles y una informacion de su estado

	for i,elemento in enumerate(records):
				#La primera frase antes de los niveles
				if i == 0:	
					print ("Hay {} niveles en esta version del juego:".format(nivel_totales))
				#Niveles ya pasados en verde
				elif i < nivel_max or nivel_max == nivel_totales and records[i] != 0:	
					print("\033[32mNivel {}: Record actual({})\033[0m".format(i,records[i]))
				#Nivel permitido sin record (subrayado en verde)
				elif i == nivel_max and nivel_max <= nivel_totales:		
					print("\033[37mNivel {}: \033[42m¡NUEVO!\033[0m".format(i))
				#Nivel bloqueado en rojo
				else:	
					print("Nivel {}: \033[31mBLOQUEADO\033[0m".format(i)) 	
	print('Teclee "salir" para guardar y salir')

def pedir_selector():
	#Se pide una opcion y comprueba que sea posible
	#Incluye el comando salir que devuelve 0 

	bandera = True
	while bandera:
		selector = input("Inserte el numero de la opcion deseada: ")
		if selector.lower() == 'salir':
			return 0
		if selector.isdigit():
			selector = int(selector)
			if selector >= 1 and selector <= 3:
				bandera = False
	return selector

def pedir_nivel(nivel_max, dt, records):
	#Pide un nivel y comprueba que sea un valor aceptado
	#Tambien incluye el comando 'salir' que devuelve 0 y guarda el tiempo jugado

	bandera = True
	while bandera:
		nivel = input("Inserte el numero de la opcion deseada: ")
		if(nivel.lower()) == "salir":
			t = datetime.datetime.now()	#t contiene la fecha actual
			tiempo_partida = t-dt	#tiempo_partida contiene la diferencia entre la fecha en que empezo el juego y la actual
			tiempo_partida_sec = float(tiempo_partida.hour*3600 + tiempo_partida.minute*60 + tiempo_partida.second)	#Guarda, en segundos, el tiempo jugado
			records[0] += tiempo_partida_sec	
			return 0
		if nivel.isdigit():
			nivel = int(nivel)
			if nivel >= 1 and nivel <= nivel_max:	#Niveles aceptados
				bandera = False
	return nivel

def imprimir_tiempo(records):
	#Imprime por consola el tiempo total jugado, en records[0] esta el tiempo total jugado en segundos

	time = float(records[0])
	horas = int(time/3600)
	time = time/3600 - horas 	#Quito la parte entera correspondiente a las horas
	time = time*60 				#Lo paso a minutos
	minutos = int(time)
	segundos = int((time-minutos)*60) 	#Quito la parte entera correspondiente a los minutos y lo paso a segundos
	print("LLEVAS {} HORAS {} MINUTOS {} SEGUNDOS".format(horas,minutos,segundos))
	input('INTRO PARA VOLVER AL MENU')

def jugadas_permitidas(jugadas, coches):
	#Comprueba que la jugada introducida corresponda a la letra de un coche

	cantidad = len(coches)
	letras = []
	for i in range(cantidad):
		letras.append(chr(97+i))

	permiso = True
	for jugada in jugadas:
		if not jugada.lower() in letras and not jugada == '.':
			permiso = False
	return permiso

def guardar_records(records):
	#Guarda en el fichero records.txt el tiempo jugado y todos los records

	fichero = open('records.txt', 'w')
	fichero.seek(0)
	for record in records:
		fichero.write(str(record)+'\n')
	fichero.close()

def menu_color():
	#Imprime un menu con unos ejemplos de colores para escoger

	print("""
		Escoja un color que se vea bien en su pantalla:
		
		1: Grey '\033[40mA a\033[0m' 
		2: Green '\033[42mA a\033[0m'
		3: Yellow '\033[43mA a\033[0m'
		4: Blue '\033[44mA a\033[0m'
		5: Magenta '\033[45mA a\033[0m'
		6: Cyan '\033[46mA a\033[0m'
		""")

def pedir_color():
	#Comprueba que este dentro del rango permitido y devuelve el resultado
	#En el caso del gris (1) lo cambia por un 0, que es el numero que le corresponde realmente
	#En el reto de casos devuelve directamente el numero

	bandera = True
	while bandera:
		noc = input("Inserte el numero de la opcion deseada: ")
		if noc.isdigit():
			noc = int(noc)
			if noc >= 1 and noc <= 6:
				bandera = False
	if noc == 1:
		noc -= 1
	return noc

def jugar(nivel, niveles, records, noc):
	#Juega al nivel indicado y modifica los records si es necesario
	#Incluye los comandos 'salir'(devuelve 2) y 'reset'(devuelve 1)

	coches = cargar_coches(nivel, niveles, noc)
	park = Parking()
	for coche in coches:
		park.insertar_coche(coche)
	sys.stdout.flush()
	comando('clear')
	#Si hay un record establecido
	if records[nivel] > 0:	
		print("NIVEL {} - RECORD {} movimientos".format(nivel, records[nivel]))
	#Si es la primera vez que juega al nivel
	else:
		print("NIVEL "+ str(nivel))

	park.imprimir_tablero()
	contador_de_jugadas = 0
	lista_para_retrojugadas = []
	while not park.terminado():
		jugadas = input('Inserte su/s jugada/s: ')
		if jugadas.lower() == 'salir':
			return 2
		elif jugadas.lower() == 'reset':
			return 1
		#Elimina el salto de linea final, separa las jugadas en una lista y comprueba que correspondan a coches
		jugadas = jugadas.replace('\n', '')
		jugadas = list(jugadas)	
		if '' in jugadas:
			jugadas.remove('')
		if jugadas_permitidas(jugadas, coches):
			#Para cada jugada, identifica el coche por su letra y hace la jugada, ademas incrementa el contador en cada jugada
			for jugada in jugadas:
				if jugada == '.':
					if len(lista_para_retrojugadas) > 0:	
						new_jugada = lista_para_retrojugadas.pop()
						if ord(new_jugada) >= ord('a') and ord(new_jugada) <= ord('z'):
							new_jugada = chr(ord(new_jugada) - 32)
						else:
							new_jugada = chr(ord(new_jugada) +32)
						park.mover_coche(coches[int(ord(new_jugada.lower())-97)],new_jugada)
						contador_de_jugadas -= 1
						continue				

				elif park.mover_coche(coches[int(ord(jugada.lower())-97)],jugada):
					lista_para_retrojugadas.append(jugada)
					contador_de_jugadas += 1
					if park.terminado():
						break
				else: break
		else:
			print("Ha introducido una jugada no valida")
		
		#Una vez realizados los cambios se borra el tablero y se imprime el tablero modificado
		sys.stdout.flush()
		comando('clear')
		if records[nivel] > 0:
			print("NIVEL {} - RECORD {} movimientos".format(nivel, records[nivel]))
		else:
			print("NIVEL "+ str(nivel))
		print("\t  Llevas {} movimientos".format(contador_de_jugadas))
		park.imprimir_tablero()

	#Modifica la lista records si se ha batido el record
	if records[nivel] == 0 or records[nivel] > contador_de_jugadas:
		records[nivel] = contador_de_jugadas
		print("FELICIDADES, has completado el nivel en {} movimientos.\n¡Es un nuevo record!".format(contador_de_jugadas))	
	else:
		print("FELICIDADES, has completado el nivel en {} movimientos".format(contador_de_jugadas))
	print(lista_para_retrojugadas)


comando('clear')
niveles = leer_niveles()
records = leer_records(niveles)
noc = 4	#Por defecto el color es Azul oscuro
seguir = True
#Nada mas iniciar se captura la fecha y hora para posteriormente saber cuanto tiempo ha jugado
dt = datetime.datetime.now()
dt = datetime.timedelta(hours= dt.hour, minutes=dt.minute, seconds = dt.second)
menu()
selector = pedir_selector()
if selector == 0: seguir = False		#Corresponde al comando 'salir'
while  seguir:
	bandera = True
	while bandera:
		nivel_max = control_nivel(records, niveles)
		if selector == 1:	#Jugar
			if nivel_max == 1:	#Primera vez que juega

				print("""
		¡OH NO! Me han vuelto a dejar el coche atascado en el parking
		por favor ayudame a sacarlo. PD: El mio es el Ferrari rojo :-)
		(INTRO PARA CONTINUAR)""")
				input()
				nivel = 1	#Selecciona directamente el unico nivel posible (1)
			else:	#Ya ha jugado mas veces
				sys.stdout.flush()
				comando('clear')
				menu_niveles(records, nivel_max, niveles[0])
				nivel = pedir_nivel(nivel_max, dt, records)
				if nivel == 0:	#Corresponde al comando 'salir'
					#Se actualiza el tiempo jugado dentro de pedir_nivel() y aqui volvemos a mirar la hora por si sigue jugando
					dt = datetime.datetime.now()
					dt = datetime.timedelta(hours= dt.hour, minutes=dt.minute, seconds = dt.second)
				
			if nivel == 0:	#Corresponde al comando salir (valido para el primer juego o para cuando llevas mas tiempo jugando)
				guardar_records(records)
				bandera = False
			else:	#Se a seleccionado un nivel para jugar
			#Condicion tiene el mismo valor que devuelve jugar() si se ejecuta 'reset'
			#De esta manera dependiendo del valor de condicion podemos resetear el nivel
			#Si simplemente se pasan el nivel, condicion = None
				condicion = 1
				while condicion == 1:
					condicion = jugar(nivel, niveles, records, noc)
					#Si no ejecutan 'reset' ni 'salir' y no se ha pasado todos los niveles
					if condicion == None and nivel != niveles[0]:
						ask_for_next = input("¿Desea pasar al siguiente nivel? [S/N] ")
						if ask_for_next.lower() == 's':
							nivel += 1
							condicion = 1
		elif selector == 2:	#Ver el tiempo jugado
			imprimir_tiempo(records)
			bandera = False
		elif selector == 3:	#Cambiar color
			menu_color()
			noc = pedir_color()
			bandera = False

	sys.stdout.flush()
	comando('clear')
	menu()
	selector = pedir_selector()
	if selector == 0:
		seguir = False
