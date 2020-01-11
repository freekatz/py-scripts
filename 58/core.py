#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   core.py
@Desc    :
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/4/10 20:31   thefreer      1.0
'''
import requests
import re
import json
import time
from bs4 import BeautifulSoup

from setting import NAME, User_Agent, CITY

headers = {
	"User-Agent": User_Agent,
}

def getAjaxData1(jobId, companyId):
	url = "http://statisticszp.58.com/position/totalcount/?infoId=%s&userId=%s"\
		% (jobId, companyId)
	resp = requests.get(url=url, headers=headers)
	html = resp.text[9:-2]
	js = json.loads(html)
	applyNum = js["deliveryCount"]
	# print(applyNum)
	resumeReadPercent = js["resumeReadPercent"] # 简历阅读百分比
	positionTotal = js["infoCount"]
	if applyNum == "" or applyNum == None:
		applyNum = 0
	if resumeReadPercent == "-1" or resumeReadPercent == None or resumeReadPercent == -1:
		resumeReadPercent = 0
		
	return applyNum, resumeReadPercent, positionTotal

def getAjaxData2(companyId):
	url = "https://jianli.58.com/ajax/getefrate/%s" % companyId
	resp = requests.get(url=url, headers=headers)
	html = resp.text
	js = json.loads(html)
	feedbackRation = js["entity"]["efrate"]
	if feedbackRation == "-1" or feedbackRation == None or feedbackRation == -1:
		feedbackRation = 0
	return feedbackRation

def searchList(area, index):
	# url = "https://%s.58.com/%s/pn%s/?key=%s&final=1&jump=1" % (city, area, index, kw)
	url = "https://%s.58.com/%s/pn%s/" % (CITY, area, index)
	resp = requests.get(url, headers=headers)
	html = resp.text
	soup = BeautifulSoup(html, "lxml")
	items = soup.select("li.job_item")
	companyBaseUrlList = []
	companyIdList = []
	for item in items:
		flag = True
		try:
			icons = item.select("i")
			for icon in icons:
				if flag != True:
					continue
				if icon["class"] == "edu_label":
					print("培训机构，跳过")
					flag = False
		except:
			pass
		resultItem = item.select_one("div.job_comp")
		cbUrl = resultItem.select_one("div.comp_name")
		inp = resultItem.input
		try:
			icon = cbUrl.select_one("i")
			if flag != True:
				continue
			if "pxdz" in icon["class"]:
				print("培训机构，跳过")
				flag = False
			elif "mingqi" in icon["class"]:
				print("名企，跳过")
				flag = False
			else:
				flag = True
		except:
			pass
		if flag != True:
			continue
		a = cbUrl.a
		companyBaseUrl = a["href"]
		companyId = re.split(r"_", inp["uid"])[0]
		companyBaseUrlList.append(companyBaseUrl)
		companyIdList.append(companyId)
	return companyBaseUrlList, companyIdList

def getCompanyJobList(companyId, index=1, jobList=[]):
	url = "https://qy.58.com/ent/infolist/%s/{}".format(index) % companyId
	resp = requests.get(url, headers=headers)
	js = json.loads(resp.text)
	tempList = js["data"]["infoList"]
	positionTotal = js["data"]["total"]
	# if int(positionTotal) < (index + 2) * 10 and index > 2:
	# 	print("!!!!!!!!职位过多，跳过")
	# 	return [], 0
	if tempList != []:
		print("此公司共有 %s 个职位, 当前爬取 %s 页" % (positionTotal, str(index)))
		return getCompanyJobList(companyId, index=index+1, jobList=jobList+tempList)
	else:
		print("爬取公司职位列表完成")
		return jobList, positionTotal

# def getCompanyBaseUrl(jobDetailUrl):
# 	resp = requests.get(url=jobDetailUrl, headers=headers)
# 	html = resp.text
# 	soup = BeautifulSoup(html, "lxml")
# 	try:
# 		companyBaseUrl = soup.select_one("div.baseInfo_link").a["href"].replace("https", "http")
# 	except:
# 		companyBaseUrl = soup.select_one("a.baseInfo_daipei")["href"].replace("https", "http")
# 	return companyBaseUrl

def parseJobDetail(jobDetailUrl, jobDetailId):
	# print(jobDetailUrl)
	# print(jobDetailId)
	resp = requests.get(url=jobDetailUrl, headers=headers)
	html = resp.text
	soup = BeautifulSoup(html, "lxml")
	# 职位名字
	title = soup.select_one("span.pos_title").text
	# 子标题，一般为对职位的一些概括或者是说明职位的部分信息，如薪资
	subTitle = soup.select_one("span.pos_name").text
	# 职位薪资
	salary = soup.select_one("span.pos_salary").text
	# 公司简要链接
	companyBaseUrl = soup.select_one("div.baseInfo_link").a["href"]
	# 公司 ID
	companyId = re.search(r"qy.58.com/(.*?)/", companyBaseUrl).groups()[0]
	# 申请人数、反馈率、公司共发布职位数
	applyNum, resumeReadPercent, _ = getAjaxData1(jobDetailId, companyId)
	browserNum = soup.select_one("span.pos_base_browser").text # 浏览数目
	# 更新时间
	# updateTime = soup.select_one("span.pos_base_update").text.replace(" ", "")
	# 福利列表，类似于：['包住', '加班补助', '饭补']
	welfareItems = [w.text for w in soup.select("span.pos_welfare_item")]
	# welfare = json.dumps({"items": welfareItems})
	welfare = "_".join(welfareItems)
	# 类似于：['招1人', '学历不限', '经验不限']
	conditionItems = [c.text.replace(" ", "") for c in soup.select("span.item_condition")]
	# needNum = conditionItems[0] # 职位需要人数
	# condition = json.dumps({"items": conditionItems[1:]})
	condition = "_".join(conditionItems[1:])
	areaTemp = [a for a in re.split(r" ", soup.select_one("div.pos-area").text)]
	areaItems = [] # 地域信息，很详细
	for at in areaTemp:
		if at != " " and at != "-" and at != "" and at != "查看地图":
			areaItems.append(at)
	# area = json.dumps({"items": areaItems})
	area = "_".join(areaItems)
	description = soup.select_one("div.des").text # 职位描述，一般包括职位要求
	# requirements = soup.select_one("div.requirements").text # 职位要求，一般为空
	InfoList = [
		title, subTitle, salary, applyNum,
		resumeReadPercent, browserNum,
		welfare, condition, area, description
	]
	return InfoList

def parseComDetail1(companyBaseUrl, companyId):
	resp = requests.get(url=companyBaseUrl, headers=headers)
	html = resp.text
	soup = BeautifulSoup(html, "lxml")
	baseMsg = soup.select_one("div.basicMsg").text
	companyName = soup.select_one("a.businessName").text # 公司名字
	try:
		tradeItems = [t.replace(" ", "") for t in re.search(r"公司行业：(.*?)、(.*?)\n", baseMsg).groups()]
	except:
		tradeItems = ["其他行业"] # 公司行业
	# companyTrade = json.dumps({"items": tradeItems})
	companyTrade = "_".join(tradeItems)
	# 公司性质：私营、国企等
	companyCharacter = re.sub(r" |\t|\r|\n", "", re.search(r"公司性质：(.*?)\n", baseMsg).groups()[0])
	if companyCharacter == None or companyCharacter == "":
		companyCharacter = "无性质"
	companySize = re.search(r"公司规模：(.*?)人", baseMsg).groups()[0] # 公司规模
	companyAddr = re.search(r"公司地址：(.*?)查看地图", baseMsg, re.DOTALL).groups()[0] # 公司地址
	# 公司详情网址，可能和简要网址一样
	companyDetailUrl = re.search(r"企业网址：(.*?)\n", baseMsg).groups()[0]
	companyIntro = soup.select_one("div.compIntro").text.replace(" ", "") # 公司介绍
	postData = {
		"userName": companyName,
	}
	comJsonUrl = "http://qy.58.com/ajax/getBusinessInfo"
	cresp = requests.post(url=comJsonUrl, headers=headers, data=postData)
	chtml = cresp.text
	js = json.loads(chtml)
	businessScope = js["businessScope"] # 经营范围
	companyType = js["companyType"] # 公司类型：有限责任公司等等
	creditCode = js["creditCode"] # 统一社会信用代码
	estiblishDate = js["estiblishDate"] # 成立日期
	if estiblishDate == None or estiblishDate == "":
		estiblishDate = "1800-12-31"
	operatingStatus = js["operatingStatus"] # 经营状态
	orgNumber = js["orgNumber"] # 组织机构代码
	regAddress = js["regAddress"] # 注册地址
	regAuthority = js["regAuthority"] # 重庆市工商行政管理局南岸区分局
	regCapital = js["regCapital"] # 注册资本
	teamTime = js["termStart"] + "_" + js["teamEnd"] # 经营期限
	entUrl = js["entUrl"] # 天眼查网址
	feedbackRation = getAjaxData2(companyId)
	infoList = [
		companyName, companyTrade, companyCharacter, companySize,
		companyAddr, companyIntro, businessScope, companyType, creditCode,
		estiblishDate, operatingStatus, orgNumber, regAddress,
		regAuthority, regCapital, teamTime, entUrl, companyDetailUrl,
		feedbackRation
	]
	return infoList

def parseComDetail2(companyId):
	url = "http://qy.58.com/ent/detail/%s" % companyId
	resp = requests.get(url=url, headers=headers)
	html = resp.text
	js = json.loads(html)
	detail = js["data"]["entDetail"]
	companyName = detail["entName"] # 公司名字
	companySize = detail["sizeText"] # 公司行业
	companyIntro = detail["introduction"]
	companyCharacter = detail["typeText"] # 公司性质：私营、国企等
	if companyCharacter == None or companyCharacter == "":
		companyCharacter = "无性质"
	bussiness = detail["bussiness"]
	regCapital = bussiness["regCapital"] # 注册资本
	businessScope = bussiness["businessScope"] # 经营范围
	creditCode = bussiness["creditCode"] # 统一社会信用代码
	orgNumber = bussiness["orgNumber"] # 组织机构代码
	regAddress = bussiness["regLocation"] # 注册地址
	operatingStatus = bussiness["regStatus"] # 经营状态
	estiblishDate = bussiness["createTime"] # 成立日期
	if estiblishDate == None:
		estiblishDate = "1800-12-31"
	companyAddr = detail["address"] # 公司地址
	teamTime = "_" # 经营期限
	regAuthority = "未知" # 重庆市工商行政管理局南岸区分局
	companyTrade = "未知" # 公司行业
	companyType = "未知" # 公司类型：有限责任公司等等
	entUrl = "未知" # 天眼查网址
	companyDetailUrl = "未知" # 公司详情网址，可能和简要网址一样
	feedbackRation = getAjaxData2(companyId)
	infoList = [
		companyName, companyTrade, companyCharacter, companySize,
		companyAddr, companyIntro, businessScope, companyType, creditCode,
		estiblishDate, operatingStatus, orgNumber, regAddress,
		regAuthority, regCapital, teamTime, entUrl, companyDetailUrl,
		feedbackRation
	]
	return infoList

def coreMain(companyBaseUrl, companyId):
	resultList = []
	# companyId = re.search(r"(.*)/(\d*)/", companyBaseUrl).groups()[1]
	try:
		comInfoList = parseComDetail1(companyBaseUrl, companyId)
	except:
		try:
			comInfoList = parseComDetail2(companyId)
		except:
			return []
	if comInfoList == []:
		return []
	# 招聘与公司联系集表
	companyJobList, positionTotal = getCompanyJobList(companyId)
	if companyJobList == []:
		return []
	# 公司信息表
	companyInfoDict = {
		"Company_ID": "", "positionTotal": "0", "companyBaseUrl": "",
		"companyName": "", "companyTrade": "", "companyCharacter": "",
		"feedbackRation": "101",
		"companySize":"", "companyAddr": "", "companyIntro": "",
		"businessScope": "", "companyType": "", "creditCode": "",
		"estiblishDate": "1800-10-01", "operatingStatus": "", "orgNumber": "",
		"regAddress": "", "regAuthority": "", "regCapital": "",
		"teamTime": "", "entUrl": "", "companyDetailUrl": "",
		"Update_Name":"", "Update_Time": ""
	}
	companyInfoDict["Company_ID"] = companyId
	companyInfoDict["positionTotal"] = positionTotal
	companyInfoDict["companyBaseUrl"] = companyBaseUrl
	companyInfoDict["companyName"] = comInfoList[0]
	companyInfoDict["companyTrade"] = comInfoList[1]
	companyInfoDict["companyCharacter"] = comInfoList[2]
	companyInfoDict["companySize"] = comInfoList[3]
	companyInfoDict["companyAddr"] = comInfoList[4]
	companyInfoDict["companyIntro"] = comInfoList[5]
	companyInfoDict["businessScope"] = comInfoList[6]
	companyInfoDict["companyType"] = comInfoList[7]
	companyInfoDict["creditCode"] = comInfoList[8]
	companyInfoDict["estiblishDate"] = comInfoList[9]
	companyInfoDict["operatingStatus"] = comInfoList[10]
	companyInfoDict["orgNumber"] = comInfoList[11]
	companyInfoDict["regAddress"] = comInfoList[12]
	companyInfoDict["regAuthority"] = comInfoList[13]
	companyInfoDict["regCapital"] = comInfoList[14]
	companyInfoDict["teamTime"] = comInfoList[15]
	companyInfoDict["entUrl"] = comInfoList[16]
	companyInfoDict["companyDetailUrl"] = comInfoList[17]
	companyInfoDict["Update_Name"] = NAME
	Update_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	companyInfoDict["Update_Time"] = Update_Time
	companyInfoDict["feedbackRation"] = comInfoList[18]
	resultList.append(companyInfoDict)
	# print(companyInfoDict)
	i = 0
	for job in companyJobList:
		i+=1
		print("————————|—————%s-%s—————|————————" % (companyInfoDict["companyName"], str(i)))
		jobDetailUrl = job["url"]
		jobDetailId = re.search(r"(.*)/(\d*)", jobDetailUrl).groups()[1]
		# 联系集
		CJRelationDict = {
			"Company_ID": "", "Job_ID": "", "jobUpdateTime": "",
			"needNumber": "0", "jobDetailUrl": "",
			"Update_Name": "", "Update_Time": ""
		}
		CJRelationDict["Company_ID"] = companyId
		CJRelationDict["Job_ID"] = jobDetailId
		CJRelationDict["jobUpdateTime"] = job["postDate"]
		CJRelationDict["needNumber"] = job["nubmer"]
		CJRelationDict["jobDetailUrl"] = jobDetailUrl
		CJRelationDict["Update_Name"] = NAME
		Update_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		CJRelationDict["Update_Time"] = Update_Time
		# print(CJRelationDict)
		# 招聘表
		jobInfoDict = {
			"Job_ID": "", "jobTitle": "", "jobSubTitle": "", "jobSalary": "",
			"applyNum": "0", "resumeReadPercent": "101", "browserNum": "",
			"jobWelfare": "", "jobRequirement": "",  "jobAddr": "",
			"jobDescription": "", "jobCity": "", "Update_Name": "", "Update_Time": ""
		}
		try:
			jobInfoList = parseJobDetail(jobDetailUrl, jobDetailId)
		except:
			return False
		jobInfoDict["Job_ID"] = jobDetailId
		jobInfoDict["jobTitle"] = jobInfoList[0]
		jobInfoDict["jobSubTitle"] = jobInfoList[1]
		jobInfoDict["jobSalary"] = jobInfoList[2]
		jobInfoDict["applyNum"] = jobInfoList[3]
		jobInfoDict["resumeReadPercent"] = jobInfoList[4]
		jobInfoDict["browserNum"] = jobInfoList[5]
		jobInfoDict["jobWelfare"] = jobInfoList[6]
		jobInfoDict["jobRequirement"] = jobInfoList[7]
		jobInfoDict["jobAddr"] = jobInfoList[8]
		jobInfoDict["jobDescription"] = jobInfoList[9]
		jobInfoDict["jobCity"] = CITY
		jobInfoDict["Update_Name"] = NAME
		Update_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		jobInfoDict["Update_Time"] = Update_Time
		# print(jobInfoDict)
		resultList.append([jobInfoDict, CJRelationDict])
	return resultList
	

if __name__ == '__main__':
	city = "bj"
	index = "1"
	sl = searchList(city, "job", index)
	print(sl)
