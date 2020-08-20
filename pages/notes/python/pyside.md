---
layout: default
title: Python PySide
---

# 基本

PySideは難しいと敬遠されるが、実はpythonで使えるUIの中で一番シンプルで、ルールが統一されてる。
以下のコードが、スタンドアローンで、最低限必要とするコマンド。

```python
from PySide.QtGui import *
app = QApplication([])
button = QPushButton('test')
button.show()
app.exec_()
```

mayaだと、3行で済む。

```python
from PySide.QtGui import *
button = QPushButton('test')
button.show()
```

なぜ、`QPushButton`で、`show()`メソッドが使えて、表示出来るのか？がわかるとPySideが楽しくなる。

`exec_()`を実行する事で、イベントループになる。
この場合、`QApplication`を作成し、standaloneソフトとして待機させてる状態になる。
`exec_()`は、ダイヤログや、メニュー、スレッドでも出てくるので、覚えておくと便利。

# Document & Reference

> [PySide 1.0.7 Reference](https://srinikom.github.io/pyside-docs/)

> [PySide 1.2.1 Reference](https://pyside.github.io/docs/pyside/index.html)

> [Qt for Python(PySide2)](https://doc.qt.io/qtforpython/)

**PySide 1.2.1 Reference** では、継承図が表示されないのでちょっと不便。

そろそろPySide1は切り捨てて書いても良い気もしますが、まだ互換性考えて、
**PySide 1.0.7 Reference** の方を見て書いてます。

# Widget一覧

ウィジェットを一覧で見れるビューワー。
mayaなどの、DCCでレイアウトを確認する時に便利。

<p>
<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowA.png" width="20%">
<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowB.png" width="20%">
<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowC.png" width="20%">
</p>

> [Dwonload / Standalone / Python / ubWidgetHierarchy](https://unitbus.github.io/pages/download)

ダウンロードしたファイルは、環境変数の **PYTHONPATH** が通ってる場所に置き、
以下のコマンドを実行してください。

```python
import ubWidgetHierarchy
ubWidgetHierarchy.show()
```

standaloneでも動きますが、他にウインドウを表示して無いと意味ないです。

こうやって見ると、**Houdini** はまだ、独自UIが多く、**Qt** を使ってない事がわかる。

# リスト関連

PySideのリスト系ウィジェットは、View(表示)と、Model(データ)が必要になります。
Viewの表示を装飾したりデコる場合は、デリゲーターが出てきますが説明は割愛。
Viewでの選択も、セレクションモデルって言葉が出てきますが、コレも説明は割愛。

ViewとModelの関係をワンセットにしたユトリウィジェットが、
QListWidget, QTableWidget, QTreeWidgetです。

QWidgetから色々継承してViewを作ったのに、またWidgetって呼び名に戻るのかい。
って個人的にはツッコミ入れたいところですが…。

小難しく言うと、Viewを継承し、Modelのメソッドを追加した拡張Viewです。
なので、Viewを自前で作る場合、もれなくModelが必要になります。

## QTableView, QTableWidget

`QListWidget.setItem()`のメソッドを使ってテーブルを作成すると、
一個づつしか追加できないので、数が多いと激重になります。

`QTableView`を使用し、`QAbstractListModel`を元に自分でModelを作成すれば、
不必要な機能に絞ってを減量出来き、まとめてデータを登録出来るようにすれば、かなり高速化出来ます(当社比約20倍)。

とは言え、かなりの知識と、準備が必要なり、汎用性には向きません。
汎用性考えて、下手に機能を盛れば、盛るほど遅くなります。

リスト対象のアイテムが、1万とか超えなければ、
`QTableView`と、`QStandardItemModel`の組み合わせで十分だったりします。
`QStandardItemModel.appendRow()`で、行単位で登録する事で、十分な高速化が出来ます。

## QTreeView, QTreeWidget

`QTreeWidget`&`QTreeWidgetItem`と、
`QTreeView`&`QAbstractItemModel`の組み合わせで比較してみたが、
`parent-1000 x child-1000`とかなり高負荷で試しても速度面的な恩恵はなかった。
TreeItemの書き方次第では、`QTreeView`の方が遅くなる場合もあった。

`QListView`や、`QTableView`と違い、かなりモデルが最適化されてるみたいで、
検索や、デリゲート使うような見た目の変更をしない限り`QTreeView`を使うメリットを感じなかった。

# その他

## QFileInfo
windowsのショートカット、".lnk"から実体を取得する方法。

D&Dした時のショートカットから元のリンクを取る方法

> https://kiwamiden.com/drag-and-drop-files-to-qlistview

D&Dイベントだと、QUrlにパスが入ってくるが、
ダイヤログとかで取得した場合は、一度`QFileInfo`に変換すると色々取得できる。

> https://kiwamiden.com/how-to-read-the-shortcut-file

## QMenu, QAction

`QMenu.addAction`で同じアクションを指定すると、一番下に再配置される。
この仕組み使ってソートも可能。

ドキュメントのメソッド一覧をみると、`QMenu.insertMenu`, `QMenu.insertSeparator`はあるのに、`insertAction`が見当たらない。
しばらく使えないものだと思ってたが、QWidget側に`QWidget.insertAction`が用意されてた。
なので、継承してるQMenuでも普通に使える。これに気付かず色々頑張ってしまった…。

`Qt`のドキュメントの方が見易いと教えてもらった。ありがとうtakkun。
クラス説明上の方の、下の文字のリンクをクリックすると、継承した後のメソッド一覧が確認できる。
`List of all members, including inherited members`

> https://doc.qt.io/qt-5/qmenu.html

## QTextEdit, QPlainTextEdit

PySideでテキストを表示せたい場合、`QTextEdit`, `QPlainTextEdit`の選択肢がある。
`QTextEdit`はかなり多機能なので、迷ったら`QPlainTextEdit`を使うのがオススメ。

結論から言うと、`QTextEdit`と比べて、`QPlainTextEdit`の`append`の処理が3倍以上速かった。
`setPlainText()`メソッドの場合、速度は誤差レベルだったが、スレッドでループさせ、都度クリアし、
描画待ち含めた速度比べると、体感でわかるぐらい断然に速く負荷が低い。時には10倍以上差が付く事があった。

`QTextEdit.append()`は、カーソルを最終行に移動して`insert`してるだけなので速度は変わらないが、
`QPlainTextEdit.appendPlainText()`はエリア外の描画処理省くのでかなり速い。

ちなみに、`QPlainTextEdit.moveCursor(QTextCursor.End)`で、常に最後の行を表示しながら、
`QPlainTextEdit.appendPlainText()`をしても、`QPlainTextEdit`の方が速いところや、
文章の長さによる速度比が変わらないところをみると、基礎部分がかなりテキストに最適化されてると思われる。

ドキュメントに書いてある通り、`QPlainTextEdit`はプレーンテキスト処理用に最適化されてるが、
htmlを使って基本的な装飾可能なので、基礎部分で速度差が出る以上、`QPlainTextEdit`を使う恩恵は高いと思われる。

調べてると、`QTextDocument`と言うキーワードが出てくるが、こちらは`QTextEdit`専用になる。
`QPlainTextEdit`に普通に適用しても描画されない。`QPlainTextDocumentLayout`を使えとか出てくるがよくわからないくなってきたので放置。

ViewとModelの関係に似てると思って期待したが、`QTextEdit`に必要なメソッドがほぼ全部揃ってる感じで、
なんかちょっと違う感。詳細な変更を加えない限りは触らなくていい感じ？かと。

`QTextEdit`に、素の`QTextDocument`を突っ込んで、
ドキュメント側で`QTextDocument.setPlainText()`しても、
速度的に変わらなかった。`setData()`的なのがあれば期待通りなのだが…。

# Convert

`pyside-uic.exe`を使うと、`designer.exe`で作成した、`.ui`ファイルを、`.py`に変換出来る。

`<Python>\Lib\site-packages\PySide\designer.exe`
`<Python>\Scripts\pyside-uic.exe`

以下のエラーが出る場合は、pipで、osに合わせて正しいバージョンの`PySide`をインストールし直す。

`Fatal error in launcher: Unable to create process using '""`

# プロセスの通信

プロセスの通信には、`QLocalSocket`と、`QLocalServer`を使う。
まだ全然わかってないが、基本的なPythonのサンプルがなかったので記載。
他にもそれっぽい名前のClassあるので、追々わかれば書くかもしれません。

Pythonの標準モジュールでやる場合はこちら。

> Python2 Standard Library
https://unitbus.github.io/pages/notes/python/standard#%E3%83%97%E3%83%AD%E3%82%BB%E3%82%B9%E3%81%AE%E9%80%9A%E4%BF%A1

## QLocalServer

まずサーバー側を起動。コンソールアプリだとしても、`QApplication`でイベントループさせる。
イベントループさせないと、`waitForNewConnection`でコネクション無制限にしても意味ないので注意。

サーバー名が大事になるので、必ず付ける。
コマンドラインで実行して、そのまま待機させておく。

```python
from PySide.QtGui import QApplication
from PySide.QtNetwork import QLocalServer

class Server(QLocalServer):
    
    def __init__(self, parent=None, **kwargs):
        super(Server, self).__init__(parent)
        self.newConnection.connect(self.echo)
    
    def echo(self):
        print 'server connect !!!'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    server = Server(app)
    server.listen('home')
    server.waitForNewConnection(-1)
    
    sys.exit(app.exec_())
```

## QLocalSocket

サーバーを起動後、ソケット(クライアント？)を起動。
サーバー側に設定した名前で接続する。

こちらも、`QApplication`をイベントループさせないと通信されなかった。
親にする必要はないが、イベントループ(`exec_`)は必須っぽい。

```python
from PySide.QtGui import QApplication
from PySide.QtNetwork import QLocalSocket

class Socket(QLocalSocket):
    
    def __init__(self, parent=None, **kwargs):
        super(Socket, self).__init__(parent)
        self.connected.connect(self.echo)
    
    def echo(self):
        print 'socket connect !!!'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    socket = Socket(app)
    socket.connectToServer('home')
    socket.waitForConnected(-1)
    
    sys.exit(app.exec_())
```
