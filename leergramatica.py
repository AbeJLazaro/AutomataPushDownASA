def informacion(nombre):

  archivo = open(nombre,"r")
  datos = archivo.readlines()
  archivo.close()
  info={}
  for linea in datos:
    # si contiene a los no terminales
    if "No terminales:" in linea:
      N = linea.split(":")[1].strip().split(" ")
      info["N"]=N
    # si contiene a los terminales
    elif "Terminales:" in linea:
      M = linea.split(":")[1].strip().split(" ")
      info["M"]=M
      if "First" not in info:
        info["First"]={}
      for i in M:
        info["First"][i]=[i]
    # si contiene la palabra First, es la especificación de los first
    elif "First" in linea:
      primSep = linea.split(":")
      cabecera = primSep[0].strip().split(" ")[1]
      elem = primSep[1].strip().split(" ")
      elemp =[]
      for i in elem:
        if i == "eps":
          elemp.append("")
        else:
          elemp.append(i)
      if "First" not in info:
        info["First"]={}
      info["First"][cabecera]=elemp
    # si es una línea que está después de la línea que dice "Producciones"
    elif datos.index(linea)>datos.index("Producciones\n"):
      if "Gramatica" not in info:
        info["Gramatica"]={}
      if "Producciones" not in info:
        info["Producciones"]=[]
      separacion = linea.split("→")
      cabecera = separacion[0].strip()
      produccion = separacion[1].strip().split(" ")
      produccionp = []
      for i in produccion:
        if i == "eps":
          produccionp.append("")
        else:
          produccionp.append(i)
      produccion = produccionp
      if cabecera not in info["Gramatica"]:
        info["Gramatica"][cabecera]=[produccion]
      else:
        info["Gramatica"][cabecera].append(produccion)
      info["Producciones"].append([cabecera,produccion])
    elif "Inicial" in linea:
      sep = linea.split(":")[1].strip()
      info["Inicial"]=sep

  for key in info:
    print(key,info[key])
  print("*"*70)
  return info

if __name__ == '__main__':
  nombre = "a.txt"
  info=informacion(nombre)
  for key in info:
    print(key,info[key])
