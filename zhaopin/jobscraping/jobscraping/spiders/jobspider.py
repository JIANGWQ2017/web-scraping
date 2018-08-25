# -*- coding: utf-8 -*-
import scrapy
import re
from time import sleep
import json
import csv
import os
from jobscraping.items import JobscrapingItem

class JobspiderSpider(scrapy.Spider):
	name = 'jobspider'
	allowed_domains = ['https://fe-api.zhaopin.com']
	start_urls = ['''https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=489&
		workExperience=-1&education=-1&companyType=-1&employmentType=-1&
		jobWelfareTag=-1&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88&kt=3&
		lastUrlQuery=%7B%22jl%22:%22489%22,%22kw%22:%22%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88%22,%22kt%22:%223%22%7D''']
	# url prefix and postfix to construct new url about job details
	url_prefix = 'https://jobs.zhaopin.com/'
	url_surfix = '.htm'
	# parameter needed to construct next main page url
	start_num = 0
	# count page num
	page = 1
	# count job num in one page
	count = 1
	
	
	def parse(self, response):
		js = json.loads(response.body)
		job_count = 1
		# used as the stop condiction, if num_job_in_page = 0 , means no more jobs to scrape
		num_job_in_page = len(js['data']['results'])
		
		# fetch basic infos in a page
		for job in js['data']['results']:
			# needed to construction job detail page url
			company_num = job['number']
			# instantiate JobscrapingItem
			item = JobscrapingItem()
			# extracting informations
			item['job_name'] = job['jobName'],
			item['job_salary'] = job['salary'],
			item['workExperienced'] = job['workingExp']['name'],
			item['eduLevel'] = job['eduLevel']['name']
			item['job_empltype'] = job['emplType'],
			item['job_welfare']= job['welfare'],
			item['job_type'] = job['jobType']['display']
			item['company_url'] = job['company']['url'],
			item['company_name'] = job['company']['name'],
			item['company_type'] = job['company']['type']['name'],
			item['company_size'] = job['company']['size']['name'],
			item['company_geo'] = job['geo'],
			item['company_city'] = job['city']['display']
			#fecthing details
			print('fecthing details of job {} in page {}...'.format(str(job_count),str(self.page)))
			job_count += 1
			#construct job detail page url
			detail_url = self.url_prefix + str(company_num) + self.url_surfix
			sleep(0.5)
			yield scrapy.Request(detail_url,meta={'item':item},callback=self.job_details,dont_filter=True)
		print('\n finished getting infos in page {}\n'.format(str(self.page)))
		self.page += 1
		# iteration;  fetch next main page url, until no more jobs to scrape
		prefix = self.start_urls[0].split('?')[0]
		surfix = self.start_urls[0].split('?')[1]
		if num_job_in_page != 0:
			self.start_num += 60
			next_url = prefix+'?start='+str(self.start_num)+'&' + surfix
			yield scrapy.Request(next_url,callback = self.parse,dont_filter=True)
		
		
	def job_details(self,response):
		item = response.meta['item']
		#fetch description for each job
		description_list = response.xpath('/html/body/div[6]/div[1]/div[1]/div[1]/div[1]//text()').extract()
		description = ''
		for des in description_list:
			description += des.strip()
		item['description'] = description
		print('\nadd one job {}\n'.format(str(self.count)))
		self.count += 1
		yield item
