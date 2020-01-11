#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   edx.py    
@Desc    :   CQU EDX 平台视频代看工具
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/16 17:10   thefreer      1.0         
'''
import requests
import json
import re
import time
from bs4 import BeautifulSoup

## cookies 文件存储的是网页 Header 中的 cookies，用于登录
with open("cookies.txt", "r") as f:
	cookies = f.readline()
csrftoken = re.search(r"csrftoken=(.*?);", cookies).groups()[0]
print(csrftoken)
headers = {
	"User-Agent":
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
	"Cookie":
	cookies,
	"X-CSRFToken":
	csrftoken,
}


def get_section(url):
	section_list = []
	resp = requests.get(url, headers=headers)
	html = resp.text
	soup = BeautifulSoup(html, "lxml")
	section_items = soup.select("li.section")
	for section in section_items:
		section_id = re.split(r"@", section.select_one("button.section-name")["id"])[-1]
		title = re.sub(r"\t|\n| ", "", section.select_one("h3.section-title").text)
		section_list.append((title, section_id))
	return section_list, section_items


def get_subsection(section):
	subsection_list = []
	subsection_id_items = section.select("button.subsection-text")
	subsection_items = section.select("li.subsection")
	title_items = section.select("h4.subsection-title")
	for tit, sub in zip(title_items, subsection_id_items):
		title = re.sub(r"\t|\n| ", "", tit.text)
		subsection_id = re.split(r"@", sub["id"])[-1]
		subsection_list.append((title, subsection_id))
	return subsection_list, subsection_items


def get_video_list(section):
	video_list = []
	soup = BeautifulSoup(str(section), "lxml")
	items = soup.select("a.focusable")
	for item in items:
		title = re.sub(r"\t|\n| ", "", item.findAll("div")[0].text)
		video_id = re.split(r"@", item["href"])[-1]
		video_list.append((title, video_id))
	return video_list


def play_video(id_list):
	# print(id_list)
	course_id = id_list[0]
	section_id = id_list[1]
	subsection_id = id_list[2]
	video_id = id_list[3]
	url = "http://edx.cqu.edu.cn/courses/course-v1:%s/courseware/%s/%s/1?activate_block_id=block-v1:%s+type@vertical+block@%s" % (
		course_id, section_id, subsection_id, course_id, video_id)
	# print(url)
	resp = requests.get(url, headers=headers)
	html = resp.text
	pattern = re.compile(r"videojs\+block@(.*?)&#34")
	block_id = re.findall(pattern, html)[0]
	purl = "http://edx.cqu.edu.cn/courses/course-v1:%s/xblock/block-v1:%s+type@videojs+block@%s/handler/tracking_log" % (
		course_id, course_id, block_id)
	print("开始观看视频")
	load_video = {
		"msg": "{'id': '%s', 'code': 'html5'}" % block_id,
		"type": "load_video"
	}
	resp1 = requests.post(purl, headers=headers, data=json.dumps(load_video))
	r1 = resp1.text
	print("开始加载视频")
	print(r1)
	play_video = {
		"msg": "{'id':'%s','currentTime':0,'code':'html5'}" % block_id,
		"type": "play_video"
	}
	resp2 = requests.post(purl, headers=headers, data=json.dumps(play_video))
	r2 = resp2.text
	print("开始播放视频")
	print(r2)
	time.sleep(2)
	pause_video = {
		"msg":
		"{'id':'%s','currentTime':1200.325653,'code':'html5'}" % block_id,
		"type": "pause_video"
	}
	resp3 = requests.post(purl, headers=headers, data=json.dumps(pause_video))
	r3 = resp3.text
	print("视频马上看完了")
	print(r3)
	stop_video = {
		"msg":
		"{'id':'%s','currentTime':1200.325653,'code':'html5'}" % block_id,
		"type": "stop_video"
	}
	resp4 = requests.post(purl, headers=headers, data=json.dumps(stop_video))
	r4 = resp4.text
	print("视频看完了，下一个")
	print(r4)

    # url.slice(url.lastIndexOf('@') + 1, url.indexOf('/handler'))


if __name__ == '__main__':
	url = input(
	    "请输入要你刷时长的 EDX 课程视频首页，直接回车默认为：'http://edx.cqu.edu.cn/courses/course-v1:CQU+188235-001+2018_T2/course/':\n"
	)
	if url:
		pass
	else:
		url = "http://edx.cqu.edu.cn/courses/course-v1:CQU+188235-001+2018_T2/course/"
	print("请稍等...")

	try:
		section_list, section_items = get_section(url)
		print("解析到 %d 章要看视频， 所有章标题为：" % len(section_list))
		print("=========章==========")
		for s in section_list:
			print(s[0])
	except Exception as e:
		raise e
	course_id = re.search(r"course-v1:(.*?)/", url).groups()[0]
	number = input("请输入你不想看的章(第一个就输入 1， 乱输数字后果自负)，我帮你看, 本页面全都要看请输入 all:\n")
	if number != "all":
		try:
			section = [section_items[int(number) - 1]]
			section_id = [section_list[int(number) - 1]]
			print("请稍等...")
		except Exception as e:
			raise e
	else:
		section = section_items
		section_id = section_list
		print(section_id)
	i = 0
	for sec in section:
		j = 0
		sec_id = section_id[i][1]
		subsection_list, subsection_items = get_subsection(sec)
		print("解析到本章共有 %d 小节， 开始解析节内视频：" % len(subsection_list))
		for sub in subsection_list:
			print("===============节===============")
			print(sub[0])
			subsection = subsection_items[j]
			subsection_id = sub[1]
			video_list = get_video_list(subsection)
			print("解析到本节共有 %d 个视频， 开始观看视频：" % len(video_list))
			for video in video_list:
				time.sleep(1)
				print("=====视频=====")
				print("开始观看视频：%s" % video[0])
				video_id = video[1]
				id_list = [course_id, sec_id, subsection_id, video_id]
				try:
					play_video(id_list)
				except:
					print("本页面没有视频！！跳过")
			j += 1
		i += 1
	print("恭喜你，视频看完勒")
