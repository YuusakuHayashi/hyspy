@echo off

set project_dir=\rpa_project
set dir_file=\mydir
set user_dir=%USERPROFILE%%project_dir%
set gprofile=D:dev\hysrpa\gprofile.json
set backup_file=backup.reg

rem �v���W�F�N�g�f�B���N�g���̍쐬 ----------------------------------------------
mkdir %user_dir%
echo %gprofile% > %user_dir%%dir_file%
rem -----------------------------------------------------------------------------


rem �O�������vb�v���W�F�N�g�ւ̃A�N�Z�X�ݒ�̕ύX ------------------------------
set %ErrorLevel%=0
set myquery="HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\16.0\Excel\Security"
reg query %myquery% | find %myquery% 
if %ErrorLevel%==1 goto VBI_END
if %ErrorLevel%==0 (
reg export %myquery% %user_dir%\16.0%backup_file%
reg add %myquery% /v "VBAWarnings" /t REG_DWORD /d "3" /f
)
:VBI_END
rem -----------------------------------------------------------------------------

rem �O�������vb�v���W�F�N�g�ւ̃A�N�Z�X�ݒ�̕ύX ------------------------------
set %ErrorLevel%=0
set myquery="HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\8.0\Excel\Security"
reg query %myquery% | find %myquery% 
if %ErrorLevel%==1 goto VBII_END
if %ErrorLevel%==0 (
reg export %myquery% %user_dir%\8.0%backup_file%
reg add %myquery% /v "VBAWarnings" /t REG_DWORD /d "3" /f
)
:VBII_END
rem -----------------------------------------------------------------------------

:PY
rem Python�̃C���X�g�[�� --------------------------------------------------------
set py_file=\mypy
if %PROCESSOR_ARCHITECTURE%==x86 (
echo %PROGRAMFILES%\Python36 > %user_dir%%py_file%
) else if %PROCESSOR_ARCHITECTURE%==AMD64 (
echo "%PROGRAMFILES(x86)%\Python36-32" > %user_dir%%py_file%
) else (
echo ���g���̒[����CPU������ł��܂���ł���
echo mypy�t�@�C�����쐬���܂���ł���
)

set /p python="Python���C���X�g�[�����܂���? (y/n)"
if %python%==n ( 
echo �C���X�g�[�����܂���ł���
goto PY_END
) else if %python%==y (
echo �C���X�g�[�����Ă��܂�
call :GET_PY
goto PY_END
) else (
goto PY
)
:PY_END

:END
exit /b 0



:GET_PY
Call C:\Users\xxxxxxxxxxxxxxx\Downloads\python-3.6.8.exe /quiet /passive ^
InstallAllUsers=1 ^
AssociateFiles=0 ^
CompileAll=0 ^
PrependPath=0 ^
Shortcuts=0 ^
Include_doc=0 ^
Include_debug=0 ^
Include_dev=0 ^
Include_exe=1 ^
Include_launcher=0 ^
InstallLauncherAllUser=0 ^
Include_lib=1 ^
Include_pip=1 ^
Include_symbols=0 ^
Include_tcltk=0 ^
Include_test=0 ^
Include_tools=1 ^
LauncherOnly=0 ^
