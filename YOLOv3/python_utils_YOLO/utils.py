import shutil
import os


def copiarArchivos(text):  
    origen = directory + '/fotos/' + text[:-3] + "jpg"
    destino = directory + "/data/obj/" + text[:-3] + "jpg"
    # print(origen)
    # print(destino)
    try:
        shutil.copy(origen, destino)
    except:
        print(text)

def renombrarMayus(text):
    archivo = directory + "/fotos/" + text
    nuevo = archivo[:-3] + 'jpg'
    print(archivo)
    print(nuevo)
    os.rename(archivo, nuevo)

def borrarArchivos(text, ficheroTexto):
    img = text[:-3] + 'jpg'
    print("a")
    if text not in ficheroTexto:
        path = directory + '/fotos/' + img
        #print(path) 
        os.remove(path)
    else:
        copiarArchivos(text)

def eliminarHechos(text):
    img = text[:-3] + 'jpg'
    path = directory + '/fotos/' + img
    os.remove(path)
        


if __name__ == "__main__":

    directory = os.getcwd()
    directory = directory.replace('\\', '/')
    ficheroTexto = [file for file in os.listdir(directory + '/data/obj') if (file.endswith('.txt'))]
    ficheroImg = [file for file in os.listdir(directory + '/fotos') if (file.endswith('.JPG'))]
    
    # 
    for text in ficheroTexto:
        #copiarArchivos(text)
        #renombrarMayus(text)
        #eliminarHechos(text)
        borrarArchivos(text, ficheroTexto)
        
    
    # Borrar archivos con range ya está de 0-300 
    #for text in range(0,700):   
        #txt = str(text) + '.txt'
        #borrarArchivos(txt, ficheroTexto)
