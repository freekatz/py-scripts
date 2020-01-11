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

def createTable(db, filepath):
	# db = pymysql.connect(**DBConf)
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

def generateInsertCommand(data, tableName):
	insertData = data
	dataName = "insertData"
	keyStr = ""
	sStr = ""
	valueStr = ""
	i = 0
	for key in insertData:
		keyStr += key
		sStr += "%s"
		valueStr += 'str(%s["%s"])' % (dataName, key)
		if i != len(insertData) - 1:
			keyStr += ","
			sStr += ","
			valueStr += ","
		i+=1
	# "insert into test58(userid,sjfl) values(%s,%s)",(sqlDict[key][0],key)
	insertCommand = '"insert into %s (' % tableName + keyStr + ') values(' + sStr + ')", (' + valueStr + ')'
	print(insertCommand)

def insertDataC(db, data):
	insertData = data
	cursor = db.cursor()
	cursor.execute("insert into company (Company_ID,positionTotal,companyBaseUrl,companyName,companyTrade,companyCharacter,feedbackRation,companySize,companyAddr,companyIntro,businessScope,companyType,creditCode,estiblishDate,operatingStatus,orgNumber,regAddress,regAuthority,regCapital,teamTime,entUrl,companyDetailUrl,Update_Name,Update_Time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (str(insertData["Company_ID"]),str(insertData["positionTotal"]),str(insertData["companyBaseUrl"]),str(insertData["companyName"]),str(insertData["companyTrade"]),str(insertData["companyCharacter"]),str(insertData["feedbackRation"]),str(insertData["companySize"]),str(insertData["companyAddr"]),str(insertData["companyIntro"]),str(insertData["businessScope"]),str(insertData["companyType"]),str(insertData["creditCode"]),str(insertData["estiblishDate"]),str(insertData["operatingStatus"]),str(insertData["orgNumber"]),str(insertData["regAddress"]),str(insertData["regAuthority"]),str(insertData["regCapital"]),str(insertData["teamTime"]),str(insertData["entUrl"]),str(insertData["companyDetailUrl"]),str(insertData["Update_Name"]),str(insertData["Update_Time"])))
	db.commit()

def insertDataJ(db, data):
	insertData = data
	cursor = db.cursor()
	cursor.execute("insert into recruitment (Job_ID,jobTitle,jobSubTitle,jobSalary,applyNum,resumeReadPercent,browserNum,jobWelfare,jobRequirement,jobAddr,jobDescription,jobCity,Update_Name,Update_Time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (str(insertData["Job_ID"]),str(insertData["jobTitle"]),str(insertData["jobSubTitle"]),str(insertData["jobSalary"]),str(insertData["applyNum"]),str(insertData["resumeReadPercent"]),str(insertData["browserNum"]),str(insertData["jobWelfare"]),str(insertData["jobRequirement"]),str(insertData["jobAddr"]),str(insertData["jobDescription"]),str(insertData["jobCity"]),str(insertData["Update_Name"]),str(insertData["Update_Time"])))
	db.commit()

def insertDataCJ(db, data):
	insertData = data
	cursor = db.cursor()
	cursor.execute("insert into issue (Company_ID,Job_ID,jobUpdateTime,needNumber,jobDetailUrl,Update_Name,Update_Time) values(%s,%s,%s,%s,%s,%s,%s)", (str(insertData["Company_ID"]),str(insertData["Job_ID"]),str(insertData["jobUpdateTime"]),str(insertData["needNumber"]),str(insertData["jobDetailUrl"]),str(insertData["Update_Name"]),str(insertData["Update_Time"])))
	db.commit()

def queryCompanyExist(db, companyId):
	# select 1 from tablename where col = col limit 1;
	queryCommand = 'select * from company where Company_ID="%s" limit 1;' % companyId
	cursor = db.cursor()
	cursor.execute(queryCommand)
	try:
		if cursor.rowcount != 0:
			return False
		else:
			return True
	except:
		return False
	
	
	

if __name__ == '__main__':
	companyInfoDict = {
		"Company_ID": "", "positionTotal": "0", "companyBaseUrl": "",
		"companyName": "", "companyTrade": "", "companyCharacter": "",
		"feedbackRation": "101",
		"companySize": "", "companyAddr": "", "companyIntro": "",
		"businessScope": "", "companyType": "", "creditCode": "",
		"estiblishDate": "1800-10-01", "operatingStatus": "", "orgNumber": "",
		"regAddress": "", "regAuthority": "", "regCapital": "",
		"teamTime": "", "entUrl": "", "companyDetailUrl": "",
		"Update_Name": "", "Update_Time": ""
	}
	jobInfoDict = {
			"Job_ID": "", "jobTitle": "", "jobSubTitle": "", "jobSalary": "",
			"applyNum": "0", "resumeReadPercent": "101", "browserNum": "",
			"jobWelfare": "", "jobRequirement": "",  "jobAddr": "",
			"jobDescription": "", "jobCity": "", "Update_Name": "", "Update_Time": ""
		}
	CJRelationDict = {
		"Company_ID": "", "Job_ID": "", "jobUpdateTime": "",
		"needNumber": "", "jobDetailUrl": "",
		"Update_Name": "", "Update_Time": ""
	}
	test = ['company', "recruitment", "issue"]
	generateInsertCommand(jobInfoDict, test[1])
