# CppOS Launcher

ダブルクリック一つでCppOSを実行できるGUIランチャーです。

## 機能

- ✅ **ワンクリック実行**: QEMUを自動検出・実行
- ✅ **GUIコンソール**: OSの出力をウィンドウ内で表示
- ✅ **自動検出**: QEMUをPATHや標準インストール先から自動検索
- ✅ **スタンドアロン**: カーネルを内包した単一EXEファイルとしてビルド可能

## クイックスタート

### 方法1: スタンドアロンEXEを使用（推奨）

1. `releases/CppOS.exe` をダブルクリック
2. 「Run CppOS」ボタンをクリック
3. 完了！OSが起動します

### 方法2: Pythonスクリプトを実行

```bash
cd launcher
pip install -r requirements.txt
python cppos_launcher.py
```

## ビルド方法

### スタンドアロンEXEを作成（カーネル内包）

```bash
cd launcher
python build_launcher.py
# オプション1を選択
```

これにより `releases/CppOS.exe` が作成されます。
このEXEは単独で動作し、外部ファイルは必要ありません。

### ランチャーのみを作成（外部カーネル使用）

```bash
cd launcher
python build_launcher.py
# オプション2を選択
```

これにより `releases/CppOS-Launcher.exe` が作成されます。
このEXEは `releases/cppos.bin` を必要とします。

## 必要条件

- **Windows**: QEMU for Windows (qemu-system-i386.exe)
- **Linux**: qemu-system-x86 パッケージ
- **macOS**: qemu (Homebrewでインストール)

### WindowsでのQEMUインストール

1. [QEMU for Windows](https://qemu.weilnetz.de/w64/) からダウンロード
2. インストーラーを実行
3. インストール先をPATHに追加（通常自動）

または MSYS2:
```bash
pacman -S qemu
```

## スクリーンショット

```
┌─────────────────────────────────────┐
│ 🖥️ CppOS Launcher                   │
├─────────────────────────────────────┤
│ C++ Operating System - Run CppOS    │
│ instantly with QEMU                 │
├─────────────────────────────────────┤
│ Status                              │
│ ✅ QEMU: C:\Program Files\...       │
│ ✅ Kernel: releases\cppos.bin       │
├─────────────────────────────────────┤
│ [▶️ Run CppOS] [🛑 Stop] [ℹ️ About]│
├─────────────────────────────────────┤
│ Console Output                      │
│ ┌───────────────────────────────┐  │
│ │CppOS: Kernel started          │  │
│ │CppOS: Kernel init complete    │  │
│ │=== CppOS v0.1 ===             │  │
│ │Hello from C++ kernel!         │  │
│ └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## ファイル構成

```
launcher/
├── cppos_launcher.py       # メインランチャースクリプト
├── build_launcher.py       # EXEビルドスクリプト
├── requirements.txt        # Python依存パッケージ
└── README.md              # このファイル
```
