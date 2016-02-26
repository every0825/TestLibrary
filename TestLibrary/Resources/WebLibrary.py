# -*- coding: utf-8 -*-
import time
try:
	import SendKeys
except ImportError:
	# try to import other lib for target OS platform
	pass
try:
	import win32gui
except ImportError:
	# try to import other lib for target OS platform
	pass
import sys
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

"""
自定义Web Library
"""
NAME_Selenium2Library = 'weblib'#Selenium2Library的别名(RIDE中使用的别名)

class WebLibrary(object):

	ROBOT_LIBRARY_SCOPE = 'GLOBAL'
	ROBOT_LIBRARY_VERSION = 1.0 #版本

	def __init__(self):
		"""这里的代码其可以默认执行
		"""	
		reload(sys)
		sys.setdefaultencoding('utf8')
		self._handle = None	
		self._selenium2 = None

	# Public Keywords

	def set_selenium2(self):
		#实例化一个当下活动的Selenium2Library对象，这里的Library名称用的RIDE中的别名
		#初步认为每个Testcase执行的时候，都要获取最新的实例，但Keyword是分开执行的，最好每个里面都要预备实例化一下
		if self._selenium2 == None:
			self._selenium2 = BuiltIn().get_library_instance('weblib')#实例一个当下活动的Selenium2Library对象，这里的Library名称用的RIDE中的别名

