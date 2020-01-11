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

# 你的名字, 如：HUI
NAME = "HUI"

# 城市，北上广深分别为：bj、sh、gz、sz
CITY = "gz"

# tech\job
AREA = "job"

# 浏览器 UA，即你使用的默认浏览器 UA，火狐的为：
# "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0"
User_Agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0"

# 数据库配置
DBConf = {
		"host": "127.0.0.1",
		"user": "root",
		"password": "20192019zz",
		"database": "58"
	}
# DBConf = {
# 		"host": "数据库 IP，非云数据库请设置为：127.0.0.1",
# 		"user": "用户名",
# 		"password": "用户密码",
# 		"database": "数据库名字"
# 	}

# 关键字，不要更改
# KW = ""

# SQL命令目录
sqlDir = "./sql_cmds/"

# 开始页码，自行更改
BEGIN_INDEX = 3

# 最多爬取多少页
END_INDEX = 100


