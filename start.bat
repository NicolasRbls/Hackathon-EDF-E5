@echo off

cd backend

if not exist "venv" (
    echo Create venv with py 3.11
    py -3.11 -m venv venv
    if errorlevel 1 (
        echo Install python 3.11 svp
        pause
        exit /b 1
    )
)

echo Activate venv...
call venv\Scripts\activate
if errorlevel 1 (
    echo Error to activate venv
    pause
    exit /b 1
)

python -m pip install --upgrade pip --quiet

echo Install dependencies...
pip install --upgrade -r requirements.txt  --quiet
if errorlevel 1 (
    echo Error
    pause
    exit /b 1
)

echo ========================================
echo http://localhost:8000/docs
echo.
echo use npm run dev to run frontend
echo Ctrl+C Ctrl+C to stop
echo ========================================

uvicorn app.main:app --reload
if errorlevel 1 (
    echo.
    echo Server error
    pause
    exit /b 1
)
