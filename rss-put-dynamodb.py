#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto.dynamodb2
import feedparser
import urllib2
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.types import NUMBER
from boto.dynamodb2.items import Item
from BeautifulSoup import BeautifulSoup

def fmt(num):
   if num <= 9:
        num_n = '0' + str(num)
        return num_n
   else:
        return str(num)

def attach_category(org_title):
	chk_title = org_title.lower()
	if 'cloud' in chk_title:
		return 'cloud'
	if 'aws' in chk_title:
		return 'aws'
	if 'iot' in chk_title:
		return 'iot'
	if 'bigdata' in chk_title:
		return 'bigdata'
	else:
		return 'none'

def get_img_url(site_url):
        res = urllib2.urlopen(site_url)
        soup = BeautifulSoup(res.read())
        for link in soup.findAll('img'):
                if 'alt' in str(link):
                        if( link.has_key('src')):
                                imgSrc = link['src']
                                imgFile = imgSrc.split('/')[-1]
                                ext = imgFile.split('.')[-1]
                                if( ext == 'jpg' or ext == 'jpeg' or ext == 'png'):
                                        img_url = link.get('src')
                                        return img_url
                                        break

rssurl="http://54.64.75.5/?feed=rss2"
#rssurl="http://rss.rssad.jp/rss/itmnews/2.0/news_society.xml"
#rssurl="http://rss.rssad.jp/rss/itmnews/2.0/news_nettopics.xml"
#rssurl="http://feeds.feedburner.com/AmazonWebServicesBlogJp?format=xml"

fd = feedparser.parse(rssurl)

conn = boto.dynamodb2.connect_to_region('ap-northeast-1')
print conn.list_tables()

table_name = 'cic-tech-info'

for i in range(3):
	img_url = get_img_url(fd.entries[i].link)
	category = attach_category(fd.entries[i].title)
	tmp = fd.entries[i].published_parsed
	uptime = str(tmp[0]) + '-' + fmt(tmp[1]) + fmt(tmp[2]) + '-' + fmt(tmp[3]) + fmt(tmp[4]) + fmt(tmp[5])
	table = Table(table_name, connection=conn)
	table.put_item(data={
		'Category' : category,
		'LastUpdateTime': uptime,
		'URL': fd.entries[i].link,
		'Title': fd.entries[i].title,
		'Summary': fd.entries[i].summary,
		'img_url': img_url,
		'img_flag': '0',
		's3_url': 'none'
	},overwrite = True)
