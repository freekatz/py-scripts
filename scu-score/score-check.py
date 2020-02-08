#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import requests
import random
import time

import zmail # pip install zmail

'''
出分的前两天没准会提前开放接口用于测试，如果我们一直请求这个接口，那么就可能可以提前查到分数
本程序的查分原理是：利用验证码错误的响应判断查分接口是否开启，所以查分还是需要手动，本程序只用来监控接口是否开启
建议将本程序在云服务器中进行运行，有没有 Bug 没测试过，当成个心理安慰也不错
'''

if __name__ == "__main__":
	server = zmail.server('yoursendemailusr', 'yoursendmailpwd') # 用于发送出分通知的邮箱账户和密码，建议使用 outlook 邮箱
	mail = {
	    'subject': '出分了！',  
	    'content_text': '', 
	}
	
	idnum = '' # 身份证号
	name = ''.encode('utf-8') # 名字
	vcode = "L626" # 随便填一个四位的字母和数字， 建议不用改
	cnum = '' # 考号 15 位

	url = "https://yz.scu.edu.cn/score/Query/--"
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
		'Referer': 'https://yz.scu.edu.cn/score',
		'Content-type': 'application/x-www-form-urlencoded'
	}
	payload = 'zjhm=%s&xm=%s&vcode=%s&ksbh=%s' % (idnum, name, vcode, cnum)
	
	while True: # 保证程序是一直运行的
		time.sleep(random.randint(60, 120)) # 每隔 1 至 2 分钟查分一次
		resp = requests.post(url=url, headers=headers, data=payload)
		score = resp.text
		# 如果接收到的电子邮件内容为：验证码错误等其他有用信息，那就是出分了，请快速前往官网查分
		if "不在可查询时间范围内" not in score: 
			mail['content_text'] = score
			server.send_mail('yourreceiveemailusr', mail) # 如果出分了则发送电子邮件给这个账户
			print("发送成功")
		
		