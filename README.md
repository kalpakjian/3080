# 3080 - PyTorch 自動升級腳本

🚀 自動檢查和升級 PyTorch、CUDA、cuDNN 到最新版本，專為 RTX 3080 等 NVIDIA GPU 設計。

## ✨ 功能特點

- 🔍 **自動檢測** - 檢查當前 PyTorch、CUDA、cuDNN 版本
- 📊 **硬體識別** - 檢測 NVIDIA 驅動版本和 GPU 型號
- 🗑️ **乾淨卸載** - 自動移除舊版本 PyTorch
- 🎯 **智能選擇** - 根據驅動版本自動選擇合適的 CUDA 版本（12.4 / 12.1 / 11.8）
- 📥 **一鍵安裝** - 自動下載並安裝最新 GPU 版 PyTorch
- ✅ **自動驗證** - 安裝後驗證並執行 GPU 測試

## 🚀 快速開始

### 前置條件

- Python 3.8 或更高版本
- pip 21.2 或更高版本
- NVIDIA GPU（建議驅動版本 520+）
- Windows / Linux / macOS

### 使用方法

#### 1. 克隆倉庫

```bash
git clone https://github.com/kalpakjian/3080.git
cd 3080
```

#### 2. 執行腳本

```bash
python check_and_upgrade_pytorch.py
```

腳本會自動：
1. 顯示當前 PyTorch/CUDA/cuDNN 版本
2. 檢測 NVIDIA 驅動和 GPU 型號
3. 詢問是否升級到最新版本
4. 卸載舊版本
5. 安裝最新 GPU 版 PyTorch
6. 驗證安裝結果

#### 3. 驗證安裝

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.version.cuda}'); print(f'GPU: {torch.cuda.is_available()}')"
```

### 方法二：一鍵執行（推薦）

**Windows：**

```bash
quick_upgrade.bat
```

或直接雙擊 `quick_upgrade.bat` 文件

**Linux / macOS：**

```bash
./quick_upgrade.sh
```

這個腳本會自動：
- 檢測 NVIDIA 驅動版本
- 選擇合適的 CUDA 版本
- 卸載舊版 PyTorch
- 安裝最新版
- 驗證安裝結果



如果不想使用腳本，可以手動執行：

### 卸載舊版本

```bash
pip uninstall -y torch torchvision torchaudio
```

### 安裝最新版本

根據你的 NVIDIA 驅動版本選擇合適的命令：

```bash
# CUDA 12.4（驅動版本 >= 550，推薦）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# CUDA 12.1（驅動版本 >= 530）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8（驅動版本 >= 520）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 檢查驅動版本

```bash
# Windows / Linux
nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits
```

## 🔧 故障排除

### GPU 不可用

如果 `torch.cuda.is_available()` 返回 `False`：

1. 確認 NVIDIA 驅動已安裝：
   ```bash
   nvidia-smi
   ```

2. 確認使用正確的 CUDA 版本：
   ```bash
   python -c "import torch; print(torch.version.cuda)"
   ```

3. 重新安裝匹配的 CUDA 版本：
   ```bash
   pip uninstall -y torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```

### 權限錯誤

如果遇到權限問題，添加 `--user` 參數：

```bash
pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### 使用虛擬環境（推薦）

```bash
# 創建虛擬環境
python -m venv venv

# 啟用虛擬環境
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 安裝 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

## 📊 版本相容性

| NVIDIA 驅動版本 | 推薦 CUDA | PyTorch 索引 |
|----------------|-----------|-------------|
| >= 550         | 12.4      | cu124       |
| >= 530         | 12.1      | cu121       |
| >= 520         | 11.8      | cu118       |
| < 520          | 11.8      | cu118       |

## 💡 提示

- PyTorch 自帶 CUDA 運行時，通常**不需要**單獨安裝系統級 CUDA Toolkit
- cuDNN 同樣包含在 PyTorch wheel 中，無需手動安裝
- RTX 3080 建議使用驅動版本 **550+** 以獲得最佳效能
- 建議在虛擬環境（venv/conda）中操作，避免污染系統 Python

## 📚 參考資源

- [PyTorch 官方安裝指南](https://pytorch.org/get-started/locally/)
- [PyTorch CUDA 版本相容性](https://gigagpu.com/pytorch-cuda-version-compatibility/)
- [NVIDIA 驅動下載](https://www.nvidia.com/Download/index.aspx)
- [CUDA Toolkit 文檔](https://docs.nvidia.com/cuda/)

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

***

**Happy Coding!** 🎉
