@echo off
C:\Python27\python D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\Resources\alterHost.py
del /F /S /Q D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\output
del /F /S /Q D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\fisrt_round_outputs_dir
del /F /S /Q D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\second_round_outputs_dir
mkdir D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\fisrt_round_outputs_dir
mkdir D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\second_round_outputs_dir
mkdir D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\output
C:\Python27\python -m robot.run --include=test --include=citest --xunit=xunitOutput.xml --outputdir=D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\fisrt_round_outputs_dir D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\Test\BaseFunction\Plus_Web\群发消息.txt 
if errorlevel 0 (
copy D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\fisrt_round_outputs_dir\*.* D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\output\
) else (
C:\Python27\python -m robot.run --nostatusrc --rerunfailed D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\fisrt_round_outputs_dir\output.xml --outputdir=D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\second_round_outputs_dir  --include=test --include=citest D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\Test\BaseFunction\Plus_Web\群发消息.txt 
C:\Python27\python -m robot.rebot  --nostatusrc --outputdir D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\output --xunit=xunitOutput.xml --merge  D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\fisrt_round_outputs_dir\output.xml D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-121-adamdebug\second_round_outputs_dir\output.xml
)
