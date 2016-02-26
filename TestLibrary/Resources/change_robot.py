import sys
import os
import shutil
import re

mac_partpath1 = '/Library/Python/2.7/site-packages/'
mac_partpath2 = '/usr/local/lib/python2.7/site-packages/'
windows_partpath = '\\Lib\\site-packages\\robot\\reporting\\'
xunitwriter = 'xunitwriter.py'

def mac_copyfile(argpath):
	ls_files = os.listdir(argpath)
	match_path = ''
	for myfile in ls_files:
		match = re.match(r'robotframework-2.9.*-py2.7.egg', myfile)
		if match != None:
			match_path = match.group(0)			
	    	mac_xunitpath = argpath + match_path + '/robot/reporting/' + xunitwriter
	    	cur_path = os.path.abspath(os.curdir)
	    	if os.path.exists(mac_xunitpath):
				myfile_path = cur_path + '/' + xunitwriter
				shutil.copy(myfile_path, mac_xunitpath)


if __name__ == '__main__':
	if sys.platform == 'darwin':
		if os.path.exists(mac_partpath1):
			mac_copyfile(mac_partpath1)
		
		if os.path.exists(mac_partpath2):
			mac_copyfile(mac_partpath2)

	if sys.platform == 'win32':
		execpath = sys.executable
		pythonpath = execpath[0 : execpath.rfind(os.sep)]
		xunit_path = pythonpath + windows_partpath
		file_path = xunit_path + xunitwriter

		cur_path = os.path.abspath(os.curdir)
		myfile_path = cur_path + '\\' + xunitwriter
		if os.path.isfile(file_path):
			shutil.copy(myfile_path, file_path)