#!/usr/bin/env python3
"""
PyTorch + CUDA + cuDNN 版本檢查與升級腳本
適用於 RTX 3080 等 NVIDIA GPU
"""

import subprocess
import sys
import importlib
from pathlib import Path


def run_command(cmd, shell=True):
    """執行命令並返回輪出"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def check_current_versions():
    """檢查當前安裝的版本"""
    print("=" * 60)
    print("📊 當前系統版本資訊")
    print("=" * 60)

    # 檢查 PyTorch
    try:
        import torch

        print(f"✓ PyTorch 版本：{torch.__version__}")
        print(f"  - CUDA 版本 (torch 內建): {torch.version.cuda}")
        if torch.cuda.is_available():
            print(f"  - cuDNN 版本：{torch.backends.cudnn.version()}")
            print(f"  - GPU 可用：是")
            print(f"  - GPU 名稱：{torch.cuda.get_device_name(0)}")
            print(f"  - GPU 數量：{torch.cuda.device_count()}")
        else:
            print(f"  - GPU 可用：否 ⚠️")
    except ImportError:
        print("✗ PyTorch 未安裝")

    # 檢查 NVIDIA 驅動
    success, stdout, stderr = run_command(
        "nvidia-smi --query-gpu=driver_version,name --format=csv,noheader"
    )
    if success and stdout:
        parts = stdout.split(", ")
        print(f"✓ NVIDIA 驅動版本與GPU型號：{parts}")
    else:
        print("✗ 無法讀取 NVIDIA 驅動資訉")

    # 檢查 CUDA Toolkit（系統層級）
    success, stdout, stderr = run_command("nvcc --version")
    if success:
        for line in stdout.split("\n"):
            if "release" in line.lower():
                print(f"✓ CUDA Toolkit: {line.strip()}")
                break
    else:
        print("⚠ CUDA Toolkit 未安裝或不在 PATH 中（PyTorch 通常自帶 CUDA）")

    print()


def get_latest_pytorch_info():
    """獲取最新 PyTorch 版本資訊"""
    print("=" * 60)
    print("🔍 查詢最新 PyTorch 版本...")
    print("=" * 60)

    # 使用 pip index 查詢（需要 pip >= 21.2）
    success, stdout, stderr = run_command("pip index versions torch")

    if success and "Available versions:" in stdout:
        # 提取最新版本號
        for line in stdout.split("\n"):
            if line.startswith("Available versions:"):
                versions = line.replace("Available versions:", "").strip()
                latest = versions.split(",").strip()
                print(f"✓ 最新 PyTorch 版本：{latest}")
                return latest
    else:
        # 備用方法：直接 pip install 會顯示最新版本
        print("⚠ 無法透過 pip index 查詢，將嘗試直接安裝最新版")
        return None

    return None


def uninstall_pytorch():
    """卸載現有 PyTorch"""
    print("\n" + "=" * 60)
    print("🗑️  卸載現有 PyTorch...")
    print("=" * 60)

    packages = ["torch", "torchvision", "torchaudio"]
    for pkg in packages:
        print(f"正在卸載 {pkg}...")
        success, stdout, stderr = run_command(f"pip uninstall -y {pkg}")
        if success:
            print(f"✓ {pkg} 已卸載")
        else:
            print(f"⚠ {pkg} 卸載失敗或不存在")

    print()


def install_latest_pytorch():
    """安裝最新 PyTorch（GPU 版本）"""
    print("=" * 60)
    print("📥 安裝最新 PyTorch（CUDA 12.4 / 12.1 / 11.8）...")
    print("=" * 60)

    # 根據 NVIDIA 驅動版本選擇合適的 CUDA 版本
    success, stdout, stderr = run_command(
        "nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits"
    )

    driver_version = None
    if success and stdout:
        try:
            driver_version = float(stdout.strip())
        except ValueError:
            pass

    # 選擇 CUDA 版本（參考：https://gigagpu.com/pytorch-cuda-version-comcompatibility/）
    if driver_version and driver_version >= 550:
        cuda_index = "cu124"  # CUDA 12.4
        print("✓ 檢測到驅動 >= 550，使用 CUDA 12.4")
    elif driver_version and driver_version >= 530:
        cuda_index = "cu121"  # CUDA 12.1
        print("✓ 檢測到驅動 >= 530，使用 CUDA 12.1")
    elif driver_version and driver_version >= 520:
        cuda_index = "cu118"  # CUDA 11.8
        print("✓ 檢測到驅動 >= 520，使用 CUDA 11.8")
    else:
        cuda_index = "cu124"  # 預設最新
        print("⚠ 無法檢測驅動版本，預設使用 CUDA 12.4")

    # 安裝命令
    install_cmd = (
        f"pip install torch torchvision torchaudio "
        f"--index-url https://download.pytorch.org/whl/{cuda_index}"
    )

    print(f"\n📦 執行安裝命令：\n{install_cmd}\n")
    print("這可能需要幾分鐘，請等待...\n")

    success, stdout, stderr = run_command(install_cmd, shell=True)

    if success:
        print("✓ PyTorch 安裝成功！")
    else:
        print("✗ PyTorch 安裝失敗")
        print(f"錯誤資訊：{stderr}")
        return False

    print()
    return True


def verify_installation():
    """驗證安裝結果"""
    print("=" * 60)
    print("✅ 驗證安裝結果")
    print("=" * 60)

    # 重新導入 torch（如果之前已導入，需要重新載入）
    if "torch" in sys.modules:
        importlib.reload(sys.modules["torch"])

    try:
        import torch

        print(f"✓ PyTorch 版本：{torch.__version__}")
        print(f"✓ CUDA 版本 (torch): {torch.version.cuda}")

        if torch.cuda.is_available():
            print(f"✓ GPU 可用：是")
            print(f"✓ GPU 名稱：{torch.cuda.get_device_name(0)}")
            print(f"✓ cuDNN 版本：{torch.backends.cudnn.version()}")
            print(f"✓ GPU 數量：{torch.cuda.device_count()}")

            # 簡單測試
            print("\n🧪 執行簡單 GPU 測試...")
            x = torch.rand(5, 3).cuda()
            y = torch.rand(5, 3).cuda()
            z = x + y
            print(f"✓ GPU 張量運算測試通過")
        else:
            print("✗ GPU 不可用！請檢查驅動和安裝")

    except Exception as e:
        print(f"✗ 驗證失敗：{e}")


def main():
    """主函數"""
    print("\n🚀 PyTorch 版本檢查與升級腳本")
    print("適用於 RTX 3080 等 NVIDIA GPU\n")

    # 1. 檢查當前版本
    check_current_versions()

    # 2. 獲取最新版本資訊
    latest_version = get_latest_pytorch_info()

    # 3. 詢問用戶是否繼續
    if latest_version:
        response = input("\n是否要升級到最新版本？(y/n): ").strip().lower()
        if response != "y":
            print("已取消升級")
            return
    else:
        response = input("\n是否要重新安裝最新 PyTorch？(y/n): ").strip().lower()
        if response != "y":
            print("已取消安裝")
            return

    # 4. 卸載舊版本
    uninstall_pytorch()

    # 5. 安裝新版本
    if not install_latest_pytorch():
        print("\n✗ 安裝失敗，結束")
        return

    # 6. 驗證安裝
    verify_installation()

    print("\n" + "=" * 60)
    print("✨ 完成！")
    print("=" * 60)
    print("\n💡 提示：")
    print("- 如需指定版本，可使用：pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124")
    print("- 查看官方安裝指南：https://pytorch.org/get-started/locally/")
    print()


if __name__ == "__main__":
    main()

