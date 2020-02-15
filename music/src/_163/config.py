#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py    
@Desc    :   
@Project :   zapis
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2020, ZJH
@WebSite :   zjh567.cn
@Modify Time           @Author        @Version
------------           -------        --------
2020/01/30 11:40       ZJH            1.0         
'''
# 常量
headers = {
    # 'Host': 'm8c.music.126.net',
    'User-Agent':
    'NeteaseMusic/5.8.3.1548335430(135);Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A5010 Build/PKQ1.180716.001)',
    # 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Referer':
    'http://music.163.com/',
    'Content-Type':
    'application/x-www-form-urlencoded',
}
post_url = 'https://music.163.com/weapi/song/enhance/player/url'
content = {"ids": "", "br": 999000, "csrf_token": ""}
key1 = b'0CoJUm6Qyw8W8jud'
key2 = b'ryPnuAVT5RtiIWNi'
encSecKey = 'a71973af53caae445b554150da52e75ba5687609d28013aacea03e9ef07169560f156ca76be9ac8df7bb204e05b864756aa3dd2274a65d5be964f118f6d075006695059e10cdcc806306e9a5f2f36f5bf0379f511cd13a600a6cc7031c814583863ea84d3373dea69f74354cd2dc3af61d58eeb43b1de06f588ef361ebc1eed6'
iv = b'0102030405060708'