import cv2
import os
import re
import shutil
import pathlib


def moverContenido(path, n):
        source_txt = path[n][1] + text
        source_img = path[n][0] + text[:-3] + 'jpg'
        if pathlib.Path(directory + '/positive/' + text).exists():
            destination_txt = directory + '/positive/' + text[:-4] + '1.txt'
        else:
            destination_txt = directory + '/positive/' + text[:-3] + 'txt'
            
        if pathlib.Path(directory + '/positive/' + text[:-3] + 'jpg').exists():
            destination_img = directory + '/positive/' + text[:-4] + '1.jpg'
        else:
            destination_img = directory + '/positive/' + text[:-3] + 'jpg'
        
        shutil.move(source_txt,destination_txt)
        shutil.move(source_img,destination_img)
    

def verBBox(path, text, n):
    f = open(path + text)
    file = f.readlines()
    for i in file:
            file = re.split(" ", i)
    #print(file)
    f.close()
    path_img = 'E:/pictures/FinalModelo/bienLabeled/Imagen/' + text[:-3] + "jpg"
    print(path_img)
    img = cv2.imread(path_img)
    x,y = int(file[1]), int(file[2])
    x2, y2 = (int(file[1])+int(file[3])), (int(file[2])+int(file[4]))
    cv2.rectangle(img, (x,y), (x2,y2), (0,0,255), 2)
    img = cv2.resize(img, (720,480), interpolation = cv2.INTER_AREA)
    cv2.imshow('img', img)
    cv2.waitKey(10)
    opt = input('a la imagen está bien, s la imagen mal etiquetada\n')
    return opt

if __name__ == "__main__":

    # directory = 'E:/PICTURESTFG'

    # ext_img = 'E:/PICTURESTFG/Images'
    # ext_txt = 'E:/PICTURESTFG/Labels'
    # path =[[ext_img + '/fotos/', ext_txt + '/text/'], [ext_img + '/NEW_FRAMES/', ext_txt + '/labels/']
    #        , [ext_img + '/pictures1/', ext_txt + '/pictures1/'], [ext_img + '/pictures/', ext_txt + '/xtexter/']]
    #path[0] revisado completamente
    #path[1] revisado completamente
    
    directory = 'E:/pictures/FinalModelo/bienLabeled/'
    
    n = 2
    #contenido = [file for file in os.listdir(path[n][1]) if (file.endswith('.txt'))]
    contenido = [file for file in os.listdir(directory + 'LYolo') if (file.endswith('.txt'))]
    path = directory + 'LYolo/'
    for text in contenido: 
        letter = verBBox(path, text, n)
        if letter == 'a': #moverContenido(path, n)
            print("A")
        else: continue
    
        

    #img = cv2.imread('prueba/frame100.jpg')
    #cv2.rectangle(img, (173-3,259-3), (184+3, 267+5), (255,0,0),1)
    #cv2.circle(img, (170, 255), 2, (255,0,0), 1)
    #cv2.circle(img, (184, 259), 2, (255,0,0), 2)
    #cv2.imshow('img', img)
    #image, center_coordinates, radius, color, thickness

    #cv2.waitKey(0)