from utilsSeguimiento import *

if __name__ == '__main__':
    trackName = ['Boosting', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']

    modelo = 1  # 0 for haar, 1 for yolo
    track = 6
    # for modelo in range(1, 2):
    #      for track in range(0, 7):
    start1 = time.time() * 1000
    timer, caja, detecciones = detectarMasSeguimiento(modelo, track, trackName[track])
    end1 = time.time() * 1000
    timer.append(end1 - start1)
    writerPrueba(timer, modelo, trackName[track], caja, detecciones)
        #print(trackName[j] +" "+ str(TIM(0, trackName[j])))
