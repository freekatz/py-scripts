#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   MC.py
@Desc    :   
@Project :   Swap-Infor
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2020/01/12 23:55       the freer      1.0         
'''
import requests
from bs4 import BeautifulSoup

from src.config import *

class MC(object):
	def __init__(self, payload):
		# payload 格式参见 config 的 index_payload
		self.url = url
		self.payload = payload
	
	def mc_interface(self):
		# 返回列表页面的 html
		resp = requests.get(url=self.url, headers=headers, params=self.payload)
		html = resp.text
		return html
	
	def info_list(self, page):
		'''
		返回每页的信息列表
		:param page: 页码
		:return: 返回字典的列表
		'''
		self.payload["page"] = page
		data_list = []
		soup = BeautifulSoup(self.mc_interface(), "lxml")
		t_soup = soup.select("tbody.forum_body_manage")[0]
		for idx, tr in enumerate(t_soup.find_all('tr')):
			if idx != 0:
				tds = tr.find_all('td')
				data_list.append({
					'durl': tds[0].a["href"],
					'title': tds[0].text.strip(),
					'school': tds[1].text.strip(),
					'subject': tds[2].text,
					'number': tds[3].text,
					'date': tds[4].text
				})
		return data_list
	
	def info_detail(self, durl):
		'''
		得到详情页信息
		:param durl: 信息列表中获得的详情页 url
		:return: 补充信息
		'''
		html = requests.get(durl, headers=headers).text
		soup = BeautifulSoup(html, "lxml").select("div.t_fsz")[0]
		return str(soup.text.strip())

## 直接运行即可
if __name__ == '__main__':
	mc = MC(index_payload)
	info_list =  mc.info_list(1)
	u = info_list[2]["durl"]
	for key in info_list[2]:
		print(info_list[2][key])
	print(mc.info_detail(u))
	