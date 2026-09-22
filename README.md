# 3080 - PyTorch 升級腳本

用於檢查和升級 PyTorch、CUDA、cuDNN 到最新版本的自動化腳本，適用於 RTX 3080 等 NVIDIA GPU。

## 功能

- ✅ 檢查當前 PyTorch、CUDA、cuDNN 版本
- ✅ 檢測 NVIDIA 驅動版本和 GPU 型號
- ✅ 自動卸載舊版本 PyTorch
- ✅ 根據驅動版本選擇合適的 CUDA 版本（12.4 / 12.1 / 11.8）
- ✅ 安裝最新 GPU 版 PyTorch
- ✅ 驗證安裝結果並執行簡單 GPU 測試

## 使用說明

### 執行腳本

```bash
python check_and_upgrade_pytorch.py
```

### 手動安裝命令

```bash
# 卸載舊版本
pip uninstall -y torch torchvision torchaudio

# 安裝最新版（CUDA 12.4，適合驅動 550+）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# 或 CUDA 12.1（適合驅動 530+）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 或 CUDA 11.8（適合驅動 520+）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 驗證安裝

```python
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA: {torch.version.cuda}")
print(f"GPU 可用：{torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"cuDNN: {torch.backends.cudnn.version()}")
```

## 注意事項

- PyTorch 自帶 CUDA 運行時，通常不需要單獨安裝系統級 CUDA Toolkit
- cuDNN 同樣包含在 PyTorch wheel 中，無需手動安裝
- RTX 3080 建議使用驅動 550+ 以支援 CUDA 12.4
- 建議在虛擬環境（venv/conda）中操作

## 參考連結

- [PyTorch 官方安裝指南](https://pytorch.org/get-started/locally/)
- [PyTorch CUDA 版本相容性](https://gigagpu.com/pytorch-cuda-version-comcompatibility/)
