# 超簡単ビルドガイド

## 方法1: Docker（推奨）

### 1. Docker Desktopをインストール
- https://www.docker.com/products/docker-desktop
- インストーラーをダブルクリックして次へ進むだけ
- 再起動が必要かも

### 2. ビルド！
CppOSフォルダで：
```cmd
docker-build.bat
```

→ 自動的にLinux環境が作られてビルドされます
→ `build/cppos.bin` が生成されます

---

## 方法2: オンライン（ブラウザのみ）

### GitHub Codespaces（無料）
1. GitHubにCppOSをアップロード
2. リポジトリ画面で「Code」→「Codespaces」→「Create codespace」
3. ブラウザでVS Codeが開く
4. ターミナルで：
   ```bash
   make
   ```
5. 生成された`cppos.bin`をダウンロード

### GitPod（無料）
1. https://gitpod.io にログイン
2. GitHubリポジトリURLを入力
3. ブラウザで開発環境が起動
4. ターミナルで `make`

---

## 方法3: クラウドVM（無料枠）

### AWS Cloud9 / Google Cloud Shell
- ブラウザでLinux環境
- 無料枠で十分ビルド可能

---

## 💡 一番簡単なのは？

| 方法 | 難易度 | 所要時間 |
|-----|-------|---------|
| Docker | ⭐⭐ | 10分 |
| GitHub Codespaces | ⭐ | 5分 |
| GitPod | ⭐ | 5分 |

**初心者には「GitHub Codespaces」が最も簡単です！**
