import ctypes
import sys
import time
#user32 = ctypes.windll.LoadLibrary('user32.dll')
#user32.MessageBoxW(0, 'hello world', 'title', 0)
#ctypes.windll.user32.MessageBoxW(0, "hello world", "tiltle", 0)

XLDownload = ctypes.windll.LoadLibrary(r'C:\Users\RileyRen\Desktop\thunder\XLDownload.dll')
if not XLDownload.XLInitDownloadEngine():
	print("Initialize download engine failed.")
	sys.exit(1)
lTaskId = ctypes.c_long(0)
dwRet = XLDownload.XLURLDownloadToFile("d:\\xmp.exe", "http://xmp.down.sandai.net/kankan/XMPSetup_3.8.1.485-www.exe", "", ctypes.byref(lTaskId))
if dwRet:
  XLDownload.XLUninitDownloadEngine()
  print("Create new task failed, error code:%d."%dwRet)
  sys.exit(1)
print("Begin download file.")

while 0 == dwRet:
	time.sleep(1)

	ullFileSize = ctypes.c_ulonglong(0)
	ullRecvSize = ctypes.c_ulonglong(0)
	lStatus = ctypes.c_long(-1)

	dwRet = XLDownload.XLQueryTaskInfo(lTaskId, ctypes.byref(lStatus), ctypes.byref(ullFileSize), ctypes.byref(ullRecvSize))
	if not dwRet:
	   #输出进度信息
		if 0 != ullFileSize:
			douProgress = ullRecvSize.value/ullFileSize.value
			douProgress *= 100.0;
			print("Download progress:%.2f%%" % douProgress)
		else:
			print("File size is zero.")
		if  11 == lStatus.value:
			print("Download successfully.")
			break
		if  12 == lStatus.value:
			print("Download failed.")
			break
	   
XLDownload.XLStopTask(lTaskId)
XLDownload.XLUninitDownloadEngine()
sys.exit(0)
