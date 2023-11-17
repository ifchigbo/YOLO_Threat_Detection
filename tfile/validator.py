from ultralytics import YOLO
import cv2, os, cvzone, time
from math import ceil
from settings import ANALYZED_IMAGES_ASSET_PATH, NON_ANALYZED_IMAGES_ASSET_PATH, BEST_MODEL_PATH, IMAGES_GREATER_70_PATH, IMAGES_BETWEEN_PATHS
# from getClassName import getListofClassName

#class_name = getListofClassName()

cap = None

# class_name = ['1', 'handgun', 'knife', 'rifle']
# class_name = ['Handgun','Rifle','Shotgun']
class_name = ['weapon']


def getObjcetConvidenceScore():
    try:
        model = YOLO('yw/yolov8l.pt')
        result = model('images/HPW_LU_urban.jpeg', show=True)
        cv2.waitKey(0)
    except BaseException as error:
        print(error)

# Analysis of the individual images
def getStaticTest(img): # imgage frame
    current_time = time.time()
    try:
        # im = cv2.imread(img)
        im = img
        analyzed_saved_path = os.path.join(os.getcwd(), f'{ANALYZED_IMAGES_ASSET_PATH}')
        non_analyzed_saved_path = os.path.join(os.getcwd(), f'{NON_ANALYZED_IMAGES_ASSET_PATH}')

        if not os.path.exists(analyzed_saved_path):
            os.makedirs(analyzed_saved_path)

        if not os.path.exists(non_analyzed_saved_path):
            os.makedirs(non_analyzed_saved_path)

        images_greater_70 = os.path.join(os.getcwd(), f'{IMAGES_GREATER_70_PATH}')
        images_between_values = os.path.join(os.getcwd(), f'{IMAGES_BETWEEN_PATHS}')

        if not os.path.exists(images_greater_70):
            os.makedirs(images_greater_70)

        if not os.path.exists(images_between_values):
            os.makedirs(images_between_values)
        
        model = YOLO(f'{BEST_MODEL_PATH}')
        #result = model('images/ff350fa5ca28405d_jpg.rf.cedb5a31f5bd9383cb95fe35254099ae.jpg', show=True)
        results = model(im)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
                w,h = x2-x1, y2-y1
                cvzone.cornerRect(im,(x1,y1,w,h), rt=3,t=3, colorC=(10,232,123),colorR=(255,0,255))
                conf_level = ceil(box.conf[0]*100) / 100
                print(conf_level)
                obj_cls = int(box.cls[0])
                if obj_cls not in range(len(class_name)):
                    cvzone.putTextRect(im,"{} conf:{}".format(obj_cls, conf_level),(max(0,x1),max(45,y1)), scale=1.75)
                else:
                    cvzone.putTextRect(im, "{} conf:{}".format(class_name[obj_cls], conf_level), (max(0, x1), max(45, y1)),
                                           scale=1.75)
                # cv2.imshow("Image", im)
                if conf_level >= 0.7:
                    file_name = f"{analyzed_saved_path}{current_time}.jpg"
                    cv2.imwrite(file_name, im)
                if conf_level < 0.7:
                    file_name = f"{non_analyzed_saved_path}{current_time}.jpg"
                    cv2.imwrite(file_name, im)
                if conf_level >= .3 and conf_level < .7:
                    cv2.imwrite(f'{IMAGES_BETWEEN_PATHS}{conf_level}.jpg', im)
        # cv2.waitKey(1)
    except BaseException as error:
        print(error)

