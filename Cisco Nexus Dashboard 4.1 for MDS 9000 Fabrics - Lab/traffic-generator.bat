@echo off
setlocal enabledelayedexpansion
set XMLFILE=C:\dCloud\session.xml
for /f "usebackq tokens=*" %%i in (`powershell -Command "(Select-Xml -Path '%XMLFILE%' -XPath '//device/name').Node.'#text'"`) do set PODNAME=%%i
set "dcv-mds-pod1=198.19.253.171"
set "dcv-mds-pod2=198.19.253.172"
set "dcv-mds-pod3=198.19.253.173"
set "dcv-mds-pod4=198.19.253.174"
set "dcv-mds-pod5=198.19.253.175"
set "dcv-mds-pod6=198.19.253.176"
set "dcv-mds-pod7=198.19.253.177"
set "dcv-mds-pod8=198.19.253.178"
set "VMIP=!%PODNAME%!"
cls
START "Disk Test 1 (Small File)" /B C:\psexec.exe \\%VMIP% -h -nobanner cmd /k "diskspd.exe -c40G -b1M -d300 -r -w100 -t8 -o64 -L -Sh -L -Zr -W0 E:\san_testfile_small.dat"
START "Disk Test 2 (Large File)" /B C:\psexec.exe \\%VMIP% -h -nobanner cmd /k "diskspd.exe -c40G -b8k -d300 -r -w10 -t16 -o256 -L -Sh -L -Zr -W0 E:\san_testfile_large.dat"
ECHO.
ECHO ====================================================================
ECHO  Please do not close this window. You may minimize it. The process will run for 5 minutes.
ECHO  Do not open multiple instances of this window. Only one window can run at a time.
ECHO  If you want to run the test again, close this window and start the test again.
ECHO ====================================================================
ECHO  Performance tests are now running....
ECHO.