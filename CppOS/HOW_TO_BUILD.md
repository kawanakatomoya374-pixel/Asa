# ビルド済みバイナリの入手方法

## 方法1: GitHub Releasesからダウンロード（推奨）

1. [Releasesページ](https://github.com/YOUR_USERNAME/CppOS/releases) にアクセス
2. 最新バージョンの `cppos.bin` をダウンロード
3. `releases/` フォルダに配置
4. `run.bat` (Windows) または `./run.sh` (Linux/macOS) で実行

## 方法2: GitHub Actionsからダウンロード

1. [Actionsタブ](https://github.com/YOUR_USERNAME/CppOS/actions) を開く
2. 最新の成功したビルドをクリック
3. 「Artifacts」セクションから `cppos-kernel` をダウンロード
4. ZIPを解凍して `cppos.bin` を `releases/` フォルダに配置

## 方法3: 自分でビルド

### Windows (MSYS2)
```bash
# MSYS2をインストール: https://www.msys2.org/
pacman -S gcc nasm make qemu

# ビルド
cd CppOS
make

# 実行
make run
```

### Windows (WSL2)
```bash
# WSL2でUbuntuをインストール後
sudo apt-get update
sudo apt-get install gcc g++ nasm make qemu-system-x86

# ビルド
cd /mnt/c/Users/YourName/CppOS
make

# 実行
make run
```

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install gcc g++ nasm make qemu-system-x86

# Fedora
sudo dnf install gcc gcc-c++ nasm make qemu-system-x86

# Arch
sudo pacman -S gcc nasm make qemu-full

# ビルド
make && make run
```

### macOS
```bash
# Homebrewでインストール
brew install nasm qemu

# 注意: macOSでは32-bitクロスコンパイラが必要です
# DockerまたはLinux VMでのビルドを推奨
```

## バイナリの検証

ダウンロードしたバイナリが正しいか確認：

```bash
# ファイルサイズ確認（約4-8KBが正常）
ls -la releases/cppos.bin

# QEMUでテスト実行
qemu-system-i386 -kernel releases/cppos.bin -serial stdio
```

正常に動作すると、以下が表示されます：
- 緑色のテキスト: `=== CppOS v0.1 ===`
- 白色のテキスト: `Hello from C++ kernel!`
