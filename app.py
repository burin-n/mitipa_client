import boto3
import sys
import os

if(len(sys.argv) < 2):
	print('no file is provided')

client = boto3.client('s3')
client.upload_file(os.path.join(os.cwd(), sys.argv[1]))