# GitHub Codespaces 完全ガイド

## ステップ1: Codespaceを作成

1. GitHubのCppOSリポジトリを開く
2. **緑色の「<> Code」ボタン** をクリック
3. **「Codespaces」タブ** をクリック
4. **「Create codespace on main」** ボタンをクリック

→ ブラウザでVS Codeが開きます（待ち時間1-2分）

---

## ステップ2: ターミナルを開く

VS Codeが開いたら：

**方法A: メニューから**
- 画面上部のメニュー → **Terminal** → **New Terminal**

**方法B: ショートカット**
- `` Ctrl + ` `` （バッククォート、Escキーの下）

→ 画面下部にターミナルが開きます

---

## ステップ3: 正しいフォルダに移動

ターミナルに以下を打ちます：

```bash
# 現在の場所を確認
pwd
# → /workspaces/CppOS などと表示されるはず

# フォルダの中身を確認
ls
# → Makefile, src/, README.md などが見えるはず

# もしCppOSフォルダが見えたら入る
# cd CppOS  # ← 必要なら

# ビルド！
make
```

---

## ステップ4: ビルド結果を確認

```bash
# buildフォルダにカーネルができたか確認
ls build/
# → cppos.bin が表示されるはず

# ファイルサイズを確認
ls -lh build/cppos.bin
# → 約4-10KBぐらい
```

---

## ステップ5: ファイルをダウンロード

1. **左側のファイルツリー**（Explorer）で `build/` フォルダを開く
2. `cppos.bin` を見つける
3. **右クリック** → **「Download」** を選択
4. ダウンロードされたファイルを `CppOS/releases/` フォルダに移動

---

## よくあるエラーと対処法

### ❌ "No targets specified and no makefile found"
**原因**: フォルダが違う

**対処**:
```bash
# どこにいるか確認
pwd

# CppOSフォルダに移動（必要なら）
cd CppOS

# 上のフォルダに移動（必要なら）
cd ..

# もう一度make
make
```

### ❌ "command not found: make"
**原因**: makeがインストールされていない

**対処**:
```bash
# Ubuntuの場合
sudo apt-get update
sudo apt-get install make

# それでもダメならgccも
sudo apt-get install gcc g++ nasm
```

### ❌ ファイルがダウンロードできない
**対処**: ターミナルでコピーして表示
```bash
cat build/cppos.bin | base64
```
→ 表示された文字列をWindows側でデコード

---

## 💡 コツ

- **ターミナルが消えたら**: `` Ctrl + ` `` で再表示
- **ファイルが見えない時**: 左のExplorerで「Refresh」
- **操作をやり直したい**: ターミナルで `cd ~` してから `cd /workspaces/CppOS`

---

## 🚀 超簡略化まとめ

1. 「<> Code」→「Codespaces」→「Create codespace」
2. 待つ（1-2分）
3. `` Ctrl + ` `` でターミナル開く
4. `make` と打つ
5. `build/cppos.bin` ができたら右クリックでDownload
