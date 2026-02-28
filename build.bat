@echo off
REM Cross-platform build script for SysProbe - Windows version
REM Builds binaries for Windows (x86_64 and ARM64)

echo SysProbe Cross-Platform Builder
echo ====================================

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install PyInstaller
)

REM Default to x86_64
set ARCH_NAME=x86_64

REM Try to detect architecture using PowerShell (more reliable than wmic)
for /f "tokens=*" %%i in ('powershell -Command "[Environment]::Is64BitOperatingSystem"') do set IS_64BIT=%%i
if "%IS_64BIT%"=="False" (
    set ARCH_NAME=x86
)

echo Building for Windows %ARCH_NAME%

REM Create directories
if not exist build mkdir build
if not exist dist mkdir dist

REM Generate spec file if it doesn't exist
if not exist "build\windows-%ARCH_NAME%.spec" (
    echo Generating spec file...
    pyinstaller --onefile --windowed --name=SysProbe main.py --specpath=build -p . >nul 2>&1
    if exist "build\SysProbe.spec" (
        move "build\SysProbe.spec" "build\windows-%ARCH_NAME%.spec" >nul
    )
)

REM Build the executable
echo Building executable...
pyinstaller "build\windows-%ARCH_NAME%.spec" --distpath dist --workpath build\build

REM Rename the executable
if exist "dist\SysProbe.exe" (
    move "dist\SysProbe.exe" "dist\SysProbe-windows-%ARCH_NAME%.exe" >nul
    echo.
    echo Build complete!
    echo Executable: dist\SysProbe-windows-%ARCH_NAME%.exe
) else (
    echo Build failed!
    exit /b 1
)

pause

