---
layout: default
title: Software VSCode
---

# 概要

最近、一番勢いのあるテキストエディタ。
へビューユーザーから、ライトユーザーまで幅広く使われてる印象。
自分も、長年愛用してた、Notepad++からメインエディタを変更。

# 設定

**[Ctrl + Shft + P]** から、 **基本設定: 設定(JSON)を開く** を選択。
最近は、HTMLっぽく見やすくなったが、逆に設定が面倒になったので、JSONへコピペした方が楽。

## 設定の同期

アドオンでは色々な同期ツールがあったが、v1.48.xから標準で搭載。
`Settings Sync`がインクルードされた感じと思われる。
設定のコメントには`settingsSync`の単語が出てくるが、探すと無いので実際のところはわからない。

ツールバーの、歯車アイコンの上に追加され、Microsoftアカウントと、GitHubアカウントから選択。
アドオン版だとGitHubにレポジトリの用意が必要だったが、アカウントさえあれば同期出来る模様(さすが本家？)。

環境で異なる設定は除外したいが、マージ時にコントロール出来る感じはしなかった。今後のバージョンアップに期待。
ローカルパスを記述する設定だけ、ワークスペースに書くことで回避。なるべく基本的な設定だけにして同期するのが良いかと思う。

アドオン版の記事に書いてあった、`// @sync`も試したが、上手くいかなかった。
未だに健在なのをみると、まだアドオン版の方が高機能なのかもしれない(使ったこと無い)。

`--user-data-dir`を起動時に使用すると、好きな場所にユーザー設定を保存出来るのだが同期が出来なかった。
新規に作った場所でも駄目だったので、ユーザー設定の場所は固定らしい。ローカルネットワークで共通設定してた人は諦めるしかないかも？
とは言え、Cドライブの`Roaming`に置きたくなかったので、自分は [ジャンクション](https://unitbus.github.io/pages/notes/windows/batch#%E3%82%B7%E3%83%B3%E3%83%9C%E3%83%AA%E3%83%83%E3%82%AF%E3%83%AA%E3%83%B3%E3%82%AF%E3%81%A8%E3%82%B8%E3%83%A3%E3%83%B3%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3) を作成して逃した。
ジャンクションはネットワークに置けないのが残念。

`--extensions-dir`の方は使用したまま同期出来た。
複数台で使用してる場合はアドオンだけでもローカルネットワークに置くのもありかも。

### リンク

> 【VSCode】公式版の設定同期機能 Settings Sync を早速使ってみた
https://serip39.hatenablog.com/entry/2020/08/18/173000

## Font

色々試したが、 **Source Han Code JP** がオススメ。
散々悩んだが、 **2:3** 比率の、 **Source Han Code JP** に落ち着いた感じ。

日本が使える等幅フォントは少なく、大抵が **1:2** 比率で、アルファベット間隔が狭く見辛い。
かといって、アルファベットだけ等幅のフォントを使うと、
コメントの日本語がプロポーショナルになって、凸凹して気持ち悪い。

標準では入ってないので、ダウンロードが必要。
インストール方法はこちらを参考にどうぞ。

> Windows / Basic / windows-font
[https://unitbus.github.io/pages/notes/windows/basic#windows-font](https://unitbus.github.io/pages/notes/windows/basic#windows-font)

```json
"editor.fontFamily": "'Source Han Code JP Regular', Consolas",
```

`editor.fontFamily` は、代用フォントを書く前提となってるので、
スペースある場合は、シングルクォーテーションで囲む。
他の太さにしたければ、 **Regular** の部分を、置き換えれば使用可。

以下のように間違って説明してるサイトが結構あるので注意。

```json
// 間違い例
"editor.fontFamily": "Source Han Code JP Regular",
```

## Markdown

改行の有効は、設定で変更できる。
cssも指定可能。相対パスは、ワークスペースの位置になる。

```json
"markdown.styles": ["./document.css"],
"markdown.preview.breaks": true,
```

### リンク

> VS Code 標準Markdown Extensionsで、改行を有効にする
https://qiita.com/rma/items/75f502e784b7164b8813

## 検索の除外設定

ワークスペースに、複数のフォルダを登録してると、全体検索で大量結果が表示され困るのでフィルタを設定する。
基本は、表示設定 `files.exclude` が継承され、検索用にフィルタ `search.exclude` を追加出来る仕組み。

設定が反映されずに困ってたら、検索時にフィルタを有効にしないと意味が無いらしいので注意。

> VSCode ファイル検索の除外設定
https://developer.feedforce.jp/entry/2017/11/24/195644

## pythonのデバッグが出来ない場合

急に、F5を押しても、別コンソールが出てしまい、デバッグが始まらない事があった。
launch.jsonの、 `"console": "none",` にしたら直った。
noneだと赤く表示されるが、使えるらしい。

```json
    "configurations": [
        {
            "name": "Python2",
            "type": "python",
            "request": "launch",
            "stopOnEntry": true,
            "pythonPath": "${config:python.pythonPath}",
            "program": "${file}",
            "console": "none",
            "cwd": "${workspaceFolder}",
            "debugOptions": [
                "RedirectOutput",
                ]
        },
    ]
```

### リンク

> [Visual Studio Codeの設定「虎の巻」：Python編 (2/3)](https://www.atmarkit.co.jp/ait/articles/1711/24/news034_2.html)

### 追記

コマンドプロンプトのオプションで、レガシーコンソールを使用するのチェックを外したら元に戻った。
結局、何が悪いのかよくわからないので、調査中。
多分、windowsUpdateのタイミングで色々おかしくなった？

# Tips

## 折り畳み

折り畳みルールにないケースでも、regionで囲むと畳んで表示できる。
インデントも関係なく使えるので、たまに便利。コード行が増えるのが難点。

``` python
# region
<実際のコード>
# endregion
```
