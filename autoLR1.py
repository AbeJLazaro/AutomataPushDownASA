'''
Autor:        Lázaro Martínez Abraham Josué
Titulo:       autoLR1.py
Versión:      1.0
Fecha:        6 de diciembre de 2020
'''
from leergramatica import informacion

# ***************************************************************

# cerradura *****************************************************
def combinar(beta,a):
  '''Función que permite generar las combinaciones de beta con los
  posibles diferentes a

  Parámetros
  beta: porción de la producción que petenece a beta
  a:    Simbolo de preorden, es una lista de ellos

  return lista con las concatenaciones de beta y las posibles a
  '''

  # si beta no existe, es la cadena vacía, regresamos a
  if len(beta)==0:
    return [a]
  # si no, 
  else:
    return beta+[a]

def calcularAnulables():
  '''Calcula que elementos son anulables'''

  global gramatica, N, Anulables

  Anulables = []
  An = []
  lon = -1
  while(len(An)!=lon):
    lon = len(An)
    for n in N:
      for produccion in gramatica[n]:
        if produccion == [""] and n not in An:
          An.append(n)
        else:
          noAn = len(list(filter(lambda x: x not in An,produccion)))
          if noAn == 0 and n not in An:
            An.append(n)
  Anulables = An.copy()

def first(x):
  '''Función para calcular el first de una cadena

  Parámetros
  x: lista que representa la concatenación de beta y a

  return lista con el conjunto first de las cadenas
  '''
  i = 0
  A = []
  while True:
    A.extend(First[x[i]])
    if x[i] in Anulables:
      i+=1
    else:
      break

  return list(filter(lambda x: x != "",A))

def cerradura(I):
  '''
  Función cerradura

  Parámetros
  I: Estado al cual se le aplica cerradura

  return estado, conjunto de elementos punteados
  '''

  # generamos un conjunto J y un conjunto K que nos servirá como bandera
  J = I.copy()
  K = []

  # para cada elemento punteado en J, agregamos una concatenación de listas
  # representativas para cada elemento punteado
  for ep in J:
    K.append([ep[0]]+ep[1]+[ep[2]]+[ep[3]])

  # para cada elemento punteado que se encuentra en J
  for ep in J:
    # si la producción es diferente a cadena vacía y el punto no se encuentra al
    # final de la producción
    if ep[1]!=[""] and len(ep[1])>ep[-1]:
      # calculamos B, beta y a
      B = ep[1][ep[-1]]
      beta =  ep[1][ep[-1]+1:]
      a = ep[2]
      # si B pertenece a los simbolos no terminales
      if B in N:
        # para cada producción de B
        for prod in gramatica[B]:
          # calculamos la concatenación de beta y a
          comb = combinar(beta,a)
          # calculamos el first de esa combinación
          primeros = first(comb)
          # para cada elemento terminal en el conjunto first de la concatenación
          for terminal in primeros:
            if [B]+prod+[terminal]+[0] not in K:
              J.append([B,prod,terminal,0])
              K.append([B]+prod+[terminal]+[0])
  return J

# goto **********************************************************

def goto(I,X):
  '''Implementación de la función goto
  Parámetros
  I: estado 
  X: simbolo gramatical

  return estado nuevo
  '''

  # conjunto de elementos punteados inicializado
  J = []
  # para cada elemento punteado en el estado I
  for ep in I:
    # si el punto no se encuentra al final de la producción
    # y el simbolo de la producción donde se encuentra el punto es igual a X
    if len(ep[1])>ep[-1] and ep[1][ep[-1]]==X:
      # hacemos una copia del elemento punteado, y aumentamos la posición del 
      # punto
      epp = ep.copy()
      epp[-1]+=1
      # lo agregamos a J
      J.append(epp)
  # regresamos la cerradura del conjunto J
  return cerradura(J)

# funciones para imprimir ***************************************
def imprimirRenglones(x):
  '''Función para debuggear'''
  for i in x:
    print(i)

def imprimir(x):
  '''función para imprimir los estados en menos líneas
  Parámetros
  x: conjunto mejorado de elementos punteados (lista)'''

  # llave que abre
  print("{")
  # para cada elemento punteado dentro de los estados
  for i in x:
    # imprimimos la cabecera y el simbolo de producción
    print(i[0]+"→",end="")
    # imprimimos los elementos del cuerpo de la producción
    for indice in range(len(i[1])):
      # Colocamos el punto en el lugar que indica el espacio del punto, i[3]
      if indice == i[-1]:
        print("●",end="")
      print(i[1][indice],end="")
    # si el indice que indica la posición del punto es igual al tamaño del cuerpo
    # de la producción, se imprime el punto al final, ya que esto indica que terminó
    if i[-1] == len(i[1]):
      print("●",end="")
    # imprimimos una coma para empezar a imprimir los caracteres de lectura
    # anticipada
    print(",",end="")
    # para cada caracter de lectura anticipada, lo imprimimos
    for indice in range(len(i[2])):
      print(i[2][indice],end="")
      # si no es el último, imprimimos una diagonal
      if indice != len(i[2])-1:
        print("/",end="")
    # imprimimos una coma para indicar el siguiente elemento punteado
    print(",")
  # llaves que cierran
  print("}",end="")

