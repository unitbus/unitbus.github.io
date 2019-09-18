---
layout: default
title: Python
---

# Python PySide.

## 基本

PySideは難しいと敬遠されるが、実はpythonで使えるUIの中で一番シンプルで、ルールが統一されてる。
以下のコードが、スタンドアローンで、最低限必要とするコマンド。

```
from PySide.QtGui import *
app = QApplication([])
button = QPushButton('test')
button.show()
app.exec_()
```

mayaだと、3行で済む。
```
from PySide.QtGui import *
button = QPushButton('test')
button.show()
```

なぜ、QPushButtonで、show()メソッドが使えて、表示出来るのか？がわかるとPySideが楽しくなる。
