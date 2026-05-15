@echo off
chcp 65001 >nul
cd /d "%~dp0"

:menu
cls
echo ================================================
echo            CSDN 博客导出器 - 启动菜单
echo ================================================
echo.
echo    1. 图形界面模式 (推荐)
echo    2. 终端交互模式
echo    3. 退出
echo.
echo ================================================
choice /c 123 /n /m "请选择运行模式 (1/2/3): "

if errorlevel 3 exit
if errorlevel 2 goto terminal
if errorlevel 1 goto gui

:gui
echo.
echo 正在启动图形界面...
python gui.py
goto end

:terminal
echo.
echo 正在启动终端模式...
python run_interactive.py
goto end

:end
echo.
echo 按任意键退出...
pause >nul
