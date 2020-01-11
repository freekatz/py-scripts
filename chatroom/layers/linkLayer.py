# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2018-12-27 14:33:11
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2019-01-04 15:21:59
from tools import spiltListToN, binExtend, crc, fillZero, freeZero
import re

class linkLayer(object):
	"""
	使用802.3协议 
	"""
	def __init__(self):
		super(linkLayer, self).__init__()
		self.outEncodeData = []
		# self.outDecodeData = []
		self.priCode = '10101010'*7
		self.SoF = '10101011'
		self.oriMac = 'ffffffffffff'
		self.toMac = '001bfc9aa400'
		self.fill = '2'
		self.linkHeaderDict = {}
		self.linkHeader = []
		self.linkTailDict = {}
		self.linkTail = []

	def linkEncode(self, inputData):
		oriAddrList = spiltListToN(self.oriMac, 2)
		oriMacT = ''
		for a in oriAddrList:
			oriMacT+=binExtend(int(a, 16), 8)
		toAddrList = spiltListToN(self.toMac, 2)
		toMacT = ''
		for t in toAddrList:
			toMacT+=binExtend(int(t, 16), 8)
		for li in inputData:
			linkHeader = ''
			linkTail = ''
			length = len(li)
			data = li
			lengthT = binExtend(length,16)
			checkSumT = crc(li, 32)
			self.linkHeaderDict = {
				'priCode':self.priCode,
				'SoF':self.SoF,
				'oriMac':oriMacT,
				'toMac':toMacT,
				'length':lengthT
			}
			print("加入帧头部信息：")
			print(self.linkHeaderDict)
			for liH in self.linkHeaderDict:
				linkHeader+=self.linkHeaderDict[liH]
			self.linkHeader.append(linkHeader)
			outEncodeData = linkHeader + data
			self.linkTailDict = {
				'checkSum':checkSumT
			}
			self.linkTailDict = {
				'checkSum':checkSumT
			}
			print("加入帧尾部信息")
			print(self.linkTailDict)
			for liT in self.linkTailDict:
				linkTail+=self.linkTailDict[liT]
			self.linkTail.append(linkTail)
			outEncodeData = outEncodeData + linkTail
			outEncodeData = '01111110' + fillZero(outEncodeData) + '01111110'
			print("对数据进行0填充，并再次加入头部'01111110':")
			print(outEncodeData)
			self.outEncodeData.append(outEncodeData)
		return self.outEncodeData
	def linkDecode(self, inputData):
		outDecodeDataL = []
		for li in inputData:
			outDecodeData = re.split('01111110',li)[1]
			outDecodeData = freeZero(outDecodeData)
			outDecodeData = outDecodeData[22*8:-32].replace(self.fill, '')
			outDecodeDataL.append(outDecodeData)
		return outDecodeDataL





if __name__ == '__main__':
	link = linkLayer()
	data = ['010001011010010000000101001100000000000000000000010000000000000001111111000001101111010011110001010100000011000001010000011010100000101000000110100000011010000001000110100011000110000111101100000000000000000000000000000000010000000000000000000000000000001001010000000100100000000000101000101001101110101000000000000000000110100001101000011010000110100001101000']

	enData = link.linkEncode(data)
	print(enData)
	deData = link.linkDecode(enData) 
	print(deData)
	print(data == deData)
	# print(len('10101010101010101010101010101010101010101010101010101010101010111111111111111111111111111111111111111111111111110000000000011011111111001001101010100100000000000000000000001101'))