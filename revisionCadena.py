
def revisar(tabla,producciones):
  cadena = input("Ingresa la cadena a revisar, cada \
  simbolo separado por un espacio\n").split(" ")
  cadena.append("$")
  pila = ["$","0"]
  cadena = list(filter(lambda x: x!="",cadena))

  plantilla = "|{0:^15}|{1:^15}|{2:^20}|"
  print(plantilla.format("Pila","Entrada","Acción"))
  comas = "{0},{1},{2},\n"
  cadenacomas = comas.format("Pila","Entrada","Acción")

  while True:
    accion = tabla[int(pila[-1])][cadena[0]]
    cadenap = cadena.copy()
    pilap = pila.copy()
    if accion[0]=="d":
      straccion = "desplazar "+accion[1:]
      pila.append(accion[1:])
      cadena.pop(0)
    elif accion[0]=="r":
      prod = producciones[int(accion[1:])]
      cuerpo = prod[1].copy()
      if cuerpo.count(""): cuerpo[cuerpo.index("")]="eps"
      straccion = "reducir "+prod[0]+"→"+"".join(cuerpo)
      if cuerpo.count("eps"): cuerpo.remove("eps")
      for i in cuerpo:
        pila.pop()
      pila.append(tabla[int(pila[-1])][prod[0]])
    elif accion=="Acep":
      print(plantilla.format("".join(pilap),"".join(cadenap),"Aceptar"))
      cadenacomas+=comas.format("".join(pilap),"".join(cadenap),straccion)
      return cadenacomas
    else:
      print("Error")
      return ""

    print(plantilla.format("".join(pilap),"".join(cadenap),straccion))
    cadenacomas+=comas.format("".join(pilap),"".join(cadenap),straccion)

