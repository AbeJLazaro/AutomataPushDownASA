from leergramatica import informacion

# ***************************************************************

# cerradura *****************************************************
def combinar(beta,a):
  aux=[]
  if len(beta)==0:
    return a
  else:
    for j in a:
      betap=""
      for i in beta:
        betap+=i
      aux.append(betap+j)
    return aux
def first(x):
  aux = []
  for i in x:
    aux.extend(First[i[0]])
  return aux

def cerradura(I):
  J = I.copy()
  K = []

  for ep in J:
    K.append([ep[0]]+ep[1]+ep[2]+[ep[3]])

  for ep in J:
    #print("ep:",ep)
    if ep[1]!=[""] and len(ep[1])>ep[-1]:
      B = ep[1][ep[-1]]
      beta =  ep[1][ep[-1]+1:]
      a = ep[2]
      #print("B:",B)
      #print("beta:",beta)
      #print("a:",a)
      if B in N:
        for prod in gramatica[B]:
          #print(prod)
          comb = combinar(beta,a)
          #print("comb:",comb)
          primeros = first(comb)
          #print("primeros:",primeros)
          for terminal in primeros:
            #print("terminal:",terminal)
            #print([B]+prod+[terminal[0]]+[0])
            if [B]+prod+[terminal[0]]+[0] not in K:
              #print("Se agrega",[B,prod,First[terminal[0]],0])
              J.append([B,prod,First[terminal[0]],0])
              K.append([B]+prod+[terminal[0]]+[0])


  #imprimirRenglones(J)
  return J

# goto **********************************************************

def goto(I,X):
  J = []
  for ep in I:
    if len(ep[1])>ep[-1]:
      #print(ep[1][ep[-1]]==X)
      if ep[1][ep[-1]]==X:
        epp = ep.copy()
        epp[-1]+=1
        J.append(epp)
  return cerradura(J)

# funciones para imprimir ***************************************
def imprimirRenglones(x):
  for i in x:
    print(i)

def imprimir(x):
  # función para imprimir los estados mejorados
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
  lista = []
  for i in range(len(X)):
    aux=X[i].copy()
    ele=[aux[0],aux[1].copy(),aux[2].copy(),aux[3]]
    if len(lista)==0:
      lista.append(ele.copy())
    else:
      bandera = False
      for j in range(len(lista)):
        elep = lista[j].copy()
        if ele[0]==elep[0] and ele[1]==elep[1] and ele[3]==elep[3]:
          for o in ele[2]:
            if o not in elep[2]:
              elep[2].append(o)
          lista[j]=elep
          bandera = True
      if not bandera:
        lista.append(ele)
  imprimir(lista)

N = None
M = None
gramatica = None
inicial = None
First = None

def CalcularAutomata(nombre):
  global N,M,gramatica,inicial,First
  # pruebas *******************************************************
  datos = informacion(nombre)

  # definición de la gramática **********************************
  M=datos["M"]
  N=datos["N"]

  gramatica=datos["Gramatica"]

  inicial = datos["Inicial"]
  First = datos["First"]

  # [[cabecera,[producción],[prelectura],[indice del punto],...]
  # I0
  I0 =  [
          [inicial,gramatica[inicial][0],["$"],0]
        ]

  estados = []
  estados.append(cerradura(I0))
  i = 0
  j = 0
  print("Cerradura({"+inicial+"→"+gramatica[inicial][0][0]+",$})=")
  imprimirEstado(estados[0].copy())
  print("}=I0")
  print("")
  tablita = []
  while j<len(estados):
    I = estados[j]
    for x in N+M:
      aux = goto(I,x)
      #print("goto(I"+str(j)+","+x+")=",aux)
      if aux != None and aux != []:
        print("goto(I"+str(estados.index(I))+","+x+")=",end="")
        imprimirEstado(aux.copy())
        if aux in estados:
          print("=I"+str(estados.index(aux)))
          tablita.append(["I"+str(estados.index(I)),x,"I"+str(estados.index(aux))])
        else:
          estados.append(aux)
          i+=1
          print("=I"+str(i))
          tablita.append(["I"+str(estados.index(I)),x,"I"+str(i)])
        print("")

    j+=1
  return tablita,estados
if __name__ == '__main__':
  tablita,estados=CalcularAutomata("ejemplo2.txt")
  for linea in tablita:
    print(linea)
  print(estados[1])