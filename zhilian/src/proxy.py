#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   proxy.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/16 15:16   thefreer      1.0         
'''
import requests

import sys
from multiprocessing import Process

sys.path.append('.')
sys.path.append('..')

from src.Proxy.Api.ProxyApi import run as ProxyApiRun
from src.Proxy.Schedule.ProxyValidSchedule import run as ValidRun
from src.Proxy.Schedule.ProxyRefreshSchedule import run as RefreshRun


def run():
	p_list = list()
	p1 = Process(target=ProxyApiRun, name='ProxyApiRun')
	p_list.append(p1)
	p2 = Process(target=ValidRun, name='ValidRun')
	p_list.append(p2)
	p3 = Process(target=RefreshRun, name='RefreshRun')
	p_list.append(p3)
	
	for p in p_list:
		p.daemon = True
		p.start()
	for p in p_list:
		p.join()

def get_proxy():
	return requests.get("http://127.0.0.1:5010/get/").content.decode()

def del_proxy(proxy):
	requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

if __name__ == '__main__':
	run()
