#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setting.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/16 14:56   thefreer      1.0         
'''

#@ "配置文件"
import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir = os.getcwd()
sys.path.append(dir)

# 你的名字, 如：HUI
NAME = "HUI"

# 数据库配置
DBConf = {
		"host": "127.0.0.1",
		"user": "root",
		"password": "20192019zz",
		"database": "test"
	}

# 关键字文件路径
kwPath = "./kws/kw1.txt"

# 最大线程数目, 请自行测试适合自己电脑的数目，太多太少都影响效率
MAX_THREAD_NUM = 10
# # 搜索线程数
# SEARCH_MAX_THREAD_NUM = 2
#
# # 详情页爬虫最大线程数目
# DETAIL_MAX_THREAD_NUM = 6
#
# # 数据解析线程数目
# DATA_MAX_THREAD_NUM = 5
#
# # 数据存取线程数目
# DB_MAX_THREAD_NUM = 3

# 每一页爬取多少记录
PAGE_MAX_NUM = 90 * 12

# 代理最大尝试次数
PROXY_RETRY_NUM = 3

# print(BASE_DIR)

