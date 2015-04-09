#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto.dynamodb2
import feedparser
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.types import NUMBER
from boto.dynamodb2.items import Item

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


#rssurl="http://54.64.75.5/?feed=rss2"
#rssurl="http://rss.rssad.jp/rss/itmnews/2.0/news_society.xml"
#rssurl="http://rss.rssad.jp/rss/itmnews/2.0/news_nettopics.xml"
#rssurl="http://feeds.feedburner.com/AmazonWebServicesBlogJp?format=xml"

fd = feedparser.parse(rssurl)

conn = boto.dynamodb2.connect_to_region('ap-northeast-1')
print conn.list_tables()

table_name = 'cic-tech-info'

for i in range(5):
	category = attach_category(fd.entries[i].title)
	table = Table(table_name, connection=conn)
	table.put_item(data={
		'Category' : category,
		'LastUpdateTime': fd.entries[i].published,
		'URL': fd.entries[i].link,
		'Title': fd.entries[i].title,
		'Summary': fd.entries[i].summary,
	},overwrite = True)
