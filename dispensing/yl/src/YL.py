#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   YL.py    
@Desc    :   
@Project :   yl
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2020, ZJH
@WebSite :   zjh567.github.io
@Modify Time           @Author        @Version
------------           -------        --------
2020/01/14 11:31       ZJH            1.0         
'''
import requests
import json

from yl.src.config import *


class YL(object):
	def __init__(self, payload):
		# payload 格式参见 config 的 dispensing_payload
		self.college_url = college_url
		self.dispensing_url = dispensing_url
		self.payload = payload
		
	def college_list(self, province):
		'''
		输入省份，返回省份大学列表：ID，名字
		:param province: 省份名字，如：四川、内蒙古、重庆等等
		:return: 大学列表，列表元素为大学信息字典
		'''
		resp = requests.get(url=self.college_url + province, headers=headers)
		html = resp.text
		js = json.loads(html)
		data = js["data"]
		return data
	
	
	def yl_interface(self):
		'''
		根据 payload，返回查到的调剂信息
		:return: 信息列表
		'''
		resp = requests.get(url=self.dispensing_url, headers=headers, params=self.payload)
		html = resp.text
		js = json.loads(html)
		data = js["data"]["data"]
		return data
	

## 直接运行即可
if __name__ == '__main__':
	yl = YL(dispensing_payload)
	p = "重庆"
	print(yl.college_list(p))
	print(yl.yl_interface())
	

