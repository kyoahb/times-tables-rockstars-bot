REM filepath: /c:/Users/bresk/Desktop/proj/ttrbot2/start.bat
@echo off
SET VENV_DIR=.venv

REM Check if the virtual environment directory exists
IF NOT EXIST %VENV_DIR% (
    echo "Installing Requirements"
    REM Create the virtual environment
    py -m venv %VENV_DIR%
    
    REM Activate the virtual environment
    call %VENV_DIR%\Scripts\activate.bat

    echo "Activated VENV"

    REM Install the requirements line by line
    for /f "tokens=*" %%i in (requirements.txt) do (
        echo "Installing %%i"
        pip install %%i
    )
) ELSE (
    REM Activate the virtual environment
    call %VENV_DIR%\Scripts\activate.bat
    echo "Activated VENV"
)

REM Run the Python script
python main.py

REM Deactivate the virtual environment
deactivate
pause
