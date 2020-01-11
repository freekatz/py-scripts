#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   core.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/20 18:35   thefreer      1.0         
'''
import requests
import json
import re
from bs4 import BeautifulSoup

from proxy import get_proxy, del_proxy
from db import data_pause, data_insert
from thread import ThreadPool
from setting import PROXY_RETRY_NUM, MAX_THREAD_NUM

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
}


## keywords get
def getKW():
	url = " http://www.zhaopin.com/"
	proxy = get_proxy()
	retry_num = PROXY_RETRY_NUM
	while retry_num > 0:
		try:
			resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
			html = resp.text
			soup = BeautifulSoup(html, "lxml")
			# 获取关键字
			items = soup.select("a.zp-jobNavigater__pop--href")
			kws = []
			# with open("./keywords.txt", "w") as f:
			for item in items:
					# f.writelines(item.text + "\n")
				kws.append(item.text)
			return kws
		except:
			retry_num -= 1
	del_proxy(proxy)


def searchSpider(kw, start):
	# time.sleep(1)
	proxy = get_proxy()
	url = " http://fe-api.zhaopin.com/c/i/sou?start=%s&pageSize=90&cityId=489&kw=%s&kt=3" % (str(start), kw)
	retry_num = PROXY_RETRY_NUM
	while retry_num > 0:
		try:
			resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
			html = resp.text
			js = json.loads(html)
			# 获取搜索结果
			results = js["data"]["results"]
			return results
		except:
			retry_num -= 1
	del_proxy(proxy)


def detailSpider(url, curl, cid, result):
	url = url.replace("https:", "http:")
	curl = curl.replace("https:", "http:")
	proxy = get_proxy()
	# pool1 = ThreadPool(10)
	# pool2 = ThreadPool(5)
	retry_num = PROXY_RETRY_NUM
	while retry_num > 0:
		try:
			resp = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
			html = resp.text
			soup = BeautifulSoup(html, "lxml")
			
			# 获取招聘介绍，workItem
			try:
				workStr = soup.select_one("div.describtion__detail-content").text.replace("<br>", "")
				workSoup = BeautifulSoup(workStr, "lxml")
				workItem = ""
				for item in workSoup.select("p"):
					workItem += item.text
			except:
				workStr = soup.select_one("div.pos-ul")
				workSoup = BeautifulSoup(str(workStr), "lxml")
				workItem = ""
				for item in workSoup.select("p"):
					workItem += item.text
				if workItem == "":
					for item in workSoup.select("div"):
						workItem += item.text
				else:
					for item in workSoup.select("span"):
						workItem += item.text
			
			# 获取职位就业地点，addrItem
			addrStr = soup.select_one("div.work-add")
			addrSoup = BeautifulSoup(str(addrStr), "lxml")
			try:
				addrItem = addrSoup.select_one("p.add-txt").text
			except:
				addrItem = soup.select_one("span.job-address__content-text").text
			
			# 获取和公司有关的信息，[comItem, resumeTotal, interviewTotal, comTag, comAddr]
			if "company.zhaopin.com" in curl:
				cresp = requests.get(curl, headers=headers, proxies={"http": "http://{}".format(proxy)})
				chtml = cresp.text
				csoup = BeautifulSoup(chtml, "lxml")
				try:
					comItem = re.sub(r"({.*})", "", csoup.select_one("div.company-show__content__description").text)
				except:
					comItem = ""
				
				try:
					comTag = csoup.select_one("div.overview__detail-industry").text
				except:
					comTag = ""
					
				try:
					comAddr = csoup.select_one("p.map-box__adress").text
				except:
					comAddr = ""
				
				resumeTotal = csoup.select_one("span.com-interview__item__num").text
				
				inter_url = " http://fe-api.zhaopin.com/c/i/company/interview?rootCompanyId=%s&companyId=%s" % (
						cid, cid)
				iresp = requests.get(inter_url, headers=headers, proxies={"http": "http://{}".format(proxy)})
				ihtml = iresp.text
				ijs = json.loads(ihtml)
				interviewTotal = str(ijs["data"]["data"])
			else:
				comItem = curl
				resumeTotal = "0"
				interviewTotal = "0"
				comTag = ""
				comAddr = ""
			
			detailItems = [workItem, addrItem, [comItem, resumeTotal, interviewTotal, comTag, comAddr], ]
			data = data_pause(result, detailItems)
			data_insert(data)
			# data = pool.run(data_pause, (result, detailItems))
			# pool2.run(data_insert, (data))
			return detailItems
			# return
		except:
			retry_num -= 1
	del_proxy(proxy)

if __name__ == '__main__':
	# getKW()
	pool = ThreadPool(20)
	# p = ThreadPool(10)
	detailPool = threadpool.ThreadPool(20)
	results = searchSpider("Java", 100)
	args = []
	for result in results:
		url = result["positionURL"]
		comUrl = result["company"]["url"]
		print(comUrl)
		print(result["company"]["number"])
		comId = re.sub(r"(\D)", "", result["company"]["number"])[:-1]
		print(comId)
		print(url)
		print(result["number"])
		# item = detailSpider(url, comUrl, comId)
		# print(item)
		arg = [url, comUrl, comId]
		args.append((arg, None))
	print(args)
	requests = threadpool.makeRequests(detailSpider, args)
	for req in requests:
		item = detailPool.putRequest(req)
		print(item)
	detailPool.wait()
	
	# data = pool.run(data_pause, (result, item, ))
# p.run(data_insert, (data, ))

# s = data_pause(test, detailItems)[1]
# str = ""
# tsr = ""
# ss = ""
# jsr = ""
# for i in s:
# 	tsr += i + ","
# 	ss += "%s,"
# 	str += 'company["' + i + '"]' + ","
# 	jsr += 'recruitment["' + i + '"]' + ","
# print(tsr)
# print(ss)
# print(str)
# print(jsr)