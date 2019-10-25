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

なぜ、QPushButtonで、show()メソッドが使えて、表示出来るのか？がわかるとPySideが楽しくなる。

exec_()を実行する事で、イベントループになる。
この場合、QApplicationを作成し、standaloneソフトとして待機させてる状態になる。
exec_()は、ダイヤログや、メニュー、スレッドでも出てくるので、覚えておくと便利。

## Document & Reference

> PySide 1.0.7 Reference
https://srinikom.github.io/pyside-docs/

> PySide 1.2.1 Reference
https://pyside.github.io/docs/pyside/index.html

> Qt for Python(PySide2)
https://doc.qt.io/qtforpython/

*PySide 1.2.1 Reference* では、継承図が表示されないのでちょっと不便。

そろそろPySide1は切り捨てて書いても良い気もしますが、まだ互換性考えて、
*PySide 1.0.7 Reference* の方を見て書いてます。
