import os
import cv2
import json
from create_annotations import (
    create_image_annotation,
    create_annotation_from_yolo_format,
    coco_format,
)

classes = [
    "Football",
]
def proccesImagenes(img, id):
    img_file = cv2.imread(img)
    h, w, _ = img_file.shape
    file_path = img.split('/')[-1]
    image_id = id
    image_annotation = create_image_annotation(
            file_path=file_path, width=w, height=h, image_id=image_id
        )
    return image_annotation, h, w
    

def yoloToCoco(clase, x1, y1, x2, y2, annotation_id, image_id, h, w):
    # yolo format - (class_id, x_center, y_center, width, height)
    # coco format - (annotation_id, x_upper_left, y_upper_left, width, height)
      
    int_x_center = int(w * float(x1))
    int_y_center = int(h * float(y1))
    int_width = int(w * float(x2))
    int_height = int(h * float(y2))

    min_x = int_x_center - int_width / 2
    min_y = int_y_center - int_height / 2
    width = int_width
    height = int_height
    
    annotation = create_annotation_from_yolo_format(
                min_x,
                min_y,
                width,
                height,
                image_id,
                clase,
                annotation_id,
                segmentation=[],
                )
    return annotation
    

def get_images_info_and_annotations(path):
    # Imagenes que serán analizadas.
    ficheroTexto = [file for file in os.listdir(path) if (file.endswith('.txt'))]
    imagenes = [file for file in os.listdir(path) if (file.endswith('.jpg'))]
    image_id = 0
    annotation_id = 1
    for text in ficheroTexto:
        #print(text)
        imagenes = text[:-3] + 'jpg'
        imagenes = path + '/' + imagenes 
        image_annotation, h, w = proccesImagenes(imagenes, image_id)
        images_annotations.append(image_annotation)
        
        
        text = path + '/' + text
        f = open(text, "r")
        change = f.readlines()
        f.close()
        for line in change:
            if line != ' \n':
                clase = line.split()[0]
                x1 = line.split()[1]
                y1 = line.split()[2]
                x2 = line.split()[3]
                y2 = line.split()[4]
                annotation = yoloToCoco(clase, x1, y1, x2, y2, annotation_id, image_id, h, w)
                annotations.append(annotation)
                annotation_id += 1
        image_id += 1
    return images_annotations, annotations

def createJSON():
    if True:(
            coco_format["images"],
            coco_format["annotations"],
        ) = get_images_info_and_annotations(path)
    
    for index, label in enumerate(classes):
            categories = {
                "supercategory": "Defect",
                "id": index + 1,  # ID starts with '1' .
                "name": label,
            }
            coco_format["categories"].append(categories)
    
    output_path = directory + '/Cformat/train.json'
    with open(output_path, "w") as outfile:
        json.dump(coco_format, outfile, indent=4)
           
                
if __name__ == "__main__":
    # Obtener ruta de acceso.
    directory = os.getcwd()
    directory = directory.replace('\\', '/')
    path = directory + '/data/obj' 
    images_annotations = []
    annotations = []
    createJSON()
    
    
    
    
    
        