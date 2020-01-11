#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Desc:   :   主控制模块
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/2/27 19:12   thefreer      1.0
'''
from urllib import parse
import xlwt
from core import Searcher, Cookier
from modules import keywords_reader, set_table, sleepRandom
import re
import asyncio

if __name__ == '__main__':
	path = "./in_data/excels/0.xls"
	print("当前爬取的 excel 表格路径 %s" % path)
	with open('sec_data/cookies.txt', 'r') as f:
		cookies = f.readline()
	f.close()
	keywords = keywords_reader(path)
	cookier = Cookier()
	db, cursor = set_table()
	index = 0
	for key in keywords:
		print("####=====index:%s, keyword:%s====####" % (str(index), key))
		index+=1
		sleepRandom(8)
		k = "iphone"
		keyword = parse.quote(k)
		url = "https://s.taobao.com/search?q=%s&sort=sale-desc" % keyword
		searcher = Searcher(url=url, db=db, cursor=cursor)
		goods, db, cursor = searcher.get_data(cookies)
		if goods != {}:
			print("succ next, print goods")
			print(goods)
		else:
			print("fail will try")
			try:
				loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
				new_cookies = loop.run_until_complete(cookier.cookie_main(url=url, cookies=cookies))  # 将协程注册到事件循环，并启动事件循环
				cookies = re.sub("x5sec=(.*)", "", cookies)
				cookies += new_cookies
			except:
				pass
			with open('sec_data/cookies.txt', 'w') as c:
				c.write(cookies)
			c.close()
			goods, _, _ = searcher.get_data(cookies)
			print("try again, print goods")
			print(goods)