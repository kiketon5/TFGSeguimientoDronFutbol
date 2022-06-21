import os
import numpy as np
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1

if __name__ == "__main__":
    # Obtener ruta de acceso.
    directory = os.getcwd()
    directory = directory.replace('\\', '/')

    # Imagenes que serán analizadas.
    contenido = [file for file in os.listdir(directory + '/labels') if (file.endswith('.txt'))]

    # Salida de la identificación del vehículo.
    con = 0
    for texto in contenido:
        directory = "labels/" + texto
        f = open(directory, "r")
        change = f.readlines()
        f.close()
        changeString = listToString(change)
        changeString = changeString.split(" ")
        for i in range(len(changeString)):
            if changeString[i] == 'Baloncesto':
                #print("HI")
                pass
            else:
                
                if float(changeString[i]) > 1:
                    changeString[i] = float(changeString[i]) - 1
                    changeString[i] = str(changeString[i])
                    #print(changeString[i])
        changeString = ' '.join(changeString)
        f = open(directory, "w")
        f.write(changeString)
        f.close() 
        
        