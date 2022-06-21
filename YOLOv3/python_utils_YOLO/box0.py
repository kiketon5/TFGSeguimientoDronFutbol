import os
import subprocess
import cv2
import numpy as np
import re

def ejecutarModeloPelota(img, salida):
    directory = os.getcwd()
    directory = directory.replace('\\', '/')   
    # Comando de ejecución.
    command = '/darknet.exe detector test data/obj.data cfg/yolov3-custom-train.cfg backup/yolov3-custom_last.weights -dont_show -ext_output ' + img + ' > ' + salida
    # command = '/darknet.exe detector test data/obj.data cfg/yolov3-custom-train.cfg backup/yolov3-custom_last.weights -ext_output ' + img + ' > ' + salida

    #subprocess.run(directory + command, capture_output = True, text = True)
    subprocess.run(directory + command, stdout = subprocess.PIPE, shell=True)



def obtenerBBox(img ,salida):
    # Abrir el fichero de salida.
    percentage, line = 0, 0
    with open(salida, 'r') as f:
        #info = f.readlines()[-1].replace(')', '')
        info = f.readlines()
        for i in info:
            info = re.split(": |\t|\n| |%", i)
            if info[0] == "Football" and int(info[1]) > percentage:
                percentage = int(info[1])
                line += 1
               
           # print(info)
        #print(percentage) 
        #print(line)
    with open(salida, 'r') as f:
        #info = f.readlines()[-1].replace(')', '')
        lines=f.readlines()
        line_to_read = (-1 - line)
        info = lines[line_to_read].replace(')', '')
    # Obtener la última línea que corresponde con la información.
    # Obtener información: left_x, top_y, width, height
    info = [int(word) for word in info.split() if word.isdigit()]
    print("INFO: ", info)
    return info

def YOLO(x1, y1, w, h, dw, dh):
    x1 = float((x1+w+x1)/2)/dh
    y1 = float((y1+h+y1)/2)/dw
    x2 = float(w/dh)
    y2 = float(h/dw)
    return x1, y1, x2, y2
    
def convert(x1, y1, w, h, dw, dh):
        #[98, 345, 322, 117, 640, 480]
        #[((420 + 98) / 2) / 640, ((462 + 345) / 2) / 480, 322 / 640, 117 / 480]
        #x1, y1, x2, y2 = YOLO(x1, y1, w, h, dw, dh)
        x1, y1, x2, y2 = x1, y1, w, h   
        return [x1, y1, x2, y2]

def guardarTxt(info, imagen, n):
    img = imagen[:-4]
    directory = "E:/pictures/Labels/pictures" + str(n) + '/' + img + ".txt"
    f = open(directory, "w")
    info = "0 " + str(info[0]-3) + " " + str(info[1]-3) + " " + str(info[2]+3) + " " + str(info[3]+3)
    f.write(info)
    f.close

if __name__ == "__main__":
    # Obtener ruta de acceso.
    n = 0
    pictures = 'pictures' + str(n)
    directory = 'E:/pictures/' + pictures
    # Imagenes que serán analizadas.
    contenido = [file for file in os.listdir(directory) if (file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.png') or file.endswith('.jpeg'))]

    # Salida de la identificación del vehículo.
    salida = 'salida' + str(n) + '.txt'
    resultado = ""
    con = 0
    initial_count = 0
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, path)): initial_count += 1
    
    for imagen in contenido:
        print(imagen)
        # Imagen a analizar.
        img = directory + '/' + imagen

        # Detectar matrícula del vehículo.
        ejecutarModeloPelota(img, salida)
        shape = cv2.imread(img)
        dw, dh, _ = shape.shape
        #print(shape.shape)
        # Obtener matrícula recortada.
        info = obtenerBBox(img, salida)
        if len(info) != 4:
            pass
        else:
            info = convert(info[0], info[1], info[2], info[3], dw, dh)
            #print(info)
            guardarTxt(info, imagen, n)
        print(initial_count - con)
        con += 1
        
        
# DA
# 0.371875, 0.4235, 0.27725, 0.36633333333333334
# Tiene que dar
# 0.495967 0.317654 0.369568 0.274768