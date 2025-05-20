@echo off
title TMS Zone Association Tool

REM Set script directory and log file path
set "SCRIPT_DIR=%~dp0"
set "LOGFILE=%SCRIPT_DIR%Content\error_log.txt"
set "TIMESTAMP=%date:~-4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

echo ===================================================
echo         TMS ZONE ASSOCIATION TOOL
echo ===================================================
echo.
echo Starting the process...
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [%TIMESTAMP%] ERROR: Python is not installed or not in PATH. >> "%LOGFILE%"
    echo ERROR: Python is not installed or not in PATH.
    goto :ErrorExit
)

REM Check Python version
FOR /F "tokens=2" %%I IN ('python --version 2^>^&1') DO SET PYTHON_VERSION=%%I
FOR /F "tokens=1,2 delims=." %%A IN ("%PYTHON_VERSION%") DO (
    SET PYTHON_MAJOR=%%A
    SET PYTHON_MINOR=%%B
)
IF %PYTHON_MAJOR% LSS 3 (
    echo [%TIMESTAMP%] ERROR: Python version may not be compatible. Python 3.8 or higher is required. >> "%LOGFILE%"
    echo ERROR: Python version may not be compatible. Python 3.8 or higher is required.
    goto :ErrorExit
)
IF %PYTHON_MAJOR% EQU 3 (
    IF %PYTHON_MINOR% LSS 8 (
        echo [%TIMESTAMP%] ERROR: Python version may not be compatible. Python 3.8 or higher is required. >> "%LOGFILE%"
        echo ERROR: Python version may not be compatible. Python 3.8 or higher is required.
        goto :ErrorExit
    )
)

REM Check if Content directory exists
if not exist "%SCRIPT_DIR%Content\" (
    echo [%TIMESTAMP%] ERROR: Content directory not found. >> "%LOGFILE%"
    echo ERROR: Content directory not found.
    goto :ErrorExit
)

REM Create virtual environment if it doesn't exist
if not exist "%SCRIPT_DIR%Content\env\" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%Content\env"
    if %ERRORLEVEL% neq 0 (
        echo [%TIMESTAMP%] ERROR: Could not create virtual environment. >> "%LOGFILE%"
        echo ERROR: Could not create virtual environment.
        goto :ErrorExit
    )
)

REM Activate virtual environment
call "%SCRIPT_DIR%Content\env\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo [%TIMESTAMP%] ERROR: Could not activate virtual environment. >> "%LOGFILE%"
    echo ERROR: Could not activate virtual environment.
    goto :ErrorExit
)

REM Update pip
echo Updating pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo [%TIMESTAMP%] ERROR: Could not update pip. >> "%LOGFILE%"
    echo ERROR: Could not update pip.
    goto :ErrorExit
)

REM Check if requirements.txt exists
if not exist "%SCRIPT_DIR%Content\requirements.txt" (
    echo [%TIMESTAMP%] ERROR: Requirements file not found: Content\requirements.txt >> "%LOGFILE%"
    echo ERROR: Requirements file not found: Content\requirements.txt
    goto :ErrorExit
)

REM Install dependencies if requirements.txt exists
echo Checking dependencies...
python -m pip install -r "%SCRIPT_DIR%Content\requirements.txt"
if %ERRORLEVEL% neq 0 (
    echo [%TIMESTAMP%] ERROR: Could not install dependencies. >> "%LOGFILE%"
    echo ERROR: Could not install dependencies.
    goto :ErrorExit
)

REM Check if main script exists
if not exist "%SCRIPT_DIR%Content\zone_sh_loc.py" (
    echo [%TIMESTAMP%] ERROR: Main script not found: Content\zone_sh_loc.py >> "%LOGFILE%"
    echo ERROR: Main script not found: Content\zone_sh_loc.py
    goto :ErrorExit
)

REM Run the main script
echo.
echo Starting the application...
echo.
python "%SCRIPT_DIR%Content\zone_sh_loc.py"
set PYTHON_EXIT_CODE=%ERRORLEVEL%

REM Check if the Python script ran successfully
if %PYTHON_EXIT_CODE% neq 0 (
    echo [%TIMESTAMP%] ERROR: The application has ended with errors. Please review the messages above for more details. >> "%LOGFILE%"
    echo ERROR: The application has ended with errors. Please review the messages above for more details.
    goto :ErrorExit
)

REM If the python script ended with no errors, delete the log file
if %PYTHON_EXIT_CODE% equ 0 (
    if exist "%LOGFILE%" del "%LOGFILE%"
    echo.
    echo Process completed successfully.
    echo.
    echo Review the results above carefully.
) else (
    echo.
    echo Log file is available at: %LOGFILE%
)

REM Pause to view results
echo.
echo Press any key to exit...
pause >nul
goto :End

:ErrorExit
echo.
echo An error occurred during execution. See error log for details: %LOGFILE%
echo.
echo Press any key to exit...
pause >nul
exit /b 1

:NormalExit
echo.
echo Process completed successfully.
echo Press any key to exit...
pause >nul
exit /b 0

:End
exit /b 0
