@echo off

set pd=\rpa_project
set f=\mydir
set d=%USERPROFILE%%pd%
set c=D:dev\hysrpa\gprofile.json
set b=backup.reg

rem �v���W�F�N�g�f�B���N�g���̍쐬
mkdir %d%
echo %c% > %d%%f%

rem �O�������vb�v���W�F�N�g�ւ̃A�N�Z�X�ݒ�̕ύX
set q="HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\16.0\Excel\Security"
reg query %q% | find %q% 
if %ErrorLevel%==1 goto NEXT 
if %ErrorLevel%==0 (
reg export %q% %d%\16.0%b%
reg add %q% /v "VBAWarnings" /t REG_DWORD /d "3" /f
)

rem �O�������vb�v���W�F�N�g�ւ̃A�N�Z�X�ݒ�̕ύX
:NEXT
set q="HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\8.0\Excel\Security"
reg query %q% | find %q% 
if %ErrorLevel%==1 goto NEXTN 
if %ErrorLevel%==0 (
reg export %q% %d%\8.0%b%
reg add %q% /v "VBAWarnings" /t REG_DWORD /d "3" /f
)

:NEXTN
exit /b 0
