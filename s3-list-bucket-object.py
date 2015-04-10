#!/usr/bin/python
# -*- coding: utf-8 -*-

from boto.s3.connection import S3Connection

conn = S3Connection()
#print conn.get_all_buckets()
bucket_name = 'cic-tech-images'

target_bucket = conn.get_bucket(bucket_name)

for key in target_bucket.list():
	print key.name
#	print '%s    %s   %s' %(key.name, key.size, key.last_modified)

