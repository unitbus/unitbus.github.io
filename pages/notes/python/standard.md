---
layout: default
title: Python2 Standard Library
---

<!-- # Python Standard Library -->

# pprint

prettyPrintの略らしい。いい感じに折り返して文字列として表示してくれる。
コンソールの幅に合わせて、デフォルト80文字になってる。

文字列として欲しい場合は、`pprint.pformat()`を使う。
`unicode-escape`でエンコードされた`<str>`文字列が返ってくるので、
日本語含んでても、文字化けしますが`print`で出力出来ます。

文字化けが嫌なら、デコードして`<unicode>`に戻して`print`すれば日本語表示出来ます。

``` python
text = pprint.pformat(u'日本語の文章\n長さは関係ない')
print(text.decode('unicode-escape'))
```

辞書や、配列などに日本語を含む場合は、事前に`<str>`を`<unicode>`に変換しておけば、
`unicode-escape`でデコードすれば、`<unicode>`に戻ります。

``` python
text = pprint.pformat([u'日本語その1', u'日本語その2'], width=0)
print(text.decode('unicode-escape'))
```

注意する点は、別の文字コードでエンコードしたasciiを`pformat`へ渡すと、
`unicode-escape`で再エンコードされてしまう点です。再エンコードされた文字は元に戻らなくなります。
`unicode-escape`でデコードしようとするとエラーになったりするので、注意してください。

良くわからない人は、`pprint.pprint()`の方を使って、文字化けしてるけどエラー出ないからいいや。
って覚えるのもありかもしれません。

# subprocess

**※ 日々試行錯誤中で、間違った情報が混ざってる可能性あります。**

Peopenで、プロセスが非同期に開始する、終了を待つ場合は、`wait()`で待機する。
処理を待たず、非同期でよければ、マルチプロセスの代わりに使う事も可能。
テクスチャのコンバートとかに使える。

`subprocess.SW_HIDE`は最小化ではなく完全隠蔽。

## shell

`shell=True`の場合、osのshellを経由する(windowsの場合はcmd.exe)
プロセスツリーを見るとcmd.exeが親に付く。
startコマンドを使う時は、`shell=True`にしないといけない。

`shell=False`の場合はwindow標準コマンド(copyとか)を直接叩け無いので注意。
外部アプリケーションを使う場合は、基本`False`でOK。
バッチファイルを動かす時も、`shell=False`で大丈夫。

windowsの場合、`cmd`を省略して書けるってだけで、`shell=False`でも、
`cmd /K copy "A" "B"`みたいに書けば動く。

## env

過去にenvを指定すると、子のプロセスで環境変数が変更できない？現象があったが多分勘違い。
standaloneでは起きなかったので、Mayaでも確認したが再現不可。

`None`だと現在の環境を引き継ぎ、空の辞書にして渡すとosに必要な情報まで欠如する。
envが空だと動作がおかしくなって基本動かないので、
`os.environ.copy()`してから、追加や削除するのがベター。

## stdout, stderr

標準エラーと、標準出力を共有するには、stdoutに`PIPE`を渡し、stderrに`STDOUT`を渡す。
batで書く時に、`cmd > log.txt 2>&1`とやってる事は同じ。

新しいコンソールに標準出力したい場合は、stdoutは指定せずNoneのままにしておく。

`stdout`に`subprocess.PIPE`を渡すことで、標準ストリームにアクセスできるようになる。
結果が欲しければ、`communicate`を使うと、処理の終了を待機してから取得する事になる。
`communicate`は全文をメモリに溜め込むので、長文が予想される場合は、ドキュメントでは非推奨になってる。

`stdout.fileno()`でファイルデスクリプタからリアルタイムに取得する事も可能

`file.fileno()`が返すのは、ファイルではなく**ファイルデスクリプタ(記述子)**、通称**FD**。
ファイルデスクリプタは、`closefd=False`にしないとプロセス終了時に閉じようとして失敗するので注意。

```python
from subprocess import Popen, PIPE, STDOUT
proc = Popen(cmdline, stdout=PIPE, stderr=STDOUT)

with io.open(proc.stdout.fileno(), mode='rt', closefd=False) as bufferIo:
    for i, textLine in enumerate(bufferIo):
        print(i, textLine.rstrip())

proc.wait()
```

## stdin

`stdin`を空にすると、subprocessが呼び出せないアプリがある。
逆に、`stdin`に`os.devnull`を入れると、キー入力を待つコマンドが使用不可になる。
バッチに、`sleep`や、`timeout`を使用してる場合、待機せず即座に進む。多分、YES/NO系も駄目。

pythonwで、io.openだと起動できない？事があった。

devnull = open(os.devnull, "wb")
devnull = io.open(os.devnull, "wb")
devnull = codecs.open(os.devnull, "wb")

デバッグ用のヌルで代用すると良いらしい。終わったら一応閉じる。

devnull.close()

# ファイル読み書き

基本、どのモジュールも、デフォルトがテキストモードで、unicodeにデコードされる。
bytesのまま読むにはバイナリモード`rb`にする必要がある。

`os.linesep`は、公式ドキュメントでファイルの書き込みで非推奨とされ、`\n`を使う事が推奨される？

`errors='ignore`はエンコードエラーを防げるおまじないだが、情報が欠如するので注意。

## open(組み込み関数)

python2.7.15の組み込み関数open()だとencodingが変更できず`utf-8`になる。

ファイルから取得した文字列に日本語含まれてた場合、
windowsコンソールの標準出力にprintするとエンコードエラーを起こす。

2019年現在では、メモ帳が`cp932`な為、batファイルとかも`cp932`で書かれてることが多いので注意。
`Windows 10 19H1`からデフォルトが、`UTF-8`になるらしいです。

```python
writeIo = open(logPath, 'w')
```

## io.open

python2系はmode指定しないと`rt`でテキストモードに読まれ、encodingの指定がない場合は、
デフォルトエンコーディングが適用され`unicode`で返される(io.openのドキュメント参照)。

ファイルデスクリプタ(file.fileno)を扱える、python2では唯一？のモジュール。

```python
writeIo = io.open(logPath, 'wt', encoding='cp932', errors='replace')
```

## codec.open

デフォルトのエンコーディングは`ascii`です(codec.openのドキュメント参照)。
ファイル操作はおまけで、エンコードに特化したモジュール？

```python
writeIo = codecs.open(logPath, 'w', encoding='cp932', errors='replace')
```
