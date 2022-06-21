import os
import cv2


def operations(x1, y1, x2, y2, w, h):
    
    xmin = int(x2 * h)
    xmax = int((2*x1*h - xmin)/2)
    ymin = int(y2 * w)
    ymax = int((2*y1*w - ymin)/2)
    
    return [xmin,ymin,xmax,ymax]

def writeCSV(w,h,medidas,clase, img):
    directory = "CSV/test.csv"
    info = str(img) + ',' + str(w) + ',' + str(h) + ',Football,' + str(medidas[0]) + ',' + str(medidas[1]) + ',' + str(medidas[2]) + ',' + str(medidas[3]) + '\n'

    if not os.path.isfile(directory): 
        f = open(directory, "w")
        f.write("filename,width,height,class,xmin,ymin,xmax,ymax\n")
    else: f = open(directory, "a")
    f.write(info)
    f.close    

def fromYolotoCSV(path):
    ficheroTexto = [file for file in os.listdir(path) if (file.endswith('.txt'))]
    for text in ficheroTexto:
        img1 = text[:-3] + 'jpg'
        text = path + '/' + text
        f = open(text, "r")
        change = f.readlines()
        f.close()
        img = text[:-3] + 'jpg'
        imag = cv2.imread(img)
        w, h, _ = imag.shape
        for line in change:
            if line != ' \n':
                clase = line.split()[0]
                x1 = line.split()[1]
                y1 = line.split()[2]
                x2 = line.split()[3]
                y2 = line.split()[4]
                medidas = operations(float(x1), float(y1), float(x2), float(y2), w, h)
                writeCSV(w,h,medidas,clase, img1)


if __name__ == "__main__":
    # Obtener ruta de acceso.
    directory = os.getcwd()
    directory = directory.replace('\\', '/')
    path = directory + '/CSV/test'
    fromYolotoCSV(path)
