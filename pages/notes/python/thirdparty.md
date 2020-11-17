---
layout: default
title: Python2 Thirdparty
---

# Thirdparty

`pip`でインストールすると、デフォルトでは `site-packages` に配置される。
インストール先を変更できるが、パッケージを使うときはなるべく同じディレクトリにまとめた方が良い。

パッケージ名の重複を防げたり、PYTHONPATHに設定するパスが多すぎると、
パッケージの検索に時間がかかり、アプリケーションの起動が遅くなる。

PySideもサードパーティ製になるが、別言語と言っていいぐらい情報量多いので別ページに記載。

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

`Python3`になると、`py2exe`がなくなるので、`Pyinstaller`にお世話になりそうだが、
移行してから考えることにしてる。

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

## コンパイル

パッケージで作成してる場合は、`__main__.py`を利用すると邪魔にならなくていい。
`__main__.py`を作っておけば、`python.exe`に`-m`フラグでテストできるようになる。
これだけでもアプリケーションっぽい動作するので、デバッグモード時は切り替えたりとかもあり。

``` bat
python.exe -m "package_name"
```

コンパイルする時は、`py2exe`のオプションで、script部分に`__main__.py`を指定してする感じ。

``` python
# _setup.py 色々割愛

console_option = {
    'script': r'{}\__main__.py'.format(scriptDir),
    }

setup(
    console = [console_option],
    )
```

``` bat
python.exe "_setup.py" py2exe
```

## その他

コンパイルオプションでwindowモードにすると、
テキストに出力しない限りコンソールの内容が確認出来ない状態になるので注意。

stderrに書き込まれると、`<exeName>.log`が出力される。

# MkDocs

markdownから、いい感じにコマンドリファレンスみたいなサイトを作ってくれる、pythonパッケージ。
`site-packages\bin`に、環境変数の`PATH`を通せば、`mkdocs.exe`をスタンドアローンでも使える。

スタンドアローンでも使えるので、pythonのバージョンも最新の使って、pipで入れれば簡単に環境が揃う。
python2で頑張ると、テーマがなかったり、pipでコケたりと大変なだけなので、割り切った方が楽だった。

ちなみに、`.py`をパースしてdocstringだけ抽出する機能は無いので、そこは自作した。
`inspect`モジュールで、いい感じにdocstringを拾えるので、後は`dir`とか使って頑張る感じ。

markdown直接書いて、`.md`ファイル置いておけば拾ってくれるので、
スクリプトに埋め込みたくない人は、最初からドキュメントを別に分けしまえばいい。

ルートフォルダ作って、`mkdocs.yml`を作成。同階層に`docs`フォルダ作成してmarkdown置き場にする。
ルートフォルダをカレントディレクトリにして、`mkdocs.exe`叩かないと動作しないので注意。

htmlサーバーが無くても、ローカルホスト(`mkdocs.exe serve`)で見れるので便利。
この辺の説明は詳しく書いてるのがいっぱいあるので割愛。

## mkdocs.yml

基本的な変更は`mkdocs.yml`でほぼ出来る。
以下はデフォルトから変更したところ。

### breaks

改行を書いたまま表示。スペース２個後ろに付けるの嫌な場合は設定。
`New Line to Break.`の略らしい。略されてるのがわからず、見つけるのに苦労した…。

``` yaml
markdown_extensions:
    - nl2br
```

### theme

色々試したが、右にTOCが欲しいので`material`をチョイス。

ダークテーマがよかったので、cssだけ別のを適用。

> mkdocs-material-dark-theme
https://github.com/fmaida/mkdocs-material-dark-theme

自分でcssを拡張したい場合は、別ファイルで追加して、
`.md-container`みたいなのを探して、書き換えてあげる感じ。

FireFoxとかで、プレビュー中のHTMLを`要素の調査`で、cssを直接いじるとわかりやすいかった。

```yaml
theme:
    language: 'ja'
    name: 'material'

extra_css:
    - "styles/extra.css"
    - "styles/style.css"
```

### TOC問題

TOC自体は標準エクステンションなので、`mkdocs.yml`で追加できる。

```yaml
markdown_extensions:
    - toc:
        permalink: True
        separator: "-"
        toc_depth: 3
```

TOCが１個目の、`h1`以下の`h2`以下しか表示されない。
バグかと思ったが、作者的に`h1`はタイトルだから１個だろ。と譲らない模様。

> mkdocs-material issues
https://github.com/squidfunk/mkdocs-material/issues/818

１ページに、複数の`h1`を保つ場合は、テンプレートから３行を削除すれば、通常のTOCが作れる。
`site-packages\material\partials\toc.html`
バージョンによって違うかもしれないが７行目付近。

<!-- {% raw %} -->
```html
  {% if toc | first is defined and "\x3ch1 id=" in page.content %}
    {% set toc = (toc | first).children %}
  {% endif %}
```
<!-- {% endraw %} -->