def getWebCamCap(): # Web cam capture
    try:
        # cap.set(3,1280)
        # cap.set(4,720)
        model = YOLO(f'{BEST_MODEL_PATH}')
        # model = YOLO('yw/yolov8l.pt')
        #model = YOLO('/Users/ichigbo/Documents/FINAL_PROJECT/weapons_logs/yolov8n16/weights/best.pt')
        cap = cv2.VideoCapture(0)
        #model = YOLO('yw/yolov8l.pt')
        while True:
            success, captured_img = cap.read()
            if not success:
                break
            result = model(captured_img, stream=True)
            for items in result:
                boxes = items.boxes
                for bgbox in boxes: # Loop Gets Boundary box for each object indetified in the frame
                    x1,y1,x2,y2 = bgbox.xyxy[0]
                    x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                    w,h = x2-x1, y2-y1
                    cvzone.cornerRect(captured_img,(x1,y1,w,h), rt=3,t=3, colorC=(10,232,123),colorR=(255,0,255))

                    conf_level = ceil(bgbox.conf[0]*100)/ 100 # Get Convidence  Level of the Model Prediction of the Object Detected
                    print(conf_level)
                    obj_cls = int(bgbox.cls[0]) # Get the index of an object from the list defined in Object_list
                    if obj_cls not in range(len(class_name)):
                        cvzone.putTextRect(captured_img,"{} conf{}".format(obj_cls,conf_level),(max(0,x1),max(45,y1)), scale=1.75)
                    else:
                        cvzone.putTextRect(captured_img, "{} conf{}".format(class_name[obj_cls], conf_level), (max(0, x1), max(45, y1)),
                                           scale=1.75)

                    #get Class name
            ret, jpeg = cv2.imencode('.jpg', captured_img)
            cap_img_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cap_img_bytes + b'\r\n')
            # cv2.imshow("Image",captured_img)
            # cv2.waitKey(1)
    except BaseException as error:
        print(error)

def closeWebcam():
    pass

# 'assets/images/hello.jpg'
# getWebCamCap()
# getStaticTest('assets/images/hello.jpg')

def getStaticTestForFiles(img): # imgage frame
    current_time = time.time()
    try:
        im = cv2.imread(img)
        analyzed_saved_path = os.path.join(os.getcwd(), f'{ANALYZED_IMAGES_ASSET_PATH}')
        non_analyzed_saved_path = os.path.join(os.getcwd(), f'{NON_ANALYZED_IMAGES_ASSET_PATH}')

        if not os.path.exists(analyzed_saved_path):
            os.makedirs(analyzed_saved_path)

        if not os.path.exists(non_analyzed_saved_path):
            os.makedirs(non_analyzed_saved_path)

        images_greater_70 = os.path.join(os.getcwd(), f'{IMAGES_GREATER_70_PATH}')
        images_between_values = os.path.join(os.getcwd(), f'{IMAGES_BETWEEN_PATHS}')

        if not os.path.exists(images_greater_70):
            os.makedirs(images_greater_70)

        if not os.path.exists(images_between_values):
            os.makedirs(images_between_values)
        
        model = YOLO(f'{BEST_MODEL_PATH}')
        #result = model('images/ff350fa5ca28405d_jpg.rf.cedb5a31f5bd9383cb95fe35254099ae.jpg', show=True)
        results = model(im)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
                w,h = x2-x1, y2-y1
                cvzone.cornerRect(im,(x1,y1,w,h), rt=3,t=3, colorC=(10,232,123),colorR=(255,0,255))
                conf_level = ceil(box.conf[0]*100) / 100
                print(conf_level)
                obj_cls = int(box.cls[0])
                if obj_cls not in range(len(class_name)):
                    cvzone.putTextRect(im,"{} conf:{}".format(obj_cls, conf_level),(max(0,x1),max(45,y1)), scale=1.75)
                else:
                    cvzone.putTextRect(im, "{} conf:{}".format(class_name[obj_cls], conf_level), (max(0, x1), max(45, y1)),
                                           scale=1.75)
                # cv2.imshow("Image", im)
                if conf_level >= 0.7:
                    file_name = f"{analyzed_saved_path}{current_time}.jpg"
                    cv2.imwrite(file_name, im)
                if conf_level < 0.7:
                    file_name = f"{non_analyzed_saved_path}{current_time}.jpg"
                    cv2.imwrite(file_name, im)
                if conf_level >= .3 and conf_level < .7:
                    cv2.imwrite(f'{IMAGES_BETWEEN_PATHS}{conf_level}.jpg', im)
        # cv2.waitKey(1)
    except BaseException as error:
        print(error)