from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from ui.server_mainwindow import Ui_MainWindow
import sys
import subprocess

class SThread(QThread):
	sOut = pyqtSignal(str)
	def __init__(self):
		super().__init__()

	def run(self):
		server = subprocess.Popen("python server.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		while True:
			line = server.stdout.readline()
			line = line.decode("utf-8", 'ingore')
			# print(line)
			self.sOut.emit(line)
			# time.sleep(3)
			if subprocess.Popen.poll(server) == 0:  # 判断子进程是否结束
				break

class SMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(SMainWindow, self).__init__(parent)
		self.setupUi(self)
		# self.Title.setText("聊天室")
		# self.connServer.clicked.connect(self.connectServer)
		# 连接开始按钮和槽函数
		self.beginServer.clicked.connect(self.serverStart)
		# 创建新线程，将自定义信号sinOut连接到slotAdd()槽函数
		self.sThread = SThread()
		self.sThread.sOut.connect(self.begServer)

	def serverStart(self):
		self.beginServer.setEnabled(False)
		self.sThread.start()
	def begServer(self, text):
		self.serverEdit.append(text)
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = SMainWindow()
	mainWindow.show()
	sys.exit(app.exec_())