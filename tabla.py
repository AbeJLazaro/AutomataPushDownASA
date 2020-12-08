'''
Autor:        Lázaro Martínez Abraham Josué
Titulo:       tabla.py
Versión:      1.0
Fecha:        6 de diciembre de 2020
'''
from autoLR1 import CalcularAutomata
from leergramatica import informacion,imprimirGramatica

def error(x,y,ant,nue):
  '''Función para indicar donde se encuentra un error'''
  print("Error en",x,y)
  print("valor anterior:",ant)
  print("siguiente valor:",nue)

def tablaLR1(nombre,archivo=False):
  '''implementación para la generación de la tabla LR1
  Parámetros
  nombre: nombre del archivo donde se encuentran las especificaciones de la gramática
  archivo: default False, indica si se creará un archivo tipo csv con la tabla generada'''

  # obtenemos los datos de la gramática con la función informacion()
  datos = informacion(nombre)
  imprimirGramatica(datos)
  # obtenemos la tabla de transiciones y los estados con CalcularAutomata()
  transiciones,estados=CalcularAutomata(nombre)

  # imprimimos cuantos estados existen
  print("estados:",len(estados))
  # imprimimos sus transiciones
  for linea in transiciones:
    print(linea)

  # inicializamos los datos en variables más comodas
  M=datos["M"]
  N=datos["N"]
  Producciones=datos["Producciones"]
  inicial=datos["Inicial"]

  # creamos las colmnas y las filas como diccionarios
  columnas = dict([(x,"error") for x in M+N])
  tabla = dict([(x,columnas.copy()) for x in range(len(estados))])

  # para i de 0 hasta el último estado
  for i in range(len(estados)):
    # obtenemos el estado i
    estado = estados[i]
    # para cada transición
    for renglon in transiciones:
      # si es una transición que viene del estado i
      if renglon[0]=="I"+str(i):
        # si el simbolo gramatical que genera la transición es terminal
        if renglon[1] in M:
          # si el espacio no esta vacío, se arroja un error
          if tabla[i][renglon[1]]!="error":
            error(i,renglon[1],tabla[i][renglon[1]],"d"+renglon[2][1:])
          # si no, se agrega el desplazamiento en la casilla correpondiente
          else:
            tabla[i][renglon[1]]="d"+renglon[2][1:]
        # si el simbolo gramatical que genera la transición es no terminal
        elif renglon[1] in N:
          # si el espacio no esta vacío, se arroja un error
          if tabla[i][renglon[1]] != "error":
            error(i,renglon[1],tabla[i][renglon[1]],renglon[2][1:])
          # si no, se agrega el desplazamiento en la casilla correpondiente
          else:
            tabla[i][renglon[1]]=renglon[2][1:]
    # para cada elemento punteado en el estado
    for j in estado:
      # filtramos las producciones vacias para dejarlas como una lista
      # vacía, ya que se modelan como [""]
      jp = list(filter(lambda x: len(x)>0,j[1]))
      # si el punto se encuentra al final de la producción
      if len(jp)==j[3]:
        # si el simbolo de transición es $ y la cabecera es el simbolo inicial
        if j[2]=="$" and j[0]==inicial:
          # agregamos el valor de Aceptar en la casilla correspondiente siempre
          # y cuando, no se encuentre ya agregado
          if tabla[i]["$"]!="error":
            error(i,"$",tabla[i]["$"],"Acep")
          else:
            tabla[i]["$"]="Acep"
        # si no
        else:
          # obtenemos una lista con la cabecera y la producción
          aux = [j[0],j[1]]
          # obtenemos el indice de dicha producción
          indice = Producciones.index(aux)
          # si está vacía la casilla, se agrega el operador reducir
          if tabla[i][j[2]] != "error":
            error(i,j[2],tabla[i][j[2]],"r"+str(indice))
          else:
            tabla[i][j[2]]="r"+str(indice)

  # impresión de la tabla
  cabecera = ""
  for i in ["edo"]+M+N:
    cabecera+="|{0:^8}".format(i)
  cabecera +="|\n"

  imprimible = cabecera

  for llave,valor in tabla.items():
    imprimible+="|{0:^8}".format(llave)
    for llave2,valor2 in valor.items():
      imprimible+="|{0:^8}".format(valor2)
    imprimible +="|\n"

  print(imprimible)

  # generación del archivo de la tabla
  if archivo:
    cabecera = ""
    for i in ["edo"]+M+N:
      cabecera+="{0},".format(i)
    cabecera +="\n"

    imprimible = cabecera

    for llave,valor in tabla.items():
      imprimible+="{0}".format(llave)
      for llave2,valor2 in valor.items():
        imprimible+=",{0}".format(valor2)
      imprimible +=",\n"

    name = "Sol"+nombre
    archivo = open(name,"w")
    archivo.write(imprimible)
    archivo.close()

    return tabla,Producciones
if __name__ == '__main__':
  nombre = input("Ingresa el nombre del archivo de la gramatica")
  tablaLR1(nombre,archivo=True)