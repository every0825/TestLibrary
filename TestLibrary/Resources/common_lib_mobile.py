# -*- coding=utf-8 -*-
import sys
from time import sleep
from robot.libraries.BuiltIn import BuiltIn

global CUSTOME_LIBRARY_NAME
CUSTOME_LIBRARY_NAME = 'applib'

"""
Library of Wrappered/Base UI Keyword for Mobile Ending
Mobile端基础UI关键字库 
"""
class common_lib_mobile(object):
    def __init__(self):
        #self._mobilelib =  BuiltIn().get_library_instance(CUSTOME_LIBRARY_NAME)
        print "init the class common_lib_mobile !"
        self._mobilelib = None
        #添加中文支持,解决 RIDE 本Lib库，关键字不显亮问题
        reload(sys)
        sys.setdefaultencoding('utf8')

    def Mobile_Click_WebView_TextElement2(self, text):
        """用于Android端WebView中的带文本的元素(标准web页可所有点击元素，带link；hybrid web也元素不起作用)点击操作

        | Mobile_Click_WebView_TextElement | ${text} |
        | Mobile_Click_WebView_TextElement | 下载 |
        """
        self._get_appium_handle()
        print 'Current Context:'
        print self._mobilelib.get_contexts()
        print self._mobilelib.get_current_context()
        self._mobilelib.switch_to_context('WEBVIEW_im.yixin')
        print 'Current Context:'
        print self._mobilelib.get_current_context()
        
        #textelement = 'xpath=//*[text()=' + '"' + text + '"]'
        # xpath=//p[text()=‘员工手册学习’]
        #textelement = "xpath=//*[text()=" + "'" + text + "']"
        #textelement = "partial link=" + text
        textelement = "link=" + text
        print textelement
        self._mobilelib.Mobile_Click_Element(textelement)

        sleep(5)
        self._mobilelib.switch_to_context('NATIVE_APP')
        print 'Current Context:'
        print self._mobilelib.get_current_context()

    # Private function
    def _get_appium_handle(self):
        # 获得 当下活动的AppiumLibrary对象 实例，这里的Library名称用的RIDE中的别名
        # 为确保不同的用例集文件下，Testcase执行时可以直接使用每一个KW，故在每一个基础KW内前都要预备实例化一下
        # 有意思的是，资源文件（）的生命周期 是整个pybot命令周期。
        if self._mobilelib == None:
            self._mobilelib =  BuiltIn().get_library_instance(CUSTOME_LIBRARY_NAME)