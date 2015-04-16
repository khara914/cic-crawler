#!/usr/bin/python
# -*- coding: utf-8 -*-

def dl_img():
	import boto.dynamodb2
	import urllib
	from boto.dynamodb2.layer1 import DynamoDBConnection
	from boto.dynamodb2.table import Table
	from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
	from boto.dynamodb2.types import NUMBER
	from boto.dynamodb2.items import Item
	from boto.s3.connection import S3Connection
	from boto.s3.key import Key

	def download_image(dl_url,f_name):
		dl_path = '/root/local_images/' + f_name
		urllib.urlretrieve(dl_url,dl_path)

	#conn = boto.dynamodb2.connect_to_region('ap-northeast-1')
	conn = boto.dynamodb2.connect_to_region('us-east-1')
	conn_s3 = S3Connection()

	table_name = 'cic-tech-info'
	bucket_name = 'cic-tech-images-us-east1'

	table = Table(table_name, connection=conn)


	flag = table.query_2(index='img_flag-index', img_flag__eq='0')
	counter = 0
	for c in flag:
		counter +=1
	print '{0} url found' .format(counter)

	flag = table.query_2(index='img_flag-index', img_flag__eq='0')
	for i in flag:
		try:
			f_name = i['rangekey'] + '.jpg'
			f_path = '/root/local_images/' + f_name
			s3_url = 'https://s3-ap-northeast-1.amazonaws.com/' + bucket_name + '/' +  f_name
			s3_url = 'https://s3.amazonaws.com/' + bucket_name + '/' +  f_name
			thumbnail_url = 'https://s3.amazonaws.com/' + bucket_name + '-thumbnail/' + 'thumbnail-' + f_name
#			print f_name
#			print f_path
#			print s3_url
#			print thumbnail_url
	
			download_image(i['img_url'],f_name)
			target_bucket = conn_s3.get_bucket(bucket_name)
			file = Key(target_bucket)
			file.key = f_name
			file.set_contents_from_filename(f_path)
			i['img_flag'] = '1'
			i['s3_url'] = s3_url
			i['thumbnail_url'] = thumbnail_url
			i.partial_save()
			print 'img downloaded and upload to S3'

		except Exception,e:
			print 'no image'


if __name__ == '__main__' :
	print '------ Starting download images ------'
	dl_img()
