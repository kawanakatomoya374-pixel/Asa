# CppOS

C++で書かれた小さな教育用オペレーティングシステムです。

> **🚀 ビルド済みバイナリをお探しですか？**  
> [Releasesページ](../../releases) から `cppos.bin` をダウンロードできます！  
> 詳細は [`HOW_TO_BUILD.md`](HOW_TO_BUILD.md) をご覧ください。

## 概要

CppOSは、C++を使用して開発されたシンプルなx86オペレーティングシステムです。
Multiboot2標準に準拠し、GRUBブートローダーで起動できます。

## 機能

- **VGAテキストモード**: 画面への文字表示
- **シリアルポート出力**: COM1ポートによるデバッグ出力
- **C++カーネル**: モダンC++で記述されたカーネル
- **Multiboot2対応**: GRUB互換のブート方式

## 🚀 クイックスタート（GUIランチャー）

**最も簡単な方法**: Python GUIランチャーを使用

### Windows
```bash
# 1. QEMUをインストール（初回のみ）
# https://qemu.weilnetz.de/w64/

# 2. ランチャーを起動
quick_run.bat
# または: python launcher/cppos_launcher.py
```

### またはスタンドアロンEXEを使用
`releases/CppOS.exe` をダブルクリックするだけ！
（カーネル内包版、QEMUのみ別途インストールが必要）

## クイックスタート（コマンドライン）

```bash
# ビルド済みバイナリで実行
./run.sh        # Linux/macOS
run.bat         # Windows

# または直接QEMU
qemu-system-i386 -kernel releases/cppos.bin -serial stdio
```

## プロジェクト構造

```
CppOS/
├── src/
│   ├── boot/
│   │   └── boot.asm      # ブートローダー（Multiboot2対応）
│   └── kernel/
│       ├── io.hpp        # I/Oポート操作
│       ├── kernel.cpp    # カーネルメイン
│       ├── linker.ld     # リンカースクリプト
│       ├── serial.cpp/hpp # シリアルドライバ
│       ├── string.hpp    # 文字列ユーティリティ
│       └── vga.cpp/hpp   # VGAドライバ
├── build/                # ビルド出力（自動生成）
├── releases/             # ビルド済みバイナリ
│   ├── cppos.bin         # カーネルバイナリ（ビルド後に配置）
│   └── CppOS.exe         # GUIランチャーEXE（オプション）
├── launcher/             # GUIランチャーアプリ
│   ├── cppos_launcher.py # Pythonランチャー
│   └── build_launcher.py # EXEビルドスクリプト
├── quick_run.bat         # クイック起動バッチ
├── run.bat               # Windows用ランチャー
├── run.sh                # Unix用ランチャー
├── build.sh              # クロスプラットフォームビルドスクリプト
├── Makefile              # ビルドシステム
└── README.md             # このファイル
```

## 必要条件

- `g++` (i686ターゲット、または-multilib対応)
- `nasm` (アセンブラ)
- `ld` (リンカー)
- `grub-file` (Multiboot検証)
- `grub-mkrescue` (ISO作成、オプション)
- `qemu-system-i386` (テスト実行)

### Windowsでのセットアップ

#### 方法1: MSYS2（推奨）
```bash
pacman -S gcc nasm make qemu
```

#### 方法2: WSL2 (Windows Subsystem for Linux)
```bash
# WSL2でUbuntuをインストール後
sudo apt-get install gcc g++ nasm make qemu-system-x86
```

## ビルド

### Makefileを使用
```bash
# カーネルのビルド
make

# ISOイメージの作成
make iso

# ビルドファイルの削除
make clean
```

### クロスプラットフォームビルドスクリプト
```bash
# 自動的に環境を検出してビルド
./build.sh
```

## 実行

### 簡単実行（推奨）
```bash
# Unix系（Linux/macOS/MSYS2）
./run.sh

# Windows
run.bat
```

### Makefileから実行
```bash
# カーネルを直接QEMUで実行
make run

# ISOイメージをQEMUで実行
make run-iso

# GDBデバッグモードで実行
make debug
```

### QEMUを直接実行
```bash
qemu-system-i386 -kernel releases/cppos.bin -serial stdio
```

### 注意: バイナリ形式について
- `cppos.bin` は **ELFではありません** - OSのカーネルバイナリです
- WindowsのEXEファイルとは異なり、QEMUエミュレータで実行します
- 実際のハードウェアでは、GRUB2ブートローダーまたはMultiboot2対応ブートローダーで起動できます

## 技術仕様

- **アーキテクチャ**: x86 (32-bit)
- **ブート方式**: Multiboot2
- **ベースアドレス**: 1MB
- **スタックサイズ**: 16KB
- **C++標準**: C++11以上（`-fno-exceptions -fno-rtti`使用）

## 今後の拡張予定

- [ ] 割り込み処理（IDT/PIC）
- [ ] キーボードドライバ
- [ ] メモリ管理（ページング）
- [ ] システムコール
- [ ] プロセス管理
- [ ] ファイルシステム

## ライセンス

教育目的のプロジェクトとして自由に使用・改変可能です。
