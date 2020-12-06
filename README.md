# AutomataPushDownASA
Implementacióń para la generación de automatas push down para el análisis sintáctico ascendente 

Los archivos importantes son los archivos de Python
* autoLR1.py crea el autómata push down con las funciones de cerradura y goto
  - La función principal CalcularAutomata recibe como parámetro el nombre del archivo que contiene las especificaciones de la gramática, devuelve una tabla referente a las transiciones goto y los estados generados
* leergramatica.py es un archivo que contiene una función la cual lee un archivo de texto en el que se especifica la gramática y devuelve un diccionario con la información que los demas archivos necesitan. 
  - Los archivos que contienen la información de la gramática deben contener el siguiente aspecto
    + Se indica que simbolos son no terminales, cuales son terminales, que simbolo es el inicial, es necesario especificar como se muestra el conjunto First de los simbolos no terminales, y las producciones de la gramática deben especificarse después de la linea que dice Producciones
    + Todos los simbolos gramaticales deben estar separados entre espacios
    + la palabra eps representa la cadena vacía
    
    No terminales: S' S
    
    Terminales: ( ) $
    
    Inicial: S'
    
    First S': ( eps
    
    First S: ( eps
    
    Producciones
    
    S' → S
    
    S → S ( S )
    
    S → eps
    
* tabla.py cuenta con la función tablaLR1 la cual recibe el nombre del archivo que contiene a la gramática y un parámetro booleano para indicar si se creará un archivo tipo csv para exportar la tabla
    
