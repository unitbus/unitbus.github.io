---
layout: default
title: Python2 Basic
---

<!-- # Python Basic -->

# 全般

## 基本

Pythonは、すべての変数、関数がオブジェクトで、ルールが統一されている。
ファイル構成も、クラスもパッケージも、同じ考え方で慣れると色々スッキリする。

オレオレ仕様で頑張っても、正規ルートから外れたルールだといずれ詰む。

## 参考

> [PythonMatrixJp: Pythonのモジュールインポートのしくみ](http://python.matrix.jp/pages/tips/import.html)

# 組み込み関数(Built-in)

python.exeのビルド時に標準で搭載してる関数たち。

> [Built-in](https://unitbus.github.io/pages/notes/python/builtin)

# Class

クラスの中で定義された関数は、**クラスメソッド**と呼ぶ。
変数は、**クラスメンバ**と呼ぶ。それぞれ意味は変わらない。

**Class**の構造は、**Package**のファイル構造と同じ。

# Package

インストールディレクトリを見るのが分かりやすい。

## Standard Library

インストール時に、最初から付いてくるライブラリ。
インストール先は、`<python>\Lib`。

> [Standard Library](https://unitbus.github.io/pages/notes/python/standard)

## Thirdparty

外部からダウンロードした**Package**を指す。
インストール先は、デフォルトだと`<python>\Lib\site-packages`。

> [Thirdparty](https://unitbus.github.io/pages/notes/python/thirdparty)

# 文字列

## 基本

**※ 日々試行錯誤中で、間違った情報が混ざってる可能性あります。**

## エンコード

Pythonで扱う文字列には、`<str>`, `<unicode>`の2つしかない。
`encode`と`decode`とでてくるが、目的は明確。

``` yaml
encode: <unicode>から<str>に変換
decode: <str>から<unicode>に変換
```

Python内すべての文字列操作は、`<unicode>`を推奨してると思ってもいいので、
なるべく`<unicode>`で扱う。なので、`<str>`に変換する事をエンコードと呼ぶと思われ。

エンコードで調べると、色々(`cp932`, `shift_jis`, `utf16`, `utf8`, `ascii`)と出てくるが、すべて`<str>`に変換する際の形式の話になる。ざっくり総称で、**文字コード**と呼ばれたりする。

`bytes`と言う単語も出てくるが、文字コードを適用しない素(raw)の状態にを指す。
つまり、Pythonの場合、エンコードする前の文字列は、`<str>`と同意語と思って良いかと。
逆に、エンコードしないと文字化けて読めない`<str>`文字列を、マルチバイトと呼ぶ。

**Pythonの型**と、**文字コード**は別って事がわかってないと、どのサイトの説明を見ても混乱する。

では、2つしかないのに、なぜあんな面倒でイライラするUnicodeEncodeErrorが頻発するかと言うと、
外部プロセスに渡したり、Python内の文字列自動変更の場合が多い。

注意すべきなのは、以下のとき。

- コンソールに出力
- コマンドで実行
- ファイルから文字列取得
- その他自動変更

python2だと、`os.sep`や、`split`系関数が`<str>`として扱う傾向があるので、
`<unicode>`と足したりするとエンコードエラーを起こす事がある。

### コンソールに出力

`print`使うときは、`<unicode>`に変換してから行う。実際に出力される文字は`<str>`なのだが、
コンソールの環境によって出力できる文字コードが違うので、自動変換に任せる。

`sys.stdout`に直接アクセスする場合は、自分でエンコードをコントロールする必要がある。

### コマンドで実行

`os.system`, `subprocess`を使う場合は、事前に`<str>`に変換する必要がある。
内部で、`format`使った文字列処理されてて、`<str>`を混在した変換が行われる為と思われる。

※ Python3になると、メインが`<unicode>`なので問題なくなるかも、まだ触ってないので未確認。

### ファイルから文字列取得

`encoding`を指定しないでファイルを書き込む際は、`<str>`に変換して渡す？
`unicode_literals`の有無で対応が変わる？

`unicode_literals`を使ってる場合は、`unicode`で渡さないとエラーになる。

### その他自動変更

`__future__.unicode_literals`環境でformatを使った文字操作で、
`<unicode>`の自動変換が入る(`r`付けた場合も`<unicode>`)。

`unicode_literals`を使用してない場合は、`u`を付けると`<unicode>`へ自動変換される。
逆に、`u`以外はすべて`<str>`になるので注意。
raw文字も`<str>`なので、`<unicode>`でraw文字使いたい場合は、`ur`を頭に付ける。

Python3では、デフォルトエンコーディングが`<unicode>`になったので、トラブルは減る気がするが、
Python2のコードそのまま変換すると混乱が起きそうな予感。
特におまじない的に処理書いてる場合は注意。

## 参考

> 日本語文字列コード問題まとめ
http://python.matrix.jp/pages/tips/string/encoding.html#id4


> 【Python】文字列と数値（asciiコード）の変換まとめ
https://qiita.com/ell/items/6eb48e934a147898d823


# デフォルトエンコーディング

デフォルトエンコーディングを変更してた時期があったが、あまり意味ない気がしてきたのでオミット中。

デフォルトで持ってるエンコードがバラバラで、他のモジュールの動作にも影響出てくるので、
使用時に、目的に応じて指定するのが結局良いと思われる。

戒めとして、過去のメモを残しておきます。

## 標準入出力のエンコーディング(sys.stdout.encoding)

windows7, 10のコマンドプロンプトのデフォルトは、`cp932`になる。

```python
print('stdoutEncoding:', sys.stdout.encoding)
```

## Pythonエンコーディング(default Encoding)

python.exeを実行した場合のコンソールのデフォルトは、`ascii`になる。
python起動前に環境変数(PYTHONIOENCODING)で変更する事ができる。
python3は、環境依存関係なくすべて`utf8`になる。

```python
print('defaultEncoding:', sys.getdefaultencoding())
```

sysモジュールをreloadすると、setdefaultencodingで変更が反映されるようになる。

```python
reload(sys)
sys.setdefaultencoding('cp932')
```

## filesystem encoding

コマンドラインの引数や、ファイルパスに使われる。

```python
print('systemEncoding:', sys.getfilesystemencoding())
```

## preferred encoding

ファイルを開く時に使われる。組み込み関数の`open`が指すデフォルトは多分こいつ。

```python
print('preferredEncoding:', locale.getpreferredencoding())
```

## 参考

> Python 3の各種エンコーディングについて
https://qiita.com/methane/items/6e294ef5a1fad4afa843

> ikuliの日本語の文字化けに悩まない！【文字コードを攻略しよう】
http://marukentokyo.jp/2018/10/30/sikulix_character/

