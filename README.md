# TFG Seguimiento del Dron de una pelota de Fútbol
Detección y seguimiento de un objeto mediante visión artificial desde un dron de bajo coste comercial

Para descargar imágenes provenientes de la base de datos de Google https://storage.googleapis.com/openimages/web/index.html hay que seguir el siguiente comando

python main.py downloader --classes <nombre_clases> --type_csv <tipo_csv> --limit <numero>

<classes_name> -> Poner el nombre de la clase que queremos descargar las imágenes en nuestro caso se usó Football
<tipo_csv> -> Pudiendo ser train o test
<number> -> Máximo número de fotos que se quiere descargar. Hay que pensar que a lo mejor no existe tal cantidad de fotos en ese caso se descargará el máximo número de fotos que haya.

Una vez descargado se procede a ejecutar el programa convert_annotations.py para normalizar las medidas de las bounding box de las imágenes.

Con respecto a YOLOv3

Para crear el modelo hay que usar el siguiente comando

darknet.exe detector train data/obj.data cfg/yolov3-custom.cfg darknet53.conv74

Si durante la ejecución el modelo se apaga o se corta se podría volver a empezar el proceso desde aqui por ejemplo iteracion 1000
darknet.exe detector train data/obj.data cfg/yolov3-custom.cfg yolov3_custom_1000.weights

Para probar si funciona
darknet.exe detector test data/obj.data cfg/yolov3-custom-train.cfg backup/yolov3-custom_last.weights <name_image> 

darknet.exe detector demo data/obj.data cfg/yolov3-custom-train.cfg backup/yolov3-custom_last.weights <pathvideo> -out_filename <outputsave.mp4>