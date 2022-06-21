import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def IoU():
    modelo = 1 #0Haar , 1 YOLO
    trackName = "CSRT"

    D = pd.read_csv("Resultados/IoU/IoUYoloDetection.csv")
    #S = pd.read_csv("Resultados/IoU/IoU"+trackName+".csv")
    S = pd.read_csv("Resultados/IoU/IoUarregloBoosting.csv")
    bbox2 = [300, 180, 420, 300]

    Io = []
    for i in range(D.shape[0]):
        try:
            x1, y1, w1, h1 = D.x[i], D.y[i], D.w[i], D.h[i]
            x3, y3, w3, h3 = S.x[i], S.y[i], S.w[i], S.h[i]

            x2, y2 = x1 + w1, y1 + h1
            x4, y4 = x3 + w3, y3 + h3

            x_inter1 = max(x1, x3)
            y_inter1 = max(y1, y3)
            x_inter2 = min(x2, x4)
            y_inter2 = min(y2, y4)
            width_inter = max(0, x_inter2 - x_inter1)
            height_inter = max(0, y_inter2 - y_inter1)
            area_inter = width_inter * height_inter
            #print(area_inter)
            width_box1 = abs(x2 - x1)
            height_box1 = abs(y2 - y1)
            width_box2 = abs(x4 - x3)
            height_box2 = abs(y4 - y3)
            area_box1 = width_box1 * height_box1
            area_box2 = width_box2 * height_box2
            area_union = area_box1 + area_box2 - area_inter
            iou = area_inter / area_union
            if iou != 0:
                Io.append(iou)
        except:
            pass
    suma = 0
    for i in range(len(Io)):
        suma = suma + Io[i]
    #print(max(Io))
    #print(suma / len(Io))
    #f = open("Resultados/IoU/IoU.csv", "a")
    #Deteccion, Seguimiento, avg, max, min
    #f.write(str(modelo) + "," + trackName+"," + str(suma / len(Io))+","+ str(max(Io))+","+str(min(Io))+"\n")
    print(str(modelo) + "," + trackName+"," + str(suma / len(Io))+","+ str(max(Io))+","+str(min(Io))+"\n")
    #f.close()

    # return (suma / len(IoU))


def GraficoIoU():
    n_grupos = 7
    i_barras = np.arange(n_grupos)
    ancho_barras = 0.35
    plt.rcParams["figure.figsize"] = (12, 5)

    Haar, YOLO = [], []
    datos = pd.read_csv('Resultados/IoU/IoU.csv')
    for i in range(datos.shape[0]):
        if datos.Deteccion[i] == 0:
            Haar.append(datos.mini[i])
        else:
            YOLO.append(datos.mini[i])
    print(YOLO)
    print(Haar)
    plt.bar(i_barras, Haar, width=ancho_barras, label='Haar')
    plt.bar(i_barras + ancho_barras, YOLO, width=ancho_barras, label='Yolo')
    plt.legend(loc='best')
    ## Se colocan los indicadores en el eje x
    plt.xticks(i_barras + ancho_barras / 2, ('Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE'))

    for x, y in enumerate(Haar):
        plt.text(x, y, '%s' % round(y, 3), ha='center', fontsize=8)
    for z, w in enumerate(YOLO):
        plt.text(z + 0.35, w, '%s' % round(w, 3), ha='center', fontsize=8)

    plt.ylabel('Intersección Sobre la Unión (%)')
    plt.xlabel('Algoritmos')
    plt.title('IoU')
    #plt.savefig('Graficos/IoU.png')
    #plt.show()


if __name__ == '__main__':
    # trackName = ["Boosting", "MIL", "KCF", "TLD", "MEDIANFLOW", "CSRT", "MOSSE"]
    # for i in range(0,7):
    IoU()
    #GraficoIoU()
