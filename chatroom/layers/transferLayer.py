# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2018-12-16 14:16:24
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2019-01-04 15:21:37

import random
from tools import binExtend, spiltListToN, crc

class transferLayer(object):
	"""
	网络层，加上TCP头
	"""
	def __init__(self):
		super(transferLayer, self).__init__()
		# self.outEncodeData = ''
		self.outEncodeData = []
		# self.outDecodeData = ''
		self.segSize = 146*8
		self.tcpHeader = []
		self.tcpHeaderDict = {}
	def tranEncode(self, inputData):
		listOfData = spiltListToN(inputData, self.segSize)
		print('数据被分为:')
		print(listOfData)
		oriPort = random.randint(1, 25555)
		toPort = random.randint(1, 25555)
		index = 0
		lenOfTCP = 5
		tagDict = {
			'CWR':0,
			'ECE':0,
			'URG':0,
			'ACK':0,
			'PSH':0,
			'RST':0,
			'SYN':0,
			'FIN':0
			}
		urgPointer = 0
		options = None
		for li in listOfData:
			tcpHeader = ''
			oriPortT = binExtend(oriPort, 16)
			toPortT = binExtend(toPort, 16)
			index+=1
			indexT = binExtend(index, 32)
			yesIndex = index + 1
			yesIndexT = binExtend(yesIndex, 32)
			lenOfTCPT = binExtend(lenOfTCP, 4)
			tagDict['ACK'] = 1
			tagDict['SYN'] = 1
			tag = ''
			for t in tagDict:
				tag+=str(tagDict[t])
			sizeOfWin = len(li)
			sizeOfWinT = binExtend(sizeOfWin, 16)
			checkSumT = crc(li, 16)
			urgPointerT = binExtend(urgPointer, 16)
			self.tcpHeaderDict = {
				'oriPort':oriPortT,
				'toPort':toPortT,
				'index':str(indexT),
				'yesIndex':str(yesIndexT),
				'lenOfTCP':str(lenOfTCPT),
				'blank':'0000',
				'tag': str(tag),
				'sizeOfWin':str(sizeOfWinT),
				'checkNum':str(checkSumT),
				'urgPointer':str(urgPointerT),
				# 'options':str(options),
			}
			print('加入tcp头部信息')
			print(self.tcpHeaderDict)
			for tcpH in self.tcpHeaderDict:
				tcpHeader += self.tcpHeaderDict[tcpH]
			self.tcpHeader.append(tcpHeader)
			outEncodeData = tcpHeader + li
			self.outEncodeData.append(outEncodeData)
		return self.outEncodeData
	def tranDecode(self, inputData):
		outDecodeData = ''
		for i in range(len(inputData)):
			lenOfTcpH = 160
			tmpData = inputData[i][lenOfTcpH:]
			outDecodeData+=tmpData
		return outDecodeData
		
if __name__ == '__main__':
	inputData = '010110010001011100110001101100100000000000000000000000000000000100000000000000000000000000000010010100000001001000000000110010000001100000000111000000000000000000001111001101010010100010100001000000000000000000000000000000010000000000000000000000000000001001010000000100100000000000101000101001101110101000000000000000000110100001101000011010000110100001101000'
	# inputData = json.dumps(inputData)
	app = transferLayer()
	a = app.tranEncode(inputData)
	print(a)
	b = app.tranDecode(a)
	print(b == inputData)
