#!/bin/bash

echo "========================================"
echo "🚀 PyTorch 快速升級（RTX 3080）"
echo "========================================"
echo

# 檢查 Python
if ! command -v python &> /dev/null; then
    echo "✗ Python 未安裝或不在 PATH 中"
    exit 1
fi
echo "✓ Python 已安裝：$(python --version)"

# 檢查 NVIDIA 驅動
if ! command -v nvidia-smi &> /dev/null; then
    echo "✗ NVIDIA 驅動未安裝或 nvidia-smi 不可用"
    exit 1
fi
echo "✓ NVIDIA 驅動已安裝"
echo

# 顯示當前版本
echo "📊 當前版本："
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.version.cuda}')" 2>/dev/null || echo "PyTorch 未安裝"
echo

# 獲取驅動版本
DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits)
echo "✓ NVIDIA 驅動版本：$DRIVER"
echo

# 選擇 CUDA 版本
CUDA_INDEX="cu124"
if [[ "$DRIVER" =~ ^[5-9][5-9][0-9] ]]; then
    echo "✓ 使用 CUDA 12.4"
    CUDA_INDEX="cu124"
elif [[ "$DRIVER" =~ ^[5-9][3-9][0-9] ]]; then
    echo "✓ 使用 CUDA 12.1"
    CUDA_INDEX="cu121"
else
    echo "✓ 使用 CUDA 11.8"
    CUDA_INDEX="cu118"
fi
echo

# 卸載舊版本
echo "🗑️  卸載舊版本..."
pip uninstall -y torch torchvision torchaudio
echo

# 安裝新版本
echo "📥 安裝最新 PyTorch（$CUDA_INDEX）..."
echo "這可能需要幾分鐘，請等待..."
echo
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/$CUDA_INDEX
if [ $? -ne 0 ]; then
    echo "✗ 安裝失敗"
    exit 1
fi
echo

# 驗證
echo "✅ 驗證安裝..."
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.version.cuda}'); print(f'GPU: {torch.cuda.is_available()}')"
echo

echo "========================================"
echo "✨ 完成！"
echo "========================================"
