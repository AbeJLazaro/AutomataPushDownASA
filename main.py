from tabla import tablaLR1
from revisionCadena import revisar
nombre = input("Ingresa el nombre del archivo de la gramatica ")
tabla,producciones = tablaLR1(nombre,archivo=True)
# opcional, descomentar para solo calcular las tablas
'''
cadenacomas = revisar(tabla,producciones)

name = "Sol"+nombre
archivo = open(name,"a")
archivo.write(cadenacomas)
archivo.close()'''
