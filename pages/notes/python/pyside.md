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

なぜ、`QPushButton` で、`show()` メソッドが使えて、表示出来るのか？がわかるとPySideが楽しくなる。

`exec_()` を実行する事で、イベントループになる。
この場合、`QApplication` を作成し、standaloneソフトとして待機させてる状態になる。
`exec_()` は、ダイヤログや、メニュー、スレッドでも出てくるので、覚えておくと便利。

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

<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowA.png" width="50%">
<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowB.png" width="50%">
<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowC.png" width="50%">

> [Dwonload / Standalone / Python / ubWidgetHierarchy](https://unitbus.github.io/pages/download)

ダウンロードしたファイルは、環境変数の **PYTHONPATH** が通ってる場所に置き、
以下のコマンドを実行してください。

``` python
import ubWidgetHierarchy
ubWidgetHierarchy.show()
```

standaloneでも動きますが、他のウインドウが無いと意味ありません。

こうやって見ると、**Houdini** はまだ、独自UIが多く、**Qt** を使ってない事がわかる。

# Viewについて

## QListView

`QListWidget` のメソッドを使って作成すると、一個づつしか追加できないので、数が多いと激重になります。

`QAbstractListModel` を元に自分で作成し、`QListView` を使用すれば、
不必要な機能に絞ってを減量出来るので、かなり高速化出来ます(当社比約20倍)。

とは言え、かなりの知識と、準備が必要なり、汎用性には向きません。
下手に機能を盛れば、盛るほど遅くなります。

リスト対象のアイテムが、1万とか超えなければ、
`QListView` と、`QStnanderdModel` の組み合わせで十分だったりします。
`QListView` 複数行まとめて登録する事で、十分な高速化が出来ます。

## QTreeView

`QTreeWidget`&`QTreeWidgetItem`と、`QTreeView`&`QAbstractItemModel`の組み合わせで比較してみたが、
`parent-1000 x child-1000` とかなり高負荷で試しても速度面的な恩恵はなかった。
書き方次第では、Viewの方がかなり遅くなる場合も…。

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

`QMenu.addAction` で同じアクションを指定すると、一番下に再配置される。
この仕組み使ってソートも可能。

ドキュメントのメソッド一覧をみると、`QMenu.insertMenu`, `QMenu.insertSeparator`はあるのに、`insertAction`が見当たらない。
しばらく使えないものだと思ってたが、QWidget側に`QWidget.insertAction`が用意されてた。
なので、継承してるQMenuでも普通に使える。これに気付かず色々頑張ってしまった…。

`Qt`のドキュメントの方が見易いと教えてもらった。ありがとうtakkun。
クラス説明上の方の、下の文字のリンクをクリックすると、継承した後のメソッド一覧が確認できる。
`List of all members, including inherited members`

> https://doc.qt.io/qt-5/qmenu.html

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
