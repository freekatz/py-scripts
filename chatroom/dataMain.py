# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2018-12-16 14:18:55
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2019-01-04 15:20:58
from tools import spiltListToN, binExtend
from layers.applicationLayer import applicationLayer
from layers.transferLayer import transferLayer
from layers.networkLayer import networkLayer
from layers.linkLayer import linkLayer
from layers.physicalLayer import physicalLayer

applicationLayer = applicationLayer()
transferLayer  = transferLayer()
networkLayer = networkLayer()
linkLayer = linkLayer()
physicalLayer = physicalLayer()


def init():
	applicationLayer.__init__()
	transferLayer.__init__()
	networkLayer.__init__()
	linkLayer.__init__()
	physicalLayer.__init__()

def dataPack(inputData):
	print("====应用层====")
	appEncodeData = applicationLayer.appEncode(inputData)
	print("应用层编码得到：\n%s" % appEncodeData)
	print("====传输层====")
	tranEncodeData = transferLayer.tranEncode(appEncodeData)
	print("传输层编码得到：\n%s" % tranEncodeData)
	print("====网络层====")
	netEncodeData = networkLayer.netEncode(tranEncodeData)
	print("网络层编码得到：\n%s" % netEncodeData)
	print("====链路层====")
	linkEncodeData = linkLayer.linkEncode(netEncodeData)
	print("链路层编码得到：\n%s" % linkEncodeData)
	print("====物理层====")
	phyEncodeData = physicalLayer.phyEncode(linkEncodeData)
	print("物理层编码得到：\n%s" % phyEncodeData)
	print("\n==============\n")
	return phyEncodeData


def dataUnpack(inputData):
	print("====物理层====")
	phyDecodeData = physicalLayer.phyDecode(inputData)
	print("物理层解码得到：\n%s"%phyDecodeData)
	print("====传输层====")
	linkDecodeData = linkLayer.linkDecode(phyDecodeData)
	print("链路层解码得到：\n%s"%linkDecodeData)
	print("====传输层====")
	netDecodeData = networkLayer.netDecode(linkDecodeData)
	print("网络层解码得到：\n%s"%netDecodeData)
	print("====传输层====")
	tranDecodeData = transferLayer.tranDecode(netDecodeData)
	print("传输层解码得到：\n%s"%tranDecodeData)
	print("====应用层====")
	appDecodeData = applicationLayer.appDecode(tranDecodeData)
	print("应用层解码得到：\n%s"%appDecodeData)
	print("\n=============\n")
	return appDecodeData

if __name__ == '__main__':
	# inputData = ''
	while 1:
		applicationLayer.__init__()
		transferLayer.__init__()
		networkLayer.__init__()
		linkLayer.__init__()
		physicalLayer.__init__()
		inputData = input("in:")
		a = dataPack(inputData)
		print(a)
		b = dataUnpack(a)
		print(b)
		print(inputData==b)
	# print(dataUnpack('011111101010101010101010101010101010101010101010101010101010101010101011111011111011111011111011111011111011111011111011111011111000000000000110111110111001001101010100100000000000000000101101000010001011010010000000101001100000000000000000000010000000000000001111101100000110111101001111000101010000001100000101000001101010000010100000011010000001101000000100011010001100011000011110110000000000000000000000000000000001000000000000000000000000000000100101000000010010000000000010100010100110111010100000000000000000011010000110100001101000011010000110100000010101001000111110010010100011101111110'))
