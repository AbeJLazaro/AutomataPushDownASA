from autoLR1 import CalcularAutomata
from leergramatica import informacion

def error(x,y,ant,nue):
  print("Error en",x,y)
  print("valor anterior:",ant)
  print("siguiente valor:",nue)

def tablaLR1(nombre,archivo=False):
  datos = informacion(nombre)
  tablita,estados=CalcularAutomata(nombre)

  print("estados:",len(estados))

  for linea in tablita:
    print(linea)

  M=datos["M"]
  N=datos["N"]
  Producciones=datos["Producciones"]
  inicial=datos["Inicial"]

  columnas = dict([(x,"error") for x in M+N])
  tabla = dict([(x,columnas.copy()) for x in range(len(estados))])
  for i in range(len(estados)):
    estado = estados[i]
    for renglon in tablita:
      if renglon[0]=="I"+str(i):
        # print(renglon)
        if renglon[1] in M:
          if tabla[i][renglon[1]]!="error":
            error(i,renglon[1],tabla[i][renglon[1]],"d"+renglon[2][1:])
          else:
            tabla[i][renglon[1]]="d"+renglon[2][1:]
        elif renglon[1] in N:
          if tabla[i][renglon[1]] != "error":
            error(i,renglon[1],tabla[i][renglon[1]],renglon[2][1:])
          else:
            tabla[i][renglon[1]]=renglon[2][1:]
    for j in estado:
      jp = list(filter(lambda x: len(x)>0,j[1]))
      if len(jp)==j[3]:
        if j[2][0]=="$" and j[0]==inicial:
          if tabla[i]["$"]!="error":
            error(i,"$",tabla[i]["$"],"Acep")
          else:
            tabla[i]["$"]="Acep"
        else:
          aux = [j[0],j[1]]
          indice = Producciones.index(aux)
          if tabla[i][j[2][0]] != "error":
            error(i,j[2][0],tabla[i][j[2][0]],"r"+str(indice))
          else:
            tabla[i][j[2][0]]="r"+str(indice)

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

if __name__ == '__main__':
  tablaLR1("d.txt",archivo=True)