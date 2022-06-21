# TFG Seguimiento del Dron de una pelota de Fútbol
Detección y seguimiento de un objeto mediante visión artificial desde un dron de bajo coste comercial

Para descargar imágenes provenientes de la base de datos de Google https://storage.googleapis.com/openimages/web/index.html hay que seguir el siguiente comando

python main.py downloader --classes <nombre_clases> --type_csv <tipo_csv> --limit <numero>

<classes_name> -> Poner el nombre de la clase que queremos descargar las imágenes en nuestro caso se usó Football
<tipo_csv> -> Pudiendo ser train o test
<number> -> Máximo número de fotos que se quiere descargar. Hay que pensar que a lo mejor no existe tal cantidad de fotos en ese caso se descargará el máximo número de fotos que haya.

Una vez descargado se procede a ejecutar el programa convert_annotations.py para normalizar las medidas de las bounding box de las imágenes.
