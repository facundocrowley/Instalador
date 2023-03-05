# Se importa lo necesario para la conexion
import configparser
from errores import *
import pyodbc
from configparser import ConfigParser
import os

def leer_cfg():
    try: #Intentar abrir el archivo
        with open('Config.cfg', 'r') as archivo: #Lee el archivo de configuración
            for line in archivo:
                line=line.strip() #Ignora los valores en blanco
                if line.startswith(";"): #Si la linea comineza con ; la saltea
                    continue
                else:
                    opcion=line.split(" = ") #Separo los valores en la lista para indexarlos
                    if 'NombreServer' in opcion:
                        NombreServer = opcion[1]  # Si el config contiene el NombreServer lo guardo en la variable
                    if 'NombreBase' in opcion:
                        NombreBase = opcion[1]  # Si el config contiene el NombreBase lo guardo en la variable

                        return NombreServer,NombreBase
    except:
        Error = errores(1)



#Se crea la funcion para la conexion
def conexion():
    try:
        server,base=leer_cfg() #Trae los valores de la función en forma de lista y los guarda en las variables que corresponder
        #print(server,base)
    except:

        Error=errores(2)




    user='SHS'
    Pass=''
    #Try para la conexión
    try:
        conexion= pyodbc.connect('DRIVER={SQL server};SERVER='+server+';DATABASE='+base+';UID='+user+';PWD='+Pass)

       # print('Conexion exitosa')

        return  conexion.cursor()
    except:
        Error=errores(3)


def desconexion(conn):
    conexion=conn
    try:
        conexion.close()
        #print("Desconexion exitosa")
    except:
        Error=errores(4)
def actualizar_config(NombreServer,NombreBase):
    config=configparser.ConfigParser() #Se crea el objeto config con las funciones del configparser
    config.optionxform = str # Conservar capitalización de opciones y valores
    NombreServerNue=NombreServer
    NombreBaseNue=NombreBase
    ruta_config= 'Config.Cfg'

    try:    # Intentar leer el archivo
        config.read(ruta_config)
        #print("Funciono la lectura")
        try: # Intenta setear la info en memoria de lo que va a hacer posteriormente en el archivo
            config.set('SHS','NombreServer',NombreServerNue)  #SHS es la sección, después son Opcion y NuevoValor
            config.set('SHS', 'NombreBase', NombreBaseNue)  # SHS es la sección, después son Opcion y NuevoValor
            #print("Funciona el seteo")
            try:
                with open(ruta_config, 'w') as archivo_config:
                    config.write(archivo_config)
            except:
                print("Fallo al actualizar el archivo")
        except:
            print("Fallo el set de info")
    except:
        Error=errores(1)

