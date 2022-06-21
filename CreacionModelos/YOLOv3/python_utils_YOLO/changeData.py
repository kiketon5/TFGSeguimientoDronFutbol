import os 

contenido = os.listdir('Yformat/')

for ficheros in contenido:
    #print(ficheros)
    ficheros = "Yformat/" + ficheros
    #ficheros = open(ficheros, "a")
    f = open(ficheros)
    text_final = f.read()
    
    text_final = text_final.split("\n")
    line = ""
    for e in text_final:
        try:
            e = float(e)
        except:
            e = e.split(" ")
        for i in e:
            if i == str(0):
                line += "1"
            else:
                line += str(i)
            line += " "
        line +="\n"
    #print(line)
    f.close()
    # f = open(ficheros)
    # text_final = f.read()[1:]
    # f.close()
    f = open(ficheros,"w")
    f.write(line)
    f.close()