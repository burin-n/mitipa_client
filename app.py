import requests
import sys
import json
import cv2
import numpy as np
import os


def upload_video(clientId="john", location="john's place", video_location=''):
    if(video_location == ''): 
        print('no video_location')
        return
    try:
        print(clientId, location, video_location)
        file_format = video_location.split('.')[-1]
        #get presigned url
        request_signed_url = 'https://fq1x9629yl.execute-api.ap-northeast-1.amazonaws.com/default/mitipa-upload-s3?format={}'.format(file_format)
        # request_signed_url = 'https://fq1x9629yl.execute-api.ap-northeast-1.amazonaws.com/default/mitipa-upload-s3'
        res = requests.get(url = request_signed_url)
        res = res.json()

        uploadURL = res['uploadURL']
        fileName = res['fileName']

        #upload video to S3
        data = open(video_location, 'rb').read()
        res = requests.put(url=uploadURL, data=data)
        if(res.status_code == 200):
            print('success upload with fileName ' + fileName)
        else:
            print('upload error')
            return
        
        # append trigger to SQS
        request_trigger_sqs = 'https://fq1x9629yl.execute-api.ap-northeast-1.amazonaws.com/default/appendsqs'
        res = requests.put(url=request_trigger_sqs, data = json.dumps({ \
                "clientId" : clientId, \
                "location" : location, \
                "video" : fileName
            }))
        if(res.status_code == 200):
            print('success append trigger to SQS')
        else:
            print('trigger fail')
            print(res.text)
            return    

    except Exception as E:
        print (E)
        print('something went wrong')


def upload_image(clientId="john", location="john's place", image_location=""):
    if(image_location == ''): 
        print('no image_location')
        return
    try:
        file_format = image_location.split('.')[-1]
        #get presigned url
        request_signed_url = 'https://fq1x9629yl.execute-api.ap-northeast-1.amazonaws.com/default/mitipa-upload-s3?format={}'.format(file_format)
        res = requests.get(url = request_signed_url)
        res = res.json()

        uploadURL = res['uploadURL']
        fileName = res['fileName']

        #upload video to S3
        data = open(image_location, 'rb').read()
        res = requests.put(url=uploadURL, data=data)
        if(res.status_code == 200):
            print('success upload with fileName ' + fileName)
        else:
            print('upload error')
            return

        request_save_dynamo = 'https://fq1x9629yl.execute-api.ap-northeast-1.amazonaws.com/default/mitipa-upload-dynamo'
        res = requests.put(url=request_save_dynamo, data = json.dumps({ \
                "clientId" : clientId, \
                "location" : location, \
                "image" : fileName
            }))
        if(res.status_code == 200):
            print('success save to dynaomoDB')
        else:
            print('save fail')
            print(res.text)
            return    

    except Exception as E:
        print (E)
        print('something went wrong')


def getVideoFrame(video_location, image_name='cache.jpg'):
    cap = cv2.VideoCapture(video_location)
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        
        if frame is not None:
            cv2.imwrite(image_name, frame)
            break
        else:
            print('none')
    cap.release()
    return image_name



if __name__ == '__main__':
    if(len(sys.argv) == 1):
        pass
    else:
        image_name = os.path.join(os.getcwd(), getVideoFrame(video_location=sys.argv[1]))
        upload_image(image_location=image_name, clientId=sys.argv[2], location=sys.argv[3])
        upload_video(video_location=sys.argv[1], clientId=sys.argv[2], location=sys.argv[3])
