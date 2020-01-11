#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/20 18:34   thefreer      1.0         
'''

import os
import re
import random

from db import data_pause, data_insert, create_table
from core import getKW, searchSpider, detailSpider
from thread import ThreadPool
# from setting import PAGE_MAX_NUM, DB_MAX_THREAD_NUM, DATA_MAX_THREAD_NUM, DETAIL_MAX_THREAD_NUM, SEARCH_MAX_THREAD_NUM
from setting import PAGE_MAX_NUM, MAX_THREAD_NUM, kwPath


if __name__ == '__main__':
	# def callback(result):
	# 	print(result)
	# 	return result
	count = 0
	pool = ThreadPool(MAX_THREAD_NUM)
	
	
	sqlDir = "./sql_cmds/"
	pathList = os.listdir(sqlDir)
	# 建表，如果存在跳过
	for path in pathList:
		create_table(sqlDir + path)
		
	# 获取关键字
	with open(kwPath, "r", encoding="utf-8") as f:
		kws = f.readlines()
	# kws = getKW()
	# print(kws)
	
	# 将关键字设置为随机获取，更加人性化
	# 添加关键字提示，并且保存最后一个爬取的关键字，这个没啥卵用，备用
	indexs = []
	have_spider = []
	last_spider = ""
	while len(have_spider) != len(kws):
		index = random.randint(0, len(kws))
		if index not in indexs:
			indexs.append(index)
			kw = kws[index]
			last_spider = kw
			with open("last_kw.txt", "w", encoding="utf-8") as f:
				f.write(last_spider)
			start = 0
			temp = PAGE_MAX_NUM
			while temp > 0:
				# results = searchPool.run(searchSpider, (kw, start), callback=callback)
				results = searchSpider(kw, start)
				for result in results:
					count += 1
					print("####  %s  ######    %s    ###########" % (kw, str(count)))
					url = result["positionURL"]
					comUrl = result["company"]["url"]
					print(comUrl)
					comId = re.sub(r"(\D)", "", result["company"]["number"])[:-1]
					print(url)
					pool.run(detailSpider, (url, comUrl, comId, result))
					# print(item)
	
				temp -= 90
				start += 90
			have_spider.append(kw)