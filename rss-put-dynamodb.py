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

def get_rss(rssurl, table_name, media):
   fd = feedparser.parse(rssurl)
#   conn = boto.dynamodb2.connect_to_region('ap-northeast-1')
   conn = boto.dynamodb2.connect_to_region('us-east-1')
   
   for i in range(3):
	try:
		img_url = get_img_url(fd.entries[i].link)
		category = attach_category(fd.entries[i].title)
		tmp = fd.entries[i].published_parsed
		rangekey = media + '_' +  str(tmp[0]) + '-' + fmt(tmp[1]) + fmt(tmp[2]) + '-' + fmt(tmp[3]) + fmt(tmp[4]) + fmt(tmp[5])
		uptime = str(tmp[0]) + '-' + fmt(tmp[1]) + fmt(tmp[2]) + '-' + fmt(tmp[3]) + fmt(tmp[4]) + fmt(tmp[5])

		try:
		   conn.put_item(
			table_name,item={
			'category' : {'S' : category},
			'rangekey': {'S' : rangekey},
			'UpdateTime': {'S' : uptime},
			'url': {'S' : fd.entries[i].link},
			'title': {'S' : fd.entries[i].title},
			'summary': {'S' : fd.entries[i].summary},
			'img_url': {'S' : img_url},
			'img_flag': {'S' : '0'},
			's3_url': {'S' : 'none'},
			'thumbnail_url': {'S' : 'none'},
			'media': {'S' : media}
			},
			expected = {
			   'rangekey' : {"Exists" : False}
			}
		   )
		   print 'True'
		except Exception,e:
		   print 'False'

	except Exception,e:
	   print 'No Contents'		

org_table_name = 'cic-tech-info'

wp_rssurl="http://54.64.75.5/?feed=rss2"
#rssurl="http://rss.rssad.jp/rss/itmnews/2.0/news_society.xml"
#rssurl="http://rss.rssad.jp/rss/itmnews/2.0/news_nettopics.xml"
#rssurl="http://feeds.feedburner.com/AmazonWebServicesBlogJp?format=xml"

print 'wp'
media_name = 'wp'
get_rss(wp_rssurl, org_table_name, media_name)
print '\n'

#print 'itmedia'
#itmedia_rssurl="http://rss.rssad.jp/rss/itmnews/2.0/news_society.xml"
#media_name = 'itmedia'
#get_rss(itmedia_rssurl, org_table_name, media_name)
#print '\n'

##print 'asahi'
##asahi_digital_rssurl="http://rss.asahi.com/rss/asahi/digital.rdf"
##media_name = 'asahi'
##get_rss(asahi_digital_rssurl, org_table_name, media_name)
##print '\n'

#print 'reuter'
#reuter_rssurl="http://feeds.reuters.com/reuters/JPTechnologyNews?format=xml"
#media_name = 'reuter'
#get_rss(reuter_rssurl, org_table_name, media_name)
#print '\n'

##print 'mynavi'
##mynavi_rssurl="http://pubsubhubbub.appspot.com"
##media_name = 'mynavi'
##get_rss(mynavi_rssurl, org_table_name, media_name)
##print '\n'

#print 'aws'
#awsblog_rssurl="http://feeds.feedburner.com/AmazonWebServicesBlogJp?format=xml"
#media_name = 'aws'
#get_rss(awsblog_rssurl, org_table_name, media_name)
#print '\n'
