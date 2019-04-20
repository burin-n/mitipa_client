import requests
import sys


def upload_video(video_location):
    try:
        request_signed_url = 'https://fq1x9629yl.execute-api.ap-northeast-1.amazonaws.com/default/mitipa-upload-s3'
        res = requests.get(url = request_signed_url)
        res = res.json()

        uploadURL = res['uploadURL']
        fileName = res['fileName']

        data = open(video_location, 'rb').read()
        res = requests.put(url=uploadURL, data=data)
        if(res.status_code == 200):
            print('success upload with fileName ' + fileName)
    except:
        print('something went wrong')


if __name__ == '__main__':
    if(len(sys.argv) == 1):
        upload_video('/Users/burin/Desktop/john.mp4')
    else:
        upload_video(sys.argv[1])
