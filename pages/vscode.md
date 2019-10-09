---
layout: default
title: VSCode
---

# VSCode

最近、一番勢いのあるテキストエディタ。
へビューユーザーから、ライトユーザーまで幅広く使われてる印象。
自分も、長年愛用してた、Notepad++からメインエディタを変更。

## Settings

**[Ctrl + Shft + P]** から、 `基本設定: 設定(JSON)を開く` を選択。
最近は、HTMLっぽく見やすくなったが、逆に設定が面倒になったので、JSONへコピペした方が楽。

### Font

色々試したが、 `Source Han Code JP` がオススメ。
散々悩んだが、 `2:3` 比率の、 `Source Han Code JP` に落ち着いた感じ。

日本が使える等幅フォントは少なく、大抵が `1:2` 比率で、アルファベット間隔が狭く見辛い。
かといって、アルファベットだけ等幅のフォントを使うと、
コメントの日本語がプロポーショナルになって、凸凹して気持ち悪い。

標準では入ってないので、ダウンロードが必要。
インストール方法はこちらを参考にどうぞ。

https://unitbus.github.io/pages/windows/basic#windows-font

```
"editor.fontFamily": "'Source Han Code JP Regular', Consolas",
```

`editor.fontFamily` は、代用フォントを書く前提となってるので、
スペースある場合は、シングルクォーテーションで囲む。
他の太さにしたければ、 `Regular` の部分を、置き換えれば使用可。

以下のように間違って説明してるサイトが結構あるので注意。

```
// 間違い例
"editor.fontFamily": "Source Han Code JP Regular",
```

### Markdown

改行の有効は、設定で変更できる。
cssも指定可能。相対パスは、ワークスペースの位置になる。

```
"markdown.styles": ["./document.css"],
"markdown.preview.breaks": true,
```

> VS Code 標準Markdown Extensionsで、改行を有効にする
https://qiita.com/rma/items/75f502e784b7164b8813