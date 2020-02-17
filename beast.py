# coding: utf-8
import boto3
session = boto3.Session(profile_name='alexcloud2018')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='alexsvideos')
# didn't need to specify a location constraint, but if you did, it would be formatted this way.
bucket = s3.create_bucket(Bucket='alexsvideos', LocationConstraint=session.region_name)
bucket = s3.create_bucket(Bucket='alexsvideos', CreateBucketConfiguration={'LocationConstraint': session.region_name})

from pathlib import Path
# find movie file just downloaded. I actually just used system commands to get this from downloads
get_ipython().run_line_magic('ls', '*.MOV')
# had to convert .MOV to mp4 using vlc
pathname = 'zercher_squat.m4v'
path = Path(pathname).expanduser().resolve()
print(path)
# uploads video file using path
bucket.upload_file(str(path), str(path.name))
# set client to make api calls to rekognition service endpoint
rekognition_client = session.client('rekognition')
# begin processing video using rekognition
response = rekognition_client.start_label_detection(Video={'S3Object': { 'Bucket': bucket.name, 'Name': path.name}})
# response gives of the call is as follows below.
response
```
{'JobId': '1f926e60b8c23515f97540afca0f37992e93ed5508de5799eb0aa41f26e0a5a2',
 'ResponseMetadata': {'RequestId': '85e2745e-342f-4f07-b9a6-7cba07a0a696',
  'HTTPStatusCode': 200,
  'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1',
   'date': 'Sun, 27 Oct 2019 13:52:35 GMT',
   'x-amzn-requestid': '85e2745e-342f-4f07-b9a6-7cba07a0a696',
   'content-length': '76',
   'connection': 'keep-alive'},
  'RetryAttempts': 0}}
```
# parse job id to make result call
job_id = response['JobId']
result = rekognition_client.get_label_detection(JobId=job_id)
result
# result gives the reponse as follows below
```
{'JobStatus': 'IN_PROGRESS',
 'Labels': [],
 'LabelModelVersion': '2.0',
 'ResponseMetadata': {'RequestId': '3c6d1f0d-dcee-42e1-acb6-d6d7934d3998',
  'HTTPStatusCode': 200,
  'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1',
   'date': 'Sun, 27 Oct 2019 13:53:07 GMT',
   'x-amzn-requestid': '3c6d1f0d-dcee-42e1-acb6-d6d7934d3998',
   'content-length': '65',
   'connection': 'keep-alive'},
  'RetryAttempts': 0}}
```
# keys for result that you can get values for
result.keys()
```
dict_keys(['JobStatus', 'Labels', 'LabelModelVersion', 'ResponseMetadata'])
```
# current job status which can be one of 3 'IN_PROGRESS'|'SUCCEEDED'|'FAILED'
result['JobStatus']
# metadata for call made
result['ResponseMetadata']
```
{'RequestId': '3c6d1f0d-dcee-42e1-acb6-d6d7934d3998',
 'HTTPStatusCode': 200,
 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1',
  'date': 'Sun, 27 Oct 2019 13:53:07 GMT',
  'x-amzn-requestid': '3c6d1f0d-dcee-42e1-acb6-d6d7934d3998',
  'content-length': '65',
  'connection': 'keep-alive'},
 'RetryAttempts': 0}
```
# metadata for video
result['VideoMetadata']
```
{'Codec': 'h264',
 'DurationMillis': 147797,
 'Format': 'QuickTime / MOV',
 'FrameRate': 29.97360610961914,
 'FrameHeight': 1080,
 'FrameWidth': 1920}
```
# my video had 1000 labels so I had to pick one to show output
len(result['Labels'])
# one example label output.
result['Labels']
```
 {'Timestamp': 67860, # time in the video this label was found
  'Label': {'Name': 'Gym', # what rekognition intelligently labeled it as
   'Confidence': 59.93450927734375, # level of confidence rekognition has in accuracy of the label
   'Instances': [],
   'Parents': [{'Name': 'Sport'},
    {'Name': 'Person'},
    {'Name': 'Working Out'},
    {'Name': 'Fitness'}]}},
```
# note to self - ipython easily with '%save name_file.py 1-15' and specifiy lines
