# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	
	# initilize item object
	
	# job name
	job_name = scrapy.Field()
	# job salary
	job_salary = scrapy.Field()
	# required work experience
	workExperienced = scrapy.Field()
	# required education level
	eduLevel = scrapy.Field()
	# employment type 
	job_empltype = scrapy.Field()
	#welfare
	job_welfare= scrapy.Field()
	# job category 
	job_type = scrapy.Field()
	# company url
	company_url = scrapy.Field()
	# company name
	company_name = scrapy.Field()
	# company category
	company_type = scrapy.Field()
	#company size
	company_size = scrapy.Field()
	#company geographic position
	company_geo = scrapy.Field()
	# city that company locate 
	company_city = scrapy.Field()
	#job details description
	description = scrapy.Field()