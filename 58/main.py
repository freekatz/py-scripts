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
2019/4/10 20:32   thefreer      1.0         
'''
import os
import pymysql
import sys

from db import createTable, queryCompanyExist, insertDataC, insertDataJ, insertDataCJ
from core import searchList, coreMain
from setting import DBConf, AREA, sqlDir, BEGIN_INDEX, END_INDEX

def main(db, companyBaseUrl, companyId):
	result = coreMain(companyBaseUrl, companyId)
	if result == False:
		print("此IP已被58同城限制，请手动在浏览器中打开58.com中任一招聘详情页进行验证码验证，或者休息一段时间再来运行这个爬虫，谢谢合作。")
		sys.exit(-1)
	elif result == []:
		print("此公司是名企，跳过")
		return
	else:
		resultList = result
	companyInfoDict = resultList[0]
	insertDataC(db, companyInfoDict)
	for index in range(1, len(resultList)):
		job = resultList[index]
		jobInfoDict = job[0]
		insertDataJ(db, jobInfoDict)
		CJRelationDict = job[1]
		insertDataCJ(db, CJRelationDict)
	return

if __name__ == '__main__':
	db = pymysql.connect(**DBConf)
	pathList = os.listdir(sqlDir)
	# 建表，如果存在跳过
	for path in pathList:
		createTable(db, sqlDir + path)
	for index in range(BEGIN_INDEX, END_INDEX):
		print("————————|—————%s—————|————————" % (str(index)))
		print("一共 %s 页，当前正在爬取第 %s 页" % (str(END_INDEX - BEGIN_INDEX), str(index)))
		# time.sleep(5)
		companyBaseUrlList, companyIdList = searchList(AREA, index)
		for (companyBaseUrl, companyId) in zip(companyBaseUrlList, companyIdList):
			print("———————||——————第%s页—————||——————————" % str(index))
			print("当前爬取的公司链接为：%s" % companyBaseUrl)
			flag = queryCompanyExist(db, companyId)
			if flag == False:
				print("公司信息已存在，跳过")
				continue
			else:
				print("初次爬取此公司，稍等")
			# time.sleep(2)
			main(db, companyBaseUrl, companyId)
		

