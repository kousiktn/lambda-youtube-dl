# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, glob
from urlparse import urlparse

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET

import boto3
import youtube_dl

bucket_name = settings.BUCKET_NAME
conn = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)

ydl = youtube_dl.YoutubeDL({'format':'mp4', 'outtmpl': '/tmp/%(title)s.%(ext)s'})

def uploadMP4ToS3():
	files = glob.glob(os.path.join('/tmp/', '*.mp4'))
	s3_paths = set()
	for filePath in files:
		fileName = filePath.split('/')[-1]
		curFile = open(filePath, 'r').read()
		conn.upload_file(filePath, bucket_name, fileName)
		os.remove(filePath)
		s3_paths.add('s3://{}/{}'.format(bucket_name, filePath))

	return s3_paths

@require_GET
def downloadYoutubeVideo(request):
	url = request.GET.get('url', '')
	parsed_uri = urlparse(url)
	domain = parsed_uri.netloc

	if 'youtube.com' not in domain:
		return HttpResponse('Invalid youtube URL', status=404)

	try:
		ydl.download([url])
	except Exception as e:
		return HttpResponse('Unable to download because:<br> {}'.format(e), status=500)

	try:
		s3_path = uploadMP4ToS3()
	except Exception as e:
		return HttpResponse('Unable to upload to S3 because:<br> {}'.format(e), status=500)

	return HttpResponse('Downloaded and saved to:<br> {}'.format(s3_path), status=200)
