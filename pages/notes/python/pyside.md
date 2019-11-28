---
layout: default
title: Python
---

# PySide

## 基本

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

## Document & Reference

> [PySide 1.0.7 Reference](https://srinikom.github.io/pyside-docs/)

> [PySide 1.2.1 Reference](https://pyside.github.io/docs/pyside/index.html)

> [Qt for Python(PySide2)](https://doc.qt.io/qtforpython/)

**PySide 1.2.1 Reference** では、継承図が表示されないのでちょっと不便。

そろそろPySide1は切り捨てて書いても良い気もしますが、まだ互換性考えて、
**PySide 1.0.7 Reference** の方を見て書いてます。

## Widget一覧

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

## QListView

`QListWidget` のメソッドを使って作成すると、一個づつしか追加できないので、数が多いと激重になります。

`QAbstractListModel` を元に自分で作成し、`QListView` を使用すれば、
不必要な機能に絞ってを減量出来るので、かなり高速化出来ます(当社比約20倍)。

とは言え、かなりの知識と、準備が必要なり、汎用性には向きません。
下手に機能を盛れば、盛るほど遅くなります。

リスト対象のアイテムが、1万とか超えなければ、
`QListView` と、`QStnanderdModel` の組み合わせで十分だったりします。
`QListView` 複数行まとめて登録する事で、十分な高速化が出来ます。
