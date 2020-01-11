# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2018-12-16 14:20:11
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2018-12-30 01:24:35

from tools import binExtend, spiltListToN

class applicationLayer(object):
	"""
	应用层：聊天室
	
	"""
	def __init__(self):
		super(applicationLayer, self).__init__()
		self.outEncodeData = ''
		# self.outDecodeData = ''

	def appEncode(self, inputData):
		data = inputData
		for d in data:
			ordData = ord(d)
			binData = binExtend(ordData, 16)
			self.outEncodeData += binData
		return self.outEncodeData
	def appDecode(self, inputData):
		outDecodeDataL = spiltListToN(inputData, 16)
		outDecodeData = ''
		for od in outDecodeDataL:
			outDecodeData+=chr(int(od, 2))
		return outDecodeData
if __name__ == '__main__':
	inputData = '我的'
	# inputData = json.dumps(inputData)
	app = applicationLayer()
	a = app.appEncode(inputData)
	print(a)
	b = app.appDecode(a)
	print(b)
	print(b == inputData)