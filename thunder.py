#-*- encoding: utf-8 -*-

import ctypes
import sys
import time
import XLError

def main():
	'''
		Python version of thunder demo 
		see: http://xldoc.xl7.xunlei.com/0000000026/index.html
	'''
	XLDownload = ctypes.windll.LoadLibrary('XLDownload.dll')
	# 1、初始化下载引擎
	if not XLDownload.XLInitDownloadEngine():
		print("Initialize download engine failed.")
		sys.exit(1)
	# 2、启动新任务
	# PS：如果链接无法通过，请把工程属性“将wchar_t设置为内置类型        (/Zc:wchar_t)”设置为Yes
	lTaskId = ctypes.c_long(0)
	dwRet = XLDownload.XLURLDownloadToFile("d:\\xmp.exe", "http://xmp.down.sandai.net/kankan/XMPSetup_3.8.1.485-www.exe", "", ctypes.byref(lTaskId))
	if XLError.XL_SUCCESS != dwRet:
		XLDownload.XLUninitDownloadEngine()
		print("Create new task failed, error code:%d."%dwRet)
		if dwRet in XLError.XL_ERROR_MSG:
			print(XLError.XL_ERROR_MSG[dwRet])
		sys.exit(1)
	
	print("Begin download file.")

	# 3、查询任务状态
	while XLError.XL_SUCCESS == dwRet:
		time.sleep(1)

		ullFileSize = ctypes.c_ulonglong(0)
		ullRecvSize = ctypes.c_ulonglong(0)
		lStatus = ctypes.c_long(-1)

		dwRet = XLDownload.XLQueryTaskInfo(lTaskId, ctypes.byref(lStatus), ctypes.byref(ullFileSize), ctypes.byref(ullRecvSize))
		if XLError.XL_SUCCESS == dwRet:
			#输出进度信息
			if 0 != ullFileSize.value:
				douProgress = ullRecvSize.value/ullFileSize.value
				douProgress *= 100.0;
				print("Download progress:%.2f%%" % douProgress)
			else:
				print("File size is zero.")
			if  XLError.enumTaskStatus_Success == lStatus.value:
				print("Download successfully.")
				break
			if  XLError.enumTaskStatus_Fail == lStatus.value:
				print("Download failed.")
				break
	# 4、无论是否下载成功，都必须调用XLStopTask
	XLDownload.XLStopTask(lTaskId)
	# 5、释放资源
	XLDownload.XLUninitDownloadEngine()
	sys.exit(0)

if __name__ == '__main__':
	main()
