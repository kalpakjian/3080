@echo off
echo ========================================
echo 🚀 PyTorch 快速升級（RTX 3080）
echo ========================================
echo.

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python 未安裝或不在 PATH 中
    pause
    exit /b 1
)
echo ✓ Python 已安裝

REM 檢查 NVIDIA 驅動
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo ✗ NVIDIA 驅動未安裝或 nvidia-smi 不可用
    pause
    exit /b 1
)
echo ✓ NVIDIA 驅動已安裝
echo.

REM 顯示當前版本
echo 📊 當前版本：
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.version.cuda}')" 2>nul || echo PyTorch 未安裝
echo.

REM 獲取驅動版本
for /f "tokens=*" %%i in ('nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits') do set DRIVER=%%i
echo ✓ NVIDIA 驅動版本：%DRIVER%
echo.

REM 選擇 CUDA 版本
set CUDA_INDEX=cu124
echo %DRIVER% | findstr /r "^[5-9][5-9][0-9]" >nul
if not errorlevel 1 (
    echo ✓ 使用 CUDA 12.4
    set CUDA_INDEX=cu124
) else (
    echo %DRIVER% | findstr /r "^[5-9][3-9][0-9]" >nul
    if not errorlevel 1 (
        echo ✓ 使用 CUDA 12.1
        set CUDA_INDEX=cu121
    ) else (
        echo ✓ 使用 CUDA 11.8
        set CUDA_INDEX=cu118
    )
)
echo.

REM 卸載舊版本
echo 🗑️  卸載舊版本...
pip uninstall -y torch torchvision torchaudio
echo.

REM 安裝新版本
echo 📥 安裝最新 PyTorch（%CUDA_INDEX%）...
echo 這可能需要幾分鐘，請等待...
echo.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/%CUDA_INDEX%
if errorlevel 1 (
    echo ✗ 安裝失敗
    pause
    exit /b 1
)
echo.

REM 驗證
echo ✅ 驗證安裝...
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.version.cuda}'); print(f'GPU: {torch.cuda.is_available()}')"
echo.

echo ========================================
echo ✨ 完成！
echo ========================================
pause
