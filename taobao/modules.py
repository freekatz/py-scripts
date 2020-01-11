#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   modules.py
@Desc    :   工具模块
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/2/27 17:22   thefreer      1.0
'''
import random
import time
import xlwt
import xlrd
import os
import pymysql

def keywords_reader(excel):
	"""
	读取一个文件里的所有 关键字
	:param excel:
	:return: 关键字列表
	"""
	book = xlrd.open_workbook(excel)
	table = book.sheets()[0]
	keywords = table.col_values(2)[1:]
	return keywords
	
def set_table():
	# ==================#MySQL连接代码区#==================#
	'''
	连接数据库, 先建库:
	create database taobao
	default character set utf8
	default collate utf8_general_ci;
	'''
	config = {
		"host": "127.0.0.1",
		"user": "root",
		"password": "20192019zz",
		"database": "test"
	}
	db = pymysql.connect(**config)
	cursor = db.cursor()
	'''
	建表：从文件中读入建表指令，并运行，如果表test58不存在就建表
	'''
	sql_table = open('./sec_data/sql_table.txt', 'rb')
	sql_cmd = sql_table.readlines()
	sqlCmd = ''
	for sql_c in sql_cmd:
		sqlCmd += sql_c.decode()
	# print(sqlCmd)
	cursor.execute(sqlCmd)
	db.commit()
	return db, cursor

def excel_spilt(limit):
	"""
	分割一个表格为行数为 100 的若干个表格
	:param limit: 数量
	:return:
	"""
	os.mkdir("./in_data/excels")
	readbook = "./in_data/test.xls"  # 原始文件路径
	savebook = "./in_data/excels/"  # 要保存的目录
	data = xlrd.open_workbook(readbook)  # 获取sheet
	table = data.sheets()[0]  # 获取第一个sheet的所有数据 # 行数
	nrows = table.nrows  # 列数
	ncols = table.ncols
	sheets = nrows / limit  # 总共需要多少excel
	
	if not sheets.is_integer():  # 如果不是整除则需要+1
		sheets = sheets + 1
	
	title_row = table.row_values(0)  # 获取首行的标题 #
	for i in range(0, int(sheets)):
		workbook = xlwt.Workbook(encoding='ascii')
		worksheet = workbook.add_sheet(sheetname="0")  # 设置sheet名称 for col in range(0,ncols):#写首行的标题
		for col in range(0, ncols):  # 写首行的标题
			worksheet.write(0, col, title_row[col])
		for row in range(1, limit + 1):  # 每次循环limit行
			newRow = row + limit * i
			if newRow < nrows:
				row_content = table.row_values(newRow)
				for col in range(0, ncols):
					worksheet.write(row, col, row_content[col])
					workbook.save(savebook + "/" + str(i) + ".xls")

def sleepRandom(t):
	"""
	睡眠随机时长
	:param t:
	:return:
	"""
	sleep = random.randint(t, t+random.randint(60, 80))
	# sleep = 1
	time.sleep(sleep)

if __name__ == '__main__':
	# excel_spilt(25)
	path = "./in_data/excels/0.xls"
	keywords = keywords_reader(path)
	print(keywords)