from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from ui.client_mainwindow import Ui_MainWindow
import sys
import subprocess

class CThread(QThread):
	cOut = pyqtSignal(str)
	def __init__(self):
		super().__init__()

	def run(self):
		client = subprocess.Popen("python client.py", shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
		# client = subprocess.Popen("python client.py", stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
		while True:
			line = client.stdout.readline()
			line = line.decode("utf-8", 'ingore')
			# print(line)
			self.cOut.emit(line)
			# time.sleep(3)
			if subprocess.Popen.poll(client) == 0:  # 判断子进程是否结束
				break


class CMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(CMainWindow, self).__init__(parent)
		self.setupUi(self)
		# self.Title.setText("聊天室")
		# self.connServer.clicked.connect(self.connectServer)
		# 连接开始按钮和槽函数
		self.connServer.clicked.connect(self.clientStart)
		# 创建新线程，将自定义信号sinOut连接到slotAdd()槽函数
		self.cThread = CThread()
		self.cThread.cOut.connect(self.connectServer)

	# 开始按钮按下后使其不可用，启动线程
	def clientStart(self):
		self.connServer.setEnabled(False)
		self.cThread.start()
	def connectServer(self, text):
		self.msgEdit.append(text)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = CMainWindow()
	mainWindow.show()
	sys.exit(app.exec_())