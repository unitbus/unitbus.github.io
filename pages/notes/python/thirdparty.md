---
layout: default
title: Python
---

# Python Thirdparty

## 基本

`pip`でインストールすると、デフォルトでは `site-packages` に配置される。
インストール先を変更できるが、パッケージを使うときはなるべく同じディレクトリにまとめた方が良い。

パッケージ名の重複を防げたり、PYTHONPATHに設定するパスが多すぎると、
パッケージの検索に時間がかかり、アプリケーションの起動が遅くなる。

## numpy

画像を扱うなら必須になると言ってもいいライブラリ。ndarray配列が強力。
`nan/inf` を扱えるのも特徴。

### 参考

> note.nkmk.me
https://note.nkmk.me/

> numpy で nan と数値の比較に関する warning を出さないようにする
https://qiita.com/f0o0o/items/61e4b62a03801b73370e
