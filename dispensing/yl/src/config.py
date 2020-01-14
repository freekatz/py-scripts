#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py    
@Desc    :   
@Project :   yl
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2020, ZJH
@WebSite :   zjh567.github.io
@Modify Time           @Author        @Version
------------           -------        --------
2020/01/14 11:32       ZJH            1.0         
'''

college_url = "http://apis.kaoyancun.com/dispensing-data/dis-data/getCollegebyProvince?province="
dispensing_url = "http://apis.kaoyancun.com/dispensing-data/dis-data/dispensingInfo"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
}

# proxies = {
# 	"http": "127.0.0.1:10808"
# }

dispensing_payload = {
	"province": "安徽", # 省份名字，如：四川、内蒙古、重庆等等
	"college_code": "", # 建议设为空，毕竟你指定的学校不一定有
	"mode": "1", # 1 代表全日制，2 代表非全
	"major_keyword": "计算机科学与技术", # 学科完整名称
	"year": "2019", # 年份
	"page": "2", # 页码
	"pageSize": "10" # 列表长度
}
