#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   db.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/19 22:42   thefreer      1.0         
'''
import pymysql
import os
import time
import json

from setting import DBConf, NAME

def create_table(filepath):
	db = pymysql.connect(**DBConf)
	cursor = db.cursor()
	sql_table = open(filepath, 'r')
	sql_cmd = sql_table.readlines()
	sqlCmd = ''
	for sql_c in sql_cmd:
		sqlCmd += sql_c
	# print(sqlCmd)
	cursor.execute(sqlCmd)
	db.commit()
	return db, cursor

def data_pause(result, item):
	company = {}
	recruitment = {}
	
	## 公司信息
	company["Company_ID"] = result["company"]["number"]
	company["comSize"] = json.dumps(result["company"]["size"])
	company["comName"] = result["company"]["name"]
	company["comType"] = json.dumps(result["company"]["type"])
	company["comTagZhiLian"] = item[2][3]
	company["comAddr"] = item[2][4]
	company["description"] = item[2][0]
	company["positionURL"] = result["company"]["url"]
	company["vipLevel"] = result["vipLevel"]
	company["score"] = result["score"]
	company["resumeTotal"] = item[2][1]  # result["resumeCount"}
	company["recruitTotal"] = 0  # result["recruitCount"]
	company["interviewTotal"] = item[2][2]  # result["interview"]
	Update_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	
	company["Source_Website"] = "www.zhaopin.com"
	company["Update_Name"] = NAME
	company["Update_Time"] = Update_Time
	
	## 招聘信息
	recruitment["Job_ID"] = result["number"]
	recruitment["Company_ID"] = result["company"]["number"]
	recruitment["jobName"] = result["jobName"]
	recruitment["jobType"] = json.dumps(result["jobType"])
	recruitment["jobTagZhiLian"] = json.dumps(result["jobTag"])
	recruitment["detailAddr"] = item[1]
	recruitment["description"] = item[0]
	recruitment["salary"] = result["salary"]
	welfareList = result["welfare"]
	welfare = ""
	for w in welfareList:
		welfare += w
		welfare += ","
	recruitment["welfare"] = welfare
	recruitment["workingExp"] = json.dumps(result["workingExp"])
	recruitment["eduLevel"] = json.dumps(result["eduLevel"])
	recruitment["resumeCount"] = result["resumeCount"]
	recruitment["recruitCount"] = result["recruitCount"]
	recruitment["positionURL"] = result["positionURL"]
	recruitment["emplType"] = result["emplType"]
	recruitment["recentAndTotal"] = json.dumps(result["recentAndTotal"])
	recruitment["feedbackRation"] = result["feedbackRation"]
	recruitment["interview"] = result["interview"]
	recruitment["selected"] = result["selected"]
	recruitment["applied"] = result["applied"]
	recruitment["collected"] = result["collected"]
	
	recruitment["Source_Website"] = "www.zhaopin.com"
	recruitment["Update_Name"] = NAME
	recruitment["Update_Time"] = Update_Time
	
	insert_data = [company, recruitment]
	return insert_data
	

def data_insert(data):
	company = data[0]
	recruitment = data[1]
	db = pymysql.connect(**DBConf)
	cursor = db.cursor()
	try:
		cursor.execute(
			"insert into company(Company_ID,comSize,comName,comType,comTagZhiLian,comAddr,description,positionURL,vipLevel,score,resumeTotal,recruitTotal,interviewTotal,Source_Website,Update_Name,Update_Time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
			(company["Company_ID"],company["comSize"],company["comName"],company["comType"],company["comTagZhiLian"],company["comAddr"],company["description"],company["positionURL"],company["vipLevel"],company["score"],company["resumeTotal"],company["recruitTotal"],company["interviewTotal"],company["Source_Website"],company["Update_Name"],company["Update_Time"])
			)
		db.commit()
	except:
		pass
	try:
		cursor.execute(
			"insert into recruitment(Job_ID,Company_ID,jobName,jobType,jobTagZhiLian,detailAddr,description,salary,welfare,workingExp,eduLevel,resumeCount,recruitCount,positionURL,emplType,recentAndTotal,feedbackRation,interview,selected,applied,collected,Source_Website,Update_Name,Update_Time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
			(recruitment["Job_ID"],recruitment["Company_ID"],recruitment["jobName"],recruitment["jobType"],recruitment["jobTagZhiLian"],recruitment["detailAddr"],recruitment["description"],recruitment["salary"],recruitment["welfare"],recruitment["workingExp"],recruitment["eduLevel"],recruitment["resumeCount"],recruitment["recruitCount"],recruitment["positionURL"],recruitment["emplType"],recruitment["recentAndTotal"],recruitment["feedbackRation"],recruitment["interview"],recruitment["selected"],recruitment["applied"],recruitment["collected"],recruitment["Source_Website"],recruitment["Update_Name"],recruitment["Update_Time"])
			)
		db.commit()
	except:
		pass

if __name__ == '__main__':
	baseDir = "./sql_cmds/"
	pathList = os.listdir(baseDir)
	print(pathList)
	for path in pathList:
		create_table(baseDir + path)