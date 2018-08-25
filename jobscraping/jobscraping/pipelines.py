# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class JobscrapingPipeline(object):
	def __init__(self):
		client = MongoClient()
		# select database 'job_data', if not exist, creat one
		self.db = client['job_data']
	
	
	def process_item(self, item, spider):
		# insert data into collection :'data_related_jobs'
		self.db.data_related_jobs.insert(dict(item))
		return item
