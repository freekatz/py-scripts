# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2018-12-16 14:23:55
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2019-01-04 15:21:12
import random
from tools import binExtend, crc
class networkLayer(object):
	"""
	networkLayer:ip package ipv4
	"""
	def __init__(self):
		super(networkLayer, self).__init__()
		self.outEncodeData = []
		# self.outDecodeData = []
		self.pacSize = 146*8 + 32*5
		self.ipHeaderDict = {}
		self.ipHeader = []

	def netEncode(self, inputData):
		version = 4
		IHL = 5
		diffServices = '10100100'#3 1 1 1 2
		totalLength = self.pacSize
		identification = 0
		blank = '0'
		DF = '1'
		MF = '0'
		fragOffset = 0*8
		liveTime = 127
		protocol = 6
		oriIP = [
			random.randint(1, 255),
			random.randint(1, 255),
			random.randint(1, 255),
			random.randint(1, 255)
			]
		toIP = [
			random.randint(1, 255),
			random.randint(1, 255),
			random.randint(1, 255),			
			random.randint(1, 255)
			]
		options = None
		for li in inputData:
			ipHeader = ''
			versionT = binExtend(version, 4)
			IHLT = binExtend(IHL, 4)
			totalLengthT = binExtend(totalLength, 16)
			identificationT = binExtend(identification, 16)
			fragOffsetT = binExtend(fragOffset, 13)
			liveTimeT = binExtend(liveTime, 8)
			protocolT = binExtend(protocol, 8)
			checkSumT = crc(li, 16)
			oriIPT = ''
			toIPT = ''
			for o in oriIP:
				oriIPT+=binExtend(o, 8)
			for t in toIP:
				toIPT+=binExtend(t, 8)
			self.ipHeaderDict = {
				'version':versionT,
				'IHL':IHLT,
				'diffServices':diffServices,
				'totalLength':totalLengthT,
				'identification':identificationT,
				'blank':blank,
				'DF':DF,
				'MF':MF,
				'fragOffset':fragOffsetT,
				'liveTime':liveTimeT,
				'protocol':protocolT,
				'checkSum':checkSumT,
				'oriIP':oriIPT,
				'toIP':toIPT,
			}
			print("加入IP头信息：")
			print(self.ipHeaderDict)
			for ipH in self.ipHeaderDict:
				ipHeader += self.ipHeaderDict[ipH]
			self.ipHeader.append(ipHeader)
			outEncodeData = ipHeader + li
			self.outEncodeData.append(outEncodeData)
		return self.outEncodeData

	def netDecode(self, inputData):
		j = 0
		outDecodeDataL = []
		for i in range(len(inputData)):
			lenOfIpH = 160
			outDecodeData = inputData[i][lenOfIpH:]
			outDecodeDataL.append(outDecodeData)
		return outDecodeDataL
if __name__ == '__main__':
	i = ['01000110100011000110000111101100000000000000000000000000000000010000000000000000000000000000001001010000000100100000000000101000101001101110101000000000000000000110100001101000011010000110100001101000']

	app = networkLayer()
	a=app.netEncode(i)
	print(a)
	b=  app.netDecode(a)
	print(b == i)

