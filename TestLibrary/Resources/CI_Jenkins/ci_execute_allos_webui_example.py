# coding=utf-8
"""
A CI script support multiple OS.  Windows/Mac/Linux
User can use like this:
python .\Resources\CI_Jenkins\ci_execute_allos_webui_example.py --outputdir .\output --include citest --datasources .\Test\BaseFunction\Plus_Web\朋友圈消息.txt

Now work on windows node only!
"""
import optparse
import os
import re
import sys
import subprocess
import shutil
import platform
from time import ctime



class MyParser(object):
    """the main class
    """
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.default_outputdir = 'RFUI_outputs_dir'
        self.default_xunit_file = 'xunitOutput.xml'
        self.pybot_cmd = ''

        self._first_round_outputs_tempdir = "first_round_outputs_dir"
        self._second_round_outputs_tempdir = "second_round_outputs_dir"
        self.options = self.parse_options()

    def parse_options(self):
        opt = optparse.OptionParser()
        
        opt.add_option('-i', '--include', metavar='STRING',
                       help='Select the cases tOutput run by tags, Example: --include citest  --include P0')
        opt.add_option('-e', '--exclude', metavar='STRING',
                       help='Select the cases tOutput not to run by tags, Example: --exclude noauto')
        opt.add_option('-d', '--outputdir', metavar='STRING',
                       help='directory to create output files,  (defalt: .\RFUI_outputs_dir)')
        opt.add_option('-x', '--xunit', metavar='STRING',
                       help='xUnit compatible result file,  (defalt: xunitOutput.xml)')
        opt.add_option('-s', '--datasources', metavar='STRING',
                       help='RF data sources(testcase/test suite path) to run,  Example: --datasources .\YX_RFUI_Framework_demo\Test\YX_Subscriptions\Plus_Web')

        options, arguments = opt.parse_args()
        return options


    def initialize_para(self):
        """
        initialize the paras to run rebot
        """
        if self.options.outputdir:
            self.default_outputdir = self.options.outputdir
        if self.options.xunit:   
            self.default_xunit_file = self.options.xunit

    def manage_output_dir(self):
        """
        clear empty workspaces dirs
        """
        self._initialize_dir(self.options.outputdir)
        self._initialize_dir(self._first_round_outputs_tempdir)
        self._initialize_dir(self._second_round_outputs_tempdir)


    def pybot_run(self):
        """run pybot cmd with inputs according to current OS system
        """
        uname_str = platform.system()
        if re.search("Darwin", uname_str):
            self.job_mac()
        elif re.search("Windows", uname_str):
            self.job_windows()
        elif re.search("Linux", uname_str):
            self.job_linux()
        else:
            print "[x]:can NOT detect OS type :-("


    def job_mac(self):
        """Mac's job
        """
        print "\n\n>>>here is from Mac\n\n"
        cmd = ' '.join(self.input_cmd)
        cmd = 'pybot' + ' ' + cmd
        print os.popen(cmd).read()

    def job_linux(self):
        """Linux's job
        """
        print "[info]:Linux fx() need added in future ;-)"


    def job_windows(self):
        """Win's job
        """
        print "\n\n>>>here is on Windows\n\n"
        cur_dir = os.path.abspath('.')
        #pybot_execution_cmd = self._first_round_pybot_execution_cmd()
        #print "pybot_execution_cmd:\n%s" % pybot_execution_cmd
        #print os.popen(pybot_execution_cmd).read()
        #exit_value = os.system(pybot_execution_cmd)

        exit_value = self._one_round_pybot_execution(round_num=1)
        if exit_value > 0:
            #in case of failed cases in first round run, 
            # <1>launch the second round and merge output
            # <2>and copy png to default_outputdir         
            #   cp ${SECOND_ROUND_OUTPUT_DIR}/*.png  ${OUTPUT_DIR}
            self._one_round_pybot_execution(round_num=2)
            self._rebot_merge_execution()
            
            cp_cmd = 'copy /y' + ' ' + os.path.abspath(os.path.join(self._second_round_outputs_tempdir, '*.png'))
            cp_cmd += ' ' + os.path.abspath(self.default_outputdir)
            print "This copy cmd:\n%s" % cp_cmd
            os.system(cp_cmd)

        else:
            #if case of all test cases passed in first round run 
            #Just do copy the results to self.outputdir
            #    copy D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\fisrt_round_outputs_dir D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\output
            cp_cmd = 'copy /y' + ' ' + os.path.abspath(self._first_round_outputs_tempdir) 
            cp_cmd += ' ' + os.path.abspath(self.default_outputdir)
            print "This copy cmd:\n%s" % cp_cmd
            os.system(cp_cmd)


    def _one_round_pybot_execution(self, round_num=1):
        """
        setup the firt round pybot execution cmd to run
        pybot --include=test --include=citest --xunit=xunitOutput.xml --outputdir=.\first_round_outputs_dir .\Test\BaseFunction\Plus_Web
        pybot --rerunfailed .\fisrt_round_outputs_dir\output.xml --include=test --include=citest --outputdir=.\second_round_outputs_dir .\Test\BaseFunction\Plus_Web
       """
        pybot_cmd = 'pybot'
        #pybot_cmd = 'python' + ' ' + '-m' + ' ' + 'robot.run'
        if round_num == 1:
            pybot_cmd += ' ' + '--outputdir' + ' ' + os.path.abspath(self._first_round_outputs_tempdir)
        elif round_num == 2:
            failed_round_outputs_path = os.path.join(self._first_round_outputs_tempdir, 'output.xml')
            pybot_cmd += ' ' + '--rerunfailed' + ' ' + os.path.abspath(failed_round_outputs_path)
            pybot_cmd += ' ' + '--outputdir' + ' ' + os.path.abspath(self._second_round_outputs_tempdir)
        else:
            print "Not support round_num: %d!\nonly support round_num=1 or 2! " % round_num

        pybot_cmd += ' ' + '--xunit' + ' ' + self.default_xunit_file
        if self.options.include:
            pybot_cmd += ' ' + '--include' + ' ' + self.options.include 
        if self.options.exclude:       
            pybot_cmd += ' ' + '--exclude' + ' ' + self.options.exclude 
        if self.options.datasources:
            pybot_cmd +=  ' ' + self.options.datasources
        print "This round pybot execution cmd:\n%s" % pybot_cmd
        return os.system(pybot_cmd)


    def _rebot_merge_execution(self):
        """
        merge the two round outputs to one
        rebot --nostatusrc --outputdir .\output --xunit=xunitOutput.xml --merge .\fisrt_round_outputs_dir\output.xml .\second_round_outputs_dir\output.xml
        """
        #cur_dir = os.path.abspath('.')
        #os.chdir(cur_dir)
        rebot_cmd = 'rebot' + ' ' + '--nostatusrc'
        rebot_cmd += ' ' + '--output' + ' ' + 'output.xml'
        rebot_cmd += ' ' + '--outputdir' + ' ' + self.default_outputdir
        rebot_cmd += ' ' + '--xunit' + ' ' + self.default_xunit_file
        first_round_outputs_path = os.path.join(self._first_round_outputs_tempdir, 'output.xml')
        second_round_outputs_path = os.path.join(self._second_round_outputs_tempdir, 'output.xml')
        rebot_cmd += ' ' + '--merge' + ' ' + first_round_outputs_path + ' ' + second_round_outputs_path
        print "rebot_cmd to merge two round outputs:\n%s" % rebot_cmd
        os.system(rebot_cmd)


    def _initialize_dir(self, dir_path):
        abs_path=os.path.abspath(dir_path)
        if os.path.exists(abs_path):
            try:
                shutil.rmtree(abs_path)
                os.mkdir(abs_path)
            except IOError, error:
                print IOError, ">>>", error
        else:
            try:
                os.mkdir(abs_path)
            except IOError, error:
                print IOError, ">>>", error


if __name__ == '__main__':

    myparser = MyParser()
    if not myparser.options.datasources:
        print 'Must input value for "--datasources",  Here is example:'
        print '%s --outputdir .\RFUI_outputs_dir --include citest --datasources .\YX_RFUI_Framework_demo\Test\YX_Subscriptions\Plus_Web ' % sys.argv[0]
        print '%s --datasources .\YX_Plus_RFUI\Test\BaseFunction\Plus_Web ' % sys.argv[0]
    elif not os.path.exists(myparser.options.datasources):
        print 'options.datasources do not exist, Please double path of "--datasources"!,  Here is example:'
        print '%s --outputdir .\RFUI_outputs_dir --include citest --datasources .\YX_RFUI_Framework_demo\Test\YX_Subscriptions\Plus_Web ' % sys.argv[0]
        print '%s --datasources .\YX_Plus_RFUI\Test\BaseFunction\Plus_Web ' % sys.argv[0]
    else:
        myparser.initialize_para()
        myparser.manage_output_dir()  #  结果/临时文件夹整理  mkdir ./RFUI_outputs_dir
        myparser.pybot_run()  # 脚本执行，错误用例二次执行，执行结果合并
    exit(0)