def imprimirEstado(X):
  '''Función auxiliar para impresión de estados

  Parámetros
  X: Estado, conjunto de elementos punteados (lista)
  '''
  # creamos una lista nueva
  lista = []

  # para i de 0 hasta la cantidad de elementos punteados en el estado -1
  for i in range(len(X)):
    # creamos una copia del elemento punteado i
    aux=X[i].copy()
    # creamos una copia de caaa lista que exista en el elemento punteado
    ele=[aux[0],aux[1].copy(),[aux[2]],aux[3]]

    # si la longitud de la lista es 0, agregamos el elemento punteado
    if len(lista)==0:
      lista.append(ele)
    # si no
    else:
      # iniciamos una bandera como False, esta bandera nos indicará si el elemento
      # punteado ya estaba dentro de la lista pero con a diferente
      bandera = False
      # para cada elemento punteado dentro de la lista
      for j in range(len(lista)):
        # creamos una copia del elemento de la lista
        elep = lista[j].copy()
        # si la cabecera, producción y posición del punto son iguales
        if ele[0]==elep[0] and ele[1]==elep[1] and ele[3]==elep[3]:
          # para cada elemento de a en el elemento a ingresar
          for o in ele[2]:
            # si el simbolo a no se encuentra dentro del elemento punteado ya
            # ingresado en la lista
            if o not in elep[2]:
              # agregamos dicho elemento punteado
              elep[2].append(o)
          # actualizamos el elemento punteado en la lista
          lista[j]=elep
          # cambia la badera a True
          bandera = True
      # si el elemento punteado no se encontraba dentro de la lista, se agrega
      if not bandera:
        lista.append(ele)
  # se pide imprimir el estado
  imprimir(lista)

# variables globales
N = None
M = None
gramatica = None
inicial = None
First = None
Anulables = None

def CalcularAutomata(nombre):
  '''Función principal para calcular el autómata push down
  Parámetros
  nombre: nombre del archivo donde se encuentran las especificaciones de la
          gramática

  return tabla de transiciones (lista) y lista de estados'''

  # se especifica que se utilizaran las variables globales
  global N,M,gramatica,inicial,First
  # Se importan los datos con la función informacion() de leergramatica.py
  datos = informacion(nombre)

  # definición de la gramática **********************************
  M=datos["M"]
  N=datos["N"]

  gramatica=datos["Gramatica"]

  inicial = datos["Inicial"]
  First = datos["First"]

  calcularAnulables()

  # [[cabecera,[producción],[prelectura],[indice del punto],...]
  # I0
  I0 =  [
          [inicial,gramatica[inicial][0],"$",0]
        ]

  # inicialización de los estados y primer cerradura de la producción inicial
  estados = []
  estados.append(cerradura(I0))
  # contadores en 0
  i = 0
  j = 0
  # impresión del primer estado
  print("Cerradura({"+inicial+"→"+gramatica[inicial][0][0]+",$})=")
  imprimirEstado(estados[0].copy())
  print("}=I0")
  print("")
  # generación de la tabla de transiciones
  tablita = []
  # mientras j sea menor a la cantidad de estados generados
  while j<len(estados):
    # tomamos el estado j
    I = estados[j]
    # para cada simbolo gramatical
    for x in N+M:
      # calculamos el goto de ese estado con cada simbolo
      aux = goto(I,x)
      # si nos arroja un estado 
      if aux != None and aux != []:
        # imprimimos la transición
        print("goto(I"+str(estados.index(I))+","+x+")=",end="")
        imprimirEstado(aux.copy())
        # si el estado obtenido ya se encuentra en la lista de estados
        if aux in estados:
          # hacemos referencia a que estado es
          print("=I"+str(estados.index(aux)))
          # agregamos la transición a la tabla de transiciones
          tablita.append(["I"+str(estados.index(I)),x,"I"+str(estados.index(aux))])
        # si no
        else:
          # agregamos el estado a la lista de estados, aumentamos el contador de i 
          # e indicamos este nuevo estado
          estados.append(aux)
          i+=1
          print("=I"+str(i))
          # agregamos la transición a la tabla de transiciones
          tablita.append(["I"+str(estados.index(I)),x,"I"+str(i)])
        print("")
    # aumentamos el contador de j para visitar el siguiente estado
    j+=1
  # terminando el ciclo, regresamos la tabla de transiciones y la lista de estados
  return tablita,estados
  
if __name__ == '__main__':
  tablita,estados=CalcularAutomata("j.txt")
  for linea in tablita:
    print(linea)
  #print(estados[1])