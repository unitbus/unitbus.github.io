---
layout: default
title: Python2 Built-in Functions
---

<!-- # Python Built-in Functions -->
<!-- # 組み込み関数 -->

## help

`help(object)`で関数、クラス、パッケージ等のドキュメント(docstring)が取得できる。
__doc__部分に記述するので、`object.__doc__`からオリジナルが取得できる。

docstringは、モジュールファイルの最初に、自分で変数作ってドキュメントを追加する事も出来る。

```python
__doc__ = ```ドキュメント```
```

help()で取得すると、いい感じにインデントが処理されて表示される。
help()で表示される文字列を取得したい場合は、`inspect.getdoc(object)`を使うと良かった。

`inspect`モジュールは色々便利そうだが、追えてない…。
