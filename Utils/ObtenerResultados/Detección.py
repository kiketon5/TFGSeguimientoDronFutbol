from utilsDetección import *

if __name__ == '__main__':

    #modelo = 0  # 0 for haar, 1 for yolo
     #for modelo in range(0,2):
    modelo = 2
    timer = detection(modelo)
    #print(modelo)
    writePrueba(timer, modelo)
    #accuracy()
