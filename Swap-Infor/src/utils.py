#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py    
@Desc    :   
@Project :   Swap-Infor
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time           @Author        @Version
------------           -------        --------
2020/01/12 23:18       the freer      1.0         
'''

from src.config import school_list

ss = []
for city in school_list:
	cid = city["id"]
	cname = city["name"]
	school = city["school"]
	school_info = {
		"cid": cid,
		"cname": cname,
		"school": []
	}
	for s in school:
		sid = s["id"]
		sname = s["name"]
		school_info["school"].append((sid, sname))
	ss.append(school_info)
	
print(ss)