@ECHO OFF

REM Allow to explicitly specify the desired Visual Studio version
IF /I "%1" == "vc12" GOTO TRY_VS12
IF /I "%1" == "vc10" GOTO TRY_VS10

REM vs10 is VS 2010
:TRY_VS10
CALL "%VS100COMNTOOLS%\vsvars32.bat" 2>NUL
IF NOT ERRORLEVEL 1 EXIT /B

REM vs12 is VS 2012
:TRY_VS12
CALL "%VS110COMNTOOLS%\vsvars32.bat" 2>NUL
IF NOT ERRORLEVEL 1 EXIT /B

ECHO Visual Studio 2012 or 2010 doesn't seem to be installed
EXIT /B 1
