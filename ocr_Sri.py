import easyocr
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
import re
import time
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

from day import *
from date import *
from hms import *
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
#------------------------------------------------------------
date = datetime.now()
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
current_date = time.strftime("%m-%d-%Y ")
current_year = time.strftime("%Y")
current_time = time.strftime(" %H:%M:%S")
#print('today is: ',current_day)
current_day= days[date.weekday()]
print('today is: ',current_date + current_day + current_time )
#-------------------------------------------------------------

#IMAGE_DIR = "images2"
#IMAGE_DIR = 'E:\\BINO\\Bino_image_workspace\\UK_dataset\\data2\\fstown3_frames_RESIZED'
IMAGE_DIR = r"C:\Users\srira\Desktop\ocr_images"
#IMAGE_DIR = 'E:\\BINO\\Bino_image_workspace\\ocr_workspace\\OCR_staticImages\\dataset_for_ocr\\UK_store\\resized_townsend'
IMAGE_PATHS = []
for file in os.listdir(IMAGE_DIR):
    if file.endswith(".jpg") or file.endswith(".png"):
        IMAGE_PATHS.append(os.path.join(IMAGE_DIR, file))

#------------------------------
reader = easyocr.Reader(['en'])
for image_path in IMAGE_PATHS:
    b = image_path.split('\\')
    img_name = b[-1]
    img = Image.open(image_path)
    area = (4, 14, 362, 60)
    img = img.crop(area)
    new_img = img.resize((480,90), Image.ANTIALIAS)
    quality_val = 90 ##you can vary it considering the tradeoff for quality vs performance
    new_img.save("resized.jpg", "JPEG", quality=quality_val)

    img = cv2.imread('resized.jpg')
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_gray = cv2.bitwise_not(gray_image)
    #result = reader.readtext(gray_image)
    result = reader.readtext(inverted_gray)
    #print(result)
    print('=='*8)
    res = []
    for i in range(len(result)):
        res.append(result[i][1])
    print('raw result: ',res)
    
    #print('res length is: ',len(res[0]))
    print('image Name: ',img_name)

    if len(res) != 0:
        final_day = get_day(res[0])
        final_date = get_date(res[0])
        final_hms = get_hms(res)
    print('final day is:: ', final_day)
    print('final date is::  ',final_date)
    print('final time is:: ',final_hms)

    try:
        if len(final_hms)>0 and len(final_day)>0 and len(final_date)>0:
            print('Final result: ',final_date+' '+final_day+' '+final_hms)
            print('**'*20)
        else:
            print('oops!  can not display result because format is not valid.')
    except:
        pass
