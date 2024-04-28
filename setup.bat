@echo off

rem Prompt user to select Python installation directory
setlocal
call :getPythonDir
endlocal
goto :eof

:getPythonDir
set /p "PYTHON_DIR=Enter Python installation directory (e.g., C:\Python): "

rem Check if Python executable exists in the selected directory
if exist "%PYTHON_DIR%\python.exe" (
    set PYTHON_PATH="%PYTHON_DIR%\python.exe"
) else (
    echo Python executable not found in the specified directory.
    goto :getPythonDir
)

rem Installing required Python packages
echo Updating pip...
%PYTHON_PATH% -m pip install --upgrade pip
echo Installing required Python packages from requirements.txt...
%PYTHON_PATH% -m pip install -r requirements.txt

rem Proceed with creating scheduled task using PYTHON_PATH
set SCRIPT_NAME=auto_speed_test.py
set SCRIPT_PATH=%~dp0%SCRIPT_NAME%

echo PYTHON_PATH: %PYTHON_PATH%
echo SCRIPT_PATH: %SCRIPT_PATH% 

set TASK_NAME="Auto Speed Test"
set TRIGGER_FREQUENCY="HOURLY"

echo Creating scheduled task...

schtasks /create /tn %TASK_NAME% /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" /sc %TRIGGER_FREQUENCY% /mo 1


echo Task created successfully.
