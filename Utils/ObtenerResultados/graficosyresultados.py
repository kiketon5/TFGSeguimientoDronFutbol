import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


#######################################DETECCION######################
def yolovshaarTIM(Haar, YOLO):
    y = [YOLO, Haar]
    x = ["YOLO", "HaarCascade"]

    plt.rcParams["figure.figsize"] = (12, 5)

    plt.bar(x, y)
    plt.xlabel('Algoritmos')
    plt.ylabel('Tiempo de Inferencia Medio (ms)')

    plt.title('Comparación TIM', fontdict={'fontsize': 14, 'fontweight': 'bold'})

    plt.savefig('Graficos/Deteccion/TIM.png')
    # plt.show()


def yolovshaarRAM(Haar, YOLO):
    y = [YOLO * 100, Haar * 100]
    x = ["YOLO", "HaarCascade"]

    plt.rcParams["figure.figsize"] = (12, 5)

    plt.bar(x, y)
    plt.xlabel('Algoritmos')
    plt.ylabel('Ratio de Acierto Medio (%)')

    plt.title('Comparación RAM', fontdict={'fontsize': 14, 'fontweight': 'bold'})

    plt.savefig('Graficos/Deteccion/RAM.png')
    # plt.show()


def yolovshaarAcc(Haar, YOLO):
    y = [YOLO * 100, Haar * 100]
    x = ["YOLO", "HaarCascade"]

    plt.rcParams["figure.figsize"] = (12, 5)

    plt.bar(x, y)
    plt.xlabel('Algoritmos')
    plt.ylabel('Precision del Clasificador (%)')

    plt.title('Comparación Precision', fontdict={'fontsize': 14, 'fontweight': 'bold'})

    plt.savefig('Graficos/Deteccion/Acc.png')
    # plt.show()


def TIMDeteccion():
    H = open("Resultados/DeteccionHaar.csv", "r")
    Y = open("Resultados/DeteccionYolo.csv", "r")
    R = open("Resultados/DeteccionSelectROI.csv", "r")
    timerH = H.readlines()
    timerY = Y.readlines()
    timerR = R.readlines()
    H.close()
    Y.close()
    R.close()
    sumTimerH, sumTimerY, sumTimerR = 0, 0, 0
    for i in range(len(timerH) - 1):
        sumTimerH = sumTimerH + float(timerH[i])
    for i in range(len(timerY) - 1):
        sumTimerY = sumTimerY + float(timerY[i])
    for i in range(len(timerR) - 1):
        sumTimerR = sumTimerR + float(timerR[i])

    TIMH = sumTimerH / float(timerH[-1])
    TIMY = sumTimerY / float(timerY[-1])
    TIMR = sumTimerR / float(timerR[-1])
    print("TIM Haar = " + str(TIMH))
    print("TIM Yolo = " + str(TIMY) + "\n")
    print("TIM ROI = " + str(TIMR) + "\n")
    return TIMH, TIMY


def RAMDeteccion():
    H = open("Resultados/DeteccionHaar.csv", "r")
    TPHaar = len([file for file in os.listdir("Fotos/Deteccion/Haar/TP") if (file.endswith('.jpg'))])
    Y = open("Resultados/DeteccionYolo.csv", "r")
    TPYolo = len([file for file in os.listdir("Fotos/Deteccion/YOLO/TP") if (file.endswith('.jpg'))])

    timerH = H.readlines()
    H.close()
    timerY = Y.readlines()
    Y.close()
    RAMH = TPHaar / float(timerH[-1])
    RAMY = TPYolo / float(timerY[-1])
    print("RAM Haar = " + str(RAMH))
    print("RAM Yolo = " + str(RAMY) + "\n")
    return RAMH, RAMY


