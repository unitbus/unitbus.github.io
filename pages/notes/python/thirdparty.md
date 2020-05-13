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

PySideもサードパーティ製になるが、良く使うので別ページに記載。

# numpy

画像を扱うなら必須になると言ってもいいライブラリ。ndarray配列が強力。
`nan` `inf` を扱えるのも特徴。

## 参考

> note.nkmk.me
https://note.nkmk.me/

> numpy で nan と数値の比較に関する warning を出さないようにする
https://qiita.com/f0o0o/items/61e4b62a03801b73370e

# Pillow

Pillowは、PILのフォーク(派生版)らしいです。
PILは、2011年に開発中止してるらしいので、後継版とも言えるかも。

こいつのおかげで、イメージ操作がシンプルに出来る。
自分で頑張る場合は、numpy使う事になる。

Pillow内でも、ndarrayがよく使われてる。

# py2exe

`Python2`を使ってる間は、スタンドアローンアプリを作る際にお世話になる。
他にも、Pyinstallerとかあるが、ファイルサイズが肥大化しがちなのであまり使ってない。

## 参考

http://blawat2015.no-ip.com/~mieki256/diary/201210021.html

## アイコン

`PySide`に`.ico`などの画像ファイルをリソースに含めても、pythonからは認識するが、
exeにすると読み込めなくなる。インストール先に、dllが別ファイルであるので一緒に含める必要がある。

`<Pythonインストールディレクトリ>\site-packages\PySide\plugins\imageformats`

``` python
from distutils.core import setup
setup(
    data_files = [
        (r'.\imageformats', [
            r"{}\plugins\imageformats\qico4.dll".format(pysideDir),
            r"{}\plugins\imageformats\qgif4.dll".format(pysideDir),
            ]),
        ],
    # 他省略
    )
```

## マルチプロセスエラー

```
Unknown option: --
```

pythonのmultiprocessingは、実プロセスを複数起動するので、
exe化する時は、 `__main__`に以下のコマンドが必要。

``` python
multiprocessing.freeze_support()
```

`multiprocessing.set_executable` も試したが、python.exeの切り替えは出来ても、
`freeze_support`が無効になってしまって、対応策がわからないのでオミット。

## PILのインポートエラー

``` python
ImportError, "No module named " + qname
```

と出る場合は、以下の部分をコメントアウトする。
オリジナルを変更したくない場合は、コンパイル用の環境を作ってパスを通す。

`.\python\v2.7.15\Lib\site-packages\PIL\__init__.py`

``` python
__doc__ = __doc__.format(__version__)  # include version in docstring
```

## 相対パスエラー

``` python
ImportError, "relative importpath too deep"
```

batファイルで、py2exeに渡す.pyファイルの中に、相対で読まれるまれてるモジュールがあると出るエラー。
パッケージ内で使う分には問題なさそう。パッケージ内に呼び出し用の`.py`を置いてる場合は注意。

``` python
# from . import define
# ↓
from package import define
```

## DLLパス

DLLが見つからないエラーが出る時は、以下を `%PATH%` に追加。

```
<python>\v2.7.15\DLLs
<site-packages>\numpy\.libs
```

## その他

コンパイルオプションでwindowモードにすると、
テキストに出力しない限りコンソールの内容が確認出来ない状態になるので注意。

stderrに書き込まれると、`<exeName>.log`が出力される。
