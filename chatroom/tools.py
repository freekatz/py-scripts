# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2018-12-16 14:17:29
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2018-12-30 16:21:45

import crcmod.predefined
import re
def spiltListToN(List, n):
	newList = []

	for i in range(0, len(List), n):
		newList.append(List[i:i + n])
	return newList

def binExtend(List, n):
	List = bin(List).replace('0b', '')
	if len(List)<n:
		for i in range(n-len(List)):
			List = '0' + List
	return List

def crc(Bin, c):
	b2h = bytes(hex(int(Bin, 2)), 'utf-8')
	if c == 8:
		crcCmd = 'crc-8-maxim'
	elif c == 16:
		crcCmd = 'crc-16-maxim'
	elif c == 32:
		crcCmd = 'crc-32'
	C = crcmod.predefined.Crc(crcCmd)
	C.update(b2h)
	binC = binExtend(C.crcValue, c)
	return binC
def fillZero(inputData):#1
	tmpList = re.split('11111', inputData)
	# print(tmpList)
	out = ''
	for i in range(len(tmpList)-1):
		out = out + tmpList[i] + '111110'
	out = out + tmpList[-1]
	return out
def freeZero(inputData):#1
	tmpList = re.split('111110', inputData)
	out = ''
	for i in range(len(tmpList)-1):
		out = out + tmpList[i] + '11111'
	out = out + tmpList[-1]
	return out