def AccDeteccion():
    TP = len([file for file in os.listdir("Fotos/Deteccion/Haar/TP") if (file.endswith('.jpg'))])
    FP = len([file for file in os.listdir("Fotos/Deteccion/Haar/FP") if (file.endswith('.jpg'))])
    TN = len([file for file in os.listdir("Fotos/Deteccion/Haar/TN") if (file.endswith('.jpg'))])
    FN = len([file for file in os.listdir("Fotos/Deteccion/Haar/FN") if (file.endswith('.jpg'))])
    AccH = (TN + TP) / (TP + FP + TN + FN)
    print("Accuracy Haar = " + str(AccH))
    TP = len([file for file in os.listdir("Fotos/Deteccion/YOLO/TP") if (file.endswith('.jpg'))])
    FP = len([file for file in os.listdir("Fotos/Deteccion/YOLO/FP") if (file.endswith('.jpg'))])
    TN = len([file for file in os.listdir("Fotos/Deteccion/YOLO/TN") if (file.endswith('.jpg'))])
    FN = len([file for file in os.listdir("Fotos/Deteccion/YOLO/FN") if (file.endswith('.jpg'))])
    AccY = (TN + TP) / (TP + FP + TN + FN)
    print("Accuracy Yolo = " + str(AccY) + "\n")
    return AccH, AccY


def confusionMatrixDeteccion():
    TP = len([file for file in os.listdir("Fotos/Deteccion/Haar/TP") if (file.endswith('.jpg'))])
    FP = len([file for file in os.listdir("Fotos/Deteccion/Haar/FP") if (file.endswith('.jpg'))])
    TN = len([file for file in os.listdir("Fotos/Deteccion/Haar/TN") if (file.endswith('.jpg'))])
    FN = len([file for file in os.listdir("Fotos/Deteccion/Haar/FN") if (file.endswith('.jpg'))])
    print(" Haar            Positive        Negative")
    print(" Positive       " + str(TP) + "             " + str(FP))
    print(" Negative       " + str(FN) + "              " + str(TN) + "\n")
    TP = len([file for file in os.listdir("Fotos/Deteccion/YOLO/TP") if (file.endswith('.jpg'))])
    FP = len([file for file in os.listdir("Fotos/Deteccion/YOLO/FP") if (file.endswith('.jpg'))])
    TN = len([file for file in os.listdir("Fotos/Deteccion/YOLO/TN") if (file.endswith('.jpg'))])
    FN = len([file for file in os.listdir("Fotos/Deteccion/YOLO/FN") if (file.endswith('.jpg'))])
    print(" YOLO            Positive        Negative")
    print(" Positive       " + str(TP) + "             " + str(FP))
    print(" Negative       " + str(FN) + "              " + str(TN) + "\n")


############################# SEGUIMIENTO ###########################
def TIMSeguimiento(corregir):
    trackName = ['Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    if corregir == 0:
        modelo = ['Haar', 'Yolo']
    else:
        modelo = ['HaarCorrijiendoRoi', 'YoloCorrijiendoRoi']
    dir = ['SinCorregir', 'Corregir']
    TIMH, TIMY = [], []
    for i in range(0, 2):
        for j in range(0, 7):
            f = open("Resultados/" + dir[corregir] + "/" + modelo[i] + trackName[j] + ".csv", "r")
            fichero = f.readlines()
            f.close()
            sumTimer = 0
            for x in range(len(fichero) - 1):
                sumTimer = sumTimer + float(fichero[x])
            # model = [sumTimer, (sumTimer / float(fichero[-1]))]
            model = sumTimer / float(fichero[-1])
            if i == 0:
                TIMH.append(model)
            else:
                TIMY.append(model)

    # print("TIM = " + str(TIMH) + "\n")
    # print("TIM = " + str(TIMY) + "\n")

    return TIMH, TIMY


def GraficoTIMSeguimiento(Haar, YOLO, corregir):
    n_grupos = len(Haar)
    i_barras = np.arange(n_grupos)
    ancho_barras = 0.35
    plt.rcParams["figure.figsize"] = (12, 5)

    plt.bar(i_barras, Haar, width=ancho_barras, label='Haar')
    plt.bar(i_barras + ancho_barras, YOLO, width=ancho_barras, label='Yolo')
    plt.legend(loc='best')
    ## Se colocan los indicadores en el eje x
    plt.xticks(i_barras + ancho_barras / 2, ('Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE'))
    for x, y in enumerate(Haar):
        plt.text(x, y + 1, '%s' % round(y, 2), ha='center', fontsize=8)
    for z, w in enumerate(YOLO):
        plt.text(z + 0.35, w + 1, '%s' % round(w, 2), ha='center', fontsize=8)

    plt.ylabel('Tiempo de Inferencia Medio (ms)')
    plt.xlabel('Algoritmos')
    if corregir == 0:
        plt.title('TIM Sin Corregir ROI')
        plt.savefig('Graficos/Seguimiento/TIMSinCorregir.png')
    else:
        plt.title('TIM Corrigiendo ROI')
        plt.savefig('Graficos/Seguimiento/TIMCorrigiendo.png')
    # plt.show()


def RAMSeguimiento(corregir):
    trackName = ['Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    if corregir == 0:
        modelo = ['Haar', 'Yolo']
    else:
        modelo = ['HaarCorrijiendoRoi', 'YoloCorrijiendoRoi']
    dir = ['SinCorregir', 'Corregir']
    RAMH, RAMY = [], []
    for i in range(0, 2):
        for j in range(0, 7):
            f = open("Resultados/" + dir[corregir] + "/" + modelo[i] + trackName[j] + ".csv", "r")
            TP = len([file for file in os.listdir("Fotos/Seguimiento/" + modelo[i] + "/" + trackName[j] + "/TP") if
                      (file.endswith('.jpg'))])
            # f = open("Resultados/Corregir/" + modelo[i] + trackName[j] + ".csv", "r")
            fichero = f.readlines()
            f.close()
            model = TP / float(fichero[-1])
            if i == 0:
                RAMH.append(model)
            else:
                RAMY.append(model)
    print(RAMY)
    return RAMY, RAMH


def GraficoRAMSeguimiento(Haar, YOLO, corregir):
    n_grupos = len(Haar)
    i_barras = np.arange(n_grupos)
    ancho_barras = 0.35
    plt.rcParams["figure.figsize"] = (12, 5)

    plt.bar(i_barras, Haar, width=ancho_barras, label='Haar')
    plt.bar(i_barras + ancho_barras, YOLO, width=ancho_barras, label='Yolo')
    plt.legend(loc='best')
    ## Se colocan los indicadores en el eje x
    plt.xticks(i_barras + ancho_barras / 2, ('Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE'))
    for x, y in enumerate(Haar):
        plt.text(x, y + 0.009, '%s' % round(y, 3), ha='center', fontsize=8)
    for z, w in enumerate(YOLO):
        plt.text(z + 0.35, w + 0.009, '%s' % round(w, 3), ha='center', fontsize=8)

    plt.ylabel('Ratio de Acierto Medio (%)')
    plt.xlabel('Algoritmos')
    if corregir == 0:
        plt.title('RAM Sin Corregir ROI')
        plt.savefig('Graficos/Seguimiento/RAMSinCorregir.png')
    else:
        plt.title('RAM Corrigiendo ROI')
        plt.savefig('Graficos/Seguimiento/RAMCorrigiendo.png')
    # plt.show()


def AccSeguimiento(corregir):
    trackName = ['Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    if corregir == 0:
        modelo = ['Haar', 'Yolo']
    else:
        modelo = ['HaarCorrijiendoRoi', 'YoloCorrijiendoRoi']
    AccH, AccY = [], []
    for i in range(0, 2):
        for j in range(0, 7):
            TP = len([file for file in os.listdir("Fotos/Seguimiento/" + modelo[i] + "/" + trackName[j] + "/TP") if
                      (file.endswith('.jpg'))])
            FP = len([file for file in os.listdir("Fotos/Seguimiento/" + modelo[i] + "/" + trackName[j] + "/FP") if
                      (file.endswith('.jpg'))])
            TN = len([file for file in os.listdir("Fotos/Seguimiento/" + modelo[i] + "/" + trackName[j] + "/TN") if
                      (file.endswith('.jpg'))])
            FN = len([file for file in os.listdir("Fotos/Seguimiento/" + modelo[i] + "/" + trackName[j] + "/FN") if
                      (file.endswith('.jpg'))])
            if i == 0:
                if (TN + TP) == 0:
                    AccH.append(0)
                else:
                    AccH.append((TN + TP) / (TP + FP + TN + FN))
            else:
                if (TN + TP) == 0:
                    AccY.append(0)
                else:
                    AccY.append((TN + TP) / (TP + FP + TN + FN))
    print(AccY)
    return AccH, AccY


def GraficoAccSeguimiento(Haar, YOLO, corregir):
    n_grupos = len(Haar)
    i_barras = np.arange(n_grupos)
    print(i_barras)
    ancho_barras = 0.35
    plt.rcParams["figure.figsize"] = (12, 5)

    plt.bar(i_barras, Haar, width=ancho_barras, label='Haar', align="center")
    plt.bar(i_barras + ancho_barras, YOLO, width=ancho_barras, label='Yolo', align="center")
    plt.legend(loc='best')
    ## Se colocan los indicadores en el eje x
    plt.xticks(i_barras + ancho_barras / 2, ('Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE'))

    for x, y in enumerate(Haar):
        plt.text(x, y + 0.009, '%s' % round(y, 3), ha='center', fontsize=8)
    for z, w in enumerate(YOLO):
        plt.text(z + 0.35, w + 0.009, '%s' % round(w, 3), ha='center', fontsize=8)

    plt.ylabel('Precision del Clasificador (%)')
    plt.xlabel('Algoritmos')
    if corregir == 0:
        plt.title('Acc Sin Corregir ROI')
        plt.savefig('Graficos/Seguimiento/AccSinCorregir.png')
    else:
        plt.title('Acc Corrigiendo ROI')
        plt.savefig('Graficos/Seguimiento/AccCorrigiendo.png')
    # plt.show()


def IoU(detection, trackName):
    D = pd.read_csv("Resultados/IoU/IoU" + detection + "Detection.csv")
    S = pd.read_csv("Resultados/IoU/IoU" + trackName + ".csv")
    Io = []
    img = []
    suma = 0
    Detecction = [file for file in os.listdir("Fotos/Deteccion/" + detection + "/TP") if (file.endswith('.jpg'))]
    # print(Detecction)
    for i in range(len(Detecction)):
        name = Detecction[i]
        # print(name[:-4])
        img.append(int(name[:-4]))
    #print(img)
    for i in range(len(img)):
        x1, y1, w1, h1 = D.x[i], D.y[i], D.w[i], D.h[i]
        x3, y3, w3, h3 = S.x[i], S.y[i], S.w[i], S.h[i]
    #     suma = suma + x1
    # totalX = suma / D.shape[0]
    # print(totalX)
        x2, y2 = x1 + w1, y1 + h1
        x4, y4 = x3 + w3, y3 + h3

        x_inter1 = max(x1, x3)
        y_inter1 = max(y1, y3)
        x_inter2 = min(x2, x4)
        y_inter2 = min(y2, y4)
        width_inter = abs(x_inter2 - x_inter1)
        height_inter = abs(y_inter2 - y_inter1)
        area_inter = width_inter * height_inter

        width_box1 = abs(x2 - x1)
        height_box1 = abs(y2 - y1)
        width_box2 = abs(x4 - x3)
        height_box2 = abs(y4 - y3)
        area_box1 = width_box1 * height_box1
        area_box2 = width_box2 * height_box2
        area_union = area_box1 + area_box2 - area_inter
        iou = area_inter / area_union
        Io.append(iou)
    suma = 0
    for i in range(len(Io)):
        suma = suma + Io[i]
    print(max(Io))
    print(suma / len(Io))

    return (suma / len(Io))


def GraficoIoU():
    n_grupos = 7
    i_barras = np.arange(n_grupos)
    ancho_barras = 0.35
    plt.rcParams["figure.figsize"] = (12, 5)

    Haar, YOLO = [], []
    datos = pd.read_csv('Resultados/IoU/IoU1.csv')
    for i in range(datos.shape[0]):
        if datos.Deteccion[i] == 0:
            Haar.append(datos.IoU[i] * 100)
        else:
            YOLO.append(datos.IoU[i] * 100)
    print(YOLO)
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
    plt.savefig('Graficos/IoU.png')
    plt.show()


def timevserror():
    datos = pd.read_csv("Resultados/pErrorBueno.csv")
    x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = [], [], [], [], [], [], [], [], [], []
    for i in range(datos.shape[0]):
        if datos.P[i] == 0.1 and datos.I[i] == 0.5:
            x1.append(datos.TiempoTotal[i])
            y1.append(abs(datos.Error[i]))
        elif datos.P[i] == 0.5 and datos.I[i] == 0.9:
            x2.append(datos.TiempoTotal[i])
            y2.append(abs(datos.Error[i]))
        elif datos.P[i] == 0.05 and datos.I[i] == 0.1:
            x3.append(datos.TiempoTotal[i])
            y3.append(abs(datos.Error[i]))
        elif datos.P[i] == 0.8 and datos.I[i] == 0.1:
            x4.append(datos.TiempoTotal[i])
            y4.append(abs(datos.Error[i]))
        elif datos.P[i] == 0.05 and datos.I[i] == 0.05:
            x5.append(datos.TiempoTotal[i])
            y5.append(abs(datos.Error[i]))

    plt.rcParams["figure.figsize"] = (12, 5)
    plt.scatter(x1, y1, label='PI = 0.1, 0.5')
    plt.scatter(x2, y2, label='PI = 0.5, 0.9')
    plt.scatter(x3, y3, label='PI = 0.05, 0.1')
    plt.scatter(x4, y4, label='PI = 0.8, 0.1')
    plt.scatter(x5, y5, label='PI = 0.05, 0.05')

    plt.xlabel('Número de Nodos')
    plt.ylabel('Pasos de Ejecución')
    plt.title('Nodos vs Pasos - Ejercicio 1', fontdict={'fontsize': 14, 'fontweight': 'bold'})
    plt.legend()
    # plt.savefig('Graficos/NodosPasos1.png')
    plt.show()


def timepErrorvserror():
    datos = pd.read_csv("Resultados/pErrorBueno.csv")
    x, y = [], []
    for i in range(datos.shape[0]):
        y.append(datos.TimepError[i])
        x.append(datos.Error[i])

    plt.rcParams["figure.figsize"] = (12, 5)
    plt.scatter(x, y)

    plt.xlabel('Número de Nodos')
    plt.ylabel('Pasos de Ejecución')
    plt.title('Nodos vs Pasos - Ejercicio 1', fontdict={'fontsize': 14, 'fontweight': 'bold'})

    # plt.savefig('Graficos/NodosPasos1.png')
    plt.show()

def graficoTiempopErrorvsErrorXValidacion():
    datos = pd.read_csv("Resultados/Validacion.csv")

    x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = [], [], [], [], [], [], [], [], [], []
    x6, y6, x7, y7, x8, y8 = [], [], [], [], [], []
    a, b, c, d, e, f = 0, 0, 0, 0, 0, 0
    for i in range(datos.shape[0]):
        if (datos.P[i] == 0.5 and datos.D[i] == 0.5):
            x1.append(datos.TiempoTotal[i]*100)
            y1.append(abs(datos.ErrorX[i]))
        elif (datos.P[i] == 0.5 and datos.D[i] == 0.25):
            x2.append(datos.TiempoTotal[i]*100)
            y2.append(abs(datos.ErrorX[i]))
        elif (datos.P[i] == 0.25 and datos.D[i] == 0.25):
            x3.append(datos.TiempoTotal[i]*100)
            y3.append(abs(datos.ErrorX[i]))
            a += abs(datos.ErrorX[i])
            b += 1
        elif (datos.P[i] == 0.25 and datos.D[i] == 0.1):
            x4.append(datos.TiempoTotal[i]*100)
            y4.append(abs(datos.ErrorX[i]))
            c += abs(datos.ErrorX[i])
            d += 1
        elif (datos.P[i] == 0.1 and datos.D[i] == 0.1):
            x5.append(datos.TiempoTotal[i]*100)
            y5.append(abs(datos.ErrorX[i]))
            e += abs(datos.ErrorX[i])
            f += 1
        # elif (datos.P[i] == 0.1 and datos.D[i] == 0.05):
        #     x6.append(datos.TiempoTotal[i]*100)
        #     y6.append(abs(datos.ErrorX[i]))
        # elif (datos.P[i] == 0.05 and datos.D[i] == 0.05):
        #     x7.append(datos.TiempoTotal[i]*100)
        #     y7.append(abs(datos.ErrorX[i]))
    plt.rcParams["figure.figsize"] = (12, 5)
    #plt.plot(x1, y1, label='PD=0.5,0.5')
    #plt.plot(x2, y2, color="white", label='PD=0.5,0.25')
    #plt.plot(x2, y2, color="white")
    plt.plot(x3, y3, color="green", label='PD=0.25,0.25')
    plt.plot(x4, y4, color="red", label='PD=0.25,0.125')
    #plt.plot(x5, y5, color="purple", label='PD=0.125,0.125')
    # plt.plot(x6, y6, label='PD=0.1,0.05')
    # plt.plot(x7, y7, label='PD=0.05,0.05')
    plt.legend()
    plt.xlabel('Tiempo Total de Ejecución (segundos)')
    plt.ylabel('Error en el Eje X')
    plt.title('Error en el Tiempo', fontdict={'fontsize': 14, 'fontweight': 'bold'})
    plt.savefig("Graficos/PD0250125.png")
    print(a / b)
    print(c / d)
    print(e / f)
    plt.show()

if __name__ == '__main__':
    modelo = 0
    corregir = 1  # 0 sin corregir, 1 corrigiendo

    # tim = TIMDeteccion()
    #ram = RAMDeteccion()
    #acc = AccDeteccion()

    # confusionMatrixDeteccion()
    # yolovshaarTIM(tim[0], tim[1])
    #yolovshaarRAM(ram[0], ram[1])
    #yolovshaarAcc(acc[0], acc[1])
    # Haar1, Yolo1 = TIMSeguimiento(corregir)
    # GraficoTIMSeguimiento(Haar1, Yolo1, corregir)
    #Haar1, Yolo1 = RAMSeguimiento(corregir)
    #GraficoRAMSeguimiento( Haar1, Yolo1, corregir)
    #Haar1, Yolo1 = AccSeguimiento(corregir)
    #GraficoAccSeguimiento( Haar1, Yolo1, corregir)
    # print(Haar1)
    # print(Yolo1)
    #trackName = ['Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    #modelo = ['Haar', 'Yolo']
    #f = open("Resultados/IoU/IoU1.csv", "w")
    #f.write("Deteccion,Seguimiento,IoU" + "\n")
    #
    #for i in range(0, 2):
         #for j in range(0, 7):
             #iou = IoU(modelo[i], trackName[j])
             #f.write(str(i) + "," + trackName[j]+"," + str(iou)+"\n")
    #f.close()
    #GraficoIoU()
    # timevserror()
    # timepErrorvserror()
    graficoTiempopErrorvsErrorXValidacion()
