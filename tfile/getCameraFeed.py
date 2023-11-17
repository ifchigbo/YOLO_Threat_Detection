from ultralytics import YOLO
import cv2, os
import cvzone
from math import ceil
from settings import VIDEOS_DIRECTORY_PATH, BEST_MODEL_PATH, IMAGES_GREATER_70_PATH, IMAGES_BETWEEN_PATHS, ANALYZED_IMAGES_ASSET_PATH, NON_ANALYZED_IMAGES_ASSET_PATH
# from getClassName import getListofClassName

#className = getListofClassName()
#className = ['1', 'handgun', 'knife', 'rifle']
# className = ['Handgun','Rifle','Shotgun']

className = ['weapon']

count_greater_07 = 0

def getRecordedVideoFeed(video):
    try:
        #recorded_cap_feed = cv2.VideoCapture('videos/{}.mp4'.format('AK-47 Christmas'))
        recorded_cap_feed = cv2.VideoCapture('{}{}'.format(VIDEOS_DIRECTORY_PATH, video)) # this guy should work with the upload method on the UI
        #recorded_cap_feed = cv2.VideoCapture('videos/{}.mp4'.format('videoplayback'))
        #model = YOLO('yw/yolov8l.pt')
        #model = YOLO('/Users/ichigbo/Documents/FINAL_PROJECT/weapons_logs/yolov8n16/weights/best.pt') #Model without Variation
        model = YOLO(f'{BEST_MODEL_PATH}') #Model with variation
        # model = YOLO('/Users/ichigbo/Documents/FINAL_PROJECT/guns-dataset-2_logs/yolov8n/weights/best.pt') #Model with variation
        #model = YOLO('/Users/ichigbo/Documents/FINAL_PROJECT/guns-dataset-2_logs/yolov8l/weights/best.pt')  # Hanggun Model augmented #path to the trained model

        images_greater_70 = os.path.join(os.getcwd(), f'{IMAGES_GREATER_70_PATH}')
        images_between_values = os.path.join(os.getcwd(), f'{IMAGES_BETWEEN_PATHS}')

        if not os.path.exists(images_greater_70):
            os.makedirs(images_greater_70)

        if not os.path.exists(images_between_values):
            os.makedirs(images_between_values)

        analyzed_saved_path = os.path.join(os.getcwd(), f'{ANALYZED_IMAGES_ASSET_PATH}')
        non_analyzed_saved_path = os.path.join(os.getcwd(), f'{NON_ANALYZED_IMAGES_ASSET_PATH}')

        if not os.path.exists(analyzed_saved_path):
            os.makedirs(analyzed_saved_path)

        if not os.path.exists(non_analyzed_saved_path):
            os.makedirs(non_analyzed_saved_path)

        while True:
            success, captured_img = recorded_cap_feed.read()
            result = model(captured_img, stream=True)
            print("FPS: ", int(recorded_cap_feed.get(cv2.CAP_PROP_FPS)))
            for items in result:
                boxes = items.boxes
                for bgbox in boxes: # Loop Gets Boundary box for each object indetified in the frame

                    x1,y1,x2,y2 = bgbox.xyxy[0]
                    conf_level = ceil((bgbox.conf[0]*100))/ 100
                    if conf_level >= 0.7:
                        cv2.imwrite(f'{IMAGES_GREATER_70_PATH}{conf_level}.jpg', captured_img)

                    if conf_level >= .45 and conf_level < .7:
                        cv2.imwrite(f'{IMAGES_BETWEEN_PATHS}{conf_level}.jpg', captured_img)
                    x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                    w,h = x2-x1, y2-y1
                    cvzone.cornerRect(captured_img,(x1,y1,w,h), rt=3,t=3, colorC=(10,232,123),colorR=(255,0,255))

                    # conf_level = ceil((bgbox.conf[0]*100))/ 100 # Get Convidence  Level of the Model Prediction of the Object Detected
                    print(conf_level) # Prediction Confidence Interval
                    obj_cls = int(bgbox.cls[0])# Get the index of an object from the list defined in Object_list


                    
                    
                    # if conf_level >= .5:
                    #     cv2.imwrite(f'{ANALYZED_IMAGES_PATH}{conf_level}.jpg', captured_img)
                        # cv2.imwrite("/Users/ichigbo/Documents/FINAL_PROJECT/cf_folder/{}.jpg".format(conf_level), captured_img)

                    if obj_cls not in range(len(className)):
                        cvzone.putTextRect(captured_img,"{} conf{}".format(obj_cls,conf_level),(max(0,x1),max(45,y1)), scale=1.75)

                    else:
                        cvzone.putTextRect(captured_img, "{} conf{}".format(className[obj_cls], conf_level), (max(0, x1), max(45, y1)),
                                           scale=1.75)
                        print(className[obj_cls]) # Weapons Class

                    ret, jpeg = cv2.imencode('.jpg', captured_img)
                    cap_img_bytes = jpeg.tobytes()
                    yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + cap_img_bytes + b'\r\n')
            # cv2.imshow("Image",captured_img)
            # cv2.waitKey(1)
            # capture framess per second
            #print("I am  here : ",int(recorded_cap_feed.get(cv2.CAP_PROP_FPS)))
    except BaseException as error:
        print(error)

# getRecordedVideoFeed('AK-47 Christmas.mp4')