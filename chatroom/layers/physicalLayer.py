# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2018-12-16 14:24:26
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2018-12-30 12:08:43
import re
class physicalLayer(object):
	"""
	将输入的由链路层传来的消息一块一块（此代码并没有分块，因为还没写链路层）的调制为bit流，主要是数字调制:
	encode将输入字符转化为ASCII码，再将ASCII码转化为2进制BCD，并且加上头部;
	decode 去掉2进制中的头部.

	"""
	def __init__(self):
		super(physicalLayer, self).__init__()
		self.outEncodeData =''
		# self.outDecodeData = []

	def phyEncode(self, inputData):
		for i in range(len(inputData)):
			outEncodeData = inputData[i]
			self.outEncodeData+=outEncodeData
		return self.outEncodeData

	def phyDecode(self, inputData):
		inputDataList = re.split(r'01111110', inputData)
		outDecodeDataL = []
		for li in inputDataList:
			if li != '':
				outDecodeData = '01111110' + li + '01111110'
				outDecodeDataL.append(outDecodeData)
		return outDecodeDataL

if __name__ == '__main__':
	physicalLayer = physicalLayer()
	data = ['011111101010101010101010101010101010101010101010101010101010101010101011111011111011111011111011111011111011111011111011111011111000000000000110111110111001001101010100100000000000000000101101000010001011010010000000101001100000000000000000000010000000000000001111101100000110111101001111000101010000001100000101000001101010000010100000011010000001101000000100011010001100011000011110110000000000000000000000000000000001000000000000000000000000000000100101000000010010000000000010100010100110111010100000000000000000011010000110100001101000011010000110100000010101001000111110010010100011101111110']
	enData = physicalLayer.phyEncode(data)
	deData = physicalLayer.phyDecode(enData)
	print(enData)
	print(data == deData)