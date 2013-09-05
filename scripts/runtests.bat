@set PATH=c:\Python27;%PATH%
@call scripts\vc.bat
@IF ERRORLEVEL 1 EXIT /B 1

@rem work-around cygwin/msdev issue
@set tmp=
@set temp=

python -u -B scripts/runtests.py %1 %2 %3
