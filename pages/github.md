---
layout: default
title: GitHub
---

# GitHub

オンラインで、複数人と、サブバージョン管理できるサービス？
アカウント作るだけ作って放置してたので、よくわかってない。

# GitHub Pages

GitHubを利用して、静的ページなサイトを作れるらしいので調査とメモ。
wordpress的なのを、動的ページと言うらしい。

まず、調べても、gitがなんなのかピンとこなかったので、git自体の理解は保留。
直接、コマンドラインからgitを操作するようなのは無しで、運用できないか調査。

軽く調べるとわかるが、 `<アカウント名>.github.io` というリポジトリを作るだけらしい。
簡単なので説明は割愛。

## やりたいこと

- window10環境、コマンドラインをなるべく使わない
- markdownでメモを取る感覚でページの作成、そのまま投稿

### window10環境

GitHubのページ見てもいまいち感覚がわからず、そもそもアップロードの仕方もわからん。
**GitHub Desktop** というアプリを入れれば、色々問題が解決した。

ローカルのフォルダを指定し、ローカルリポジトリにすることで同期が可能に。
特に複雑な設定もなく、コマンドライン操作も要らない。

ただ、アプリのインストール先が、今風なので注意。データ保存先はroaming。
最近この手のアプリが増えて、管理面倒…。

**インストール先**

`C:\Users\%USERNAME%\AppData\Local\GitHubDesktop`

**データ保存先**

`C:\Users\%USERNAME%\AppData\Roaming\GitHub Desktop`

個人的には、この手のは `mklink` でジャンクション作って、別の場所で管理。
バックアップ管理とか、別マシンで使いたかったりするので。

### markdown

もう一つ個人的に重要だったのが、markdownの使用。

はっきり言って、もう記事書くのに、htmlは触りたくないので、譲れないポイント。
かと言って、wordpress的な動的サイトは、記事を書くのが面倒になるので飽きてくる。

この問題は、何もしなくても、みごとクリア。
md置くだけで、GitHub側に、jekyllというツールがインストールされてる？らしく、
何もしなくてもhtmlで表示してくれます。

~~後は書くだけなはず。~~

vscodeで書いてるが、previewでは大丈夫でも、htmlで見ると乱れる所がチラホラ…。
githubで、mdを直接見ると大丈夫だったりする。

details内でコードブロックを使う場合は、`<div>` で囲む必要があるらしい。

<details>
<summary>畳むタイトル</summary>
<div>

``` python
# コードブロック
import sys
print(sys.path)
```

</div>
</details>

**markdown-breaksが適用されない**

ダブルスペースで改行するのは嫌なので、breaksオプションが使えないのはツライ。

そもそも、書いてるときに読みづらいから改行して書いてるのに、
*「ブラウザの幅に合わせて改行すべき」* って、本家の謎の思想が意味わからん。
書いたままの見た目で出せ。と毎回思う。

[markdownの改行](#markdownの改行)

## 除外ファイル、フォルダ

`.gitignore` を置いて、ファイル名等を書くだけ。

公開したくないファイルとか、.vscodeとか、まぁその辺。
`.gitignore` 自身も追記しておけば、除外可能。

# jekyll

GitHubが、markdownプレビュー用に使ってる、Git用プラグイン？みたいなもの。
.mdファイルを置くと、自動でhtmlページが作成され、ユーザーにはhtmlで見てもらえる。
静的ページを、自動で作成してくれるので楽にサイトの更新が出来る。

必要なファイルと、階層はこんな感じ。

```
■ フォルダ、◻ ファイル

■ site.github.io
    ■ _layouts
        ◻ defaut.html
    ◻ _config.yml
    ◻ favicon.ico
    ◻ style.css
    ◻ index.md
```

## ページのスタイル

`_layout/defaut.html` みたいな感じで置いておくと、テンプレートとして適用される。
ファイル名は、maekdown側から指定する感で、複数配置して切り替え可能。
多分、指定なければ `defaut.html` になる？

`content` の部分に、markdownが変換され挿入される。
デザイン変更、スタイルシート等ここで設定しておく感じ。

普通にjs(javaScript)も使えるっぽい。

## markdownの改行

markdownの場合、半角スペース二個、`<br>` を使わずに、書いた通り改行させるには
markdown-breaksという設定で切り替え可能なのだが、GitHubには見当たらないので調べてみた。

GitHubは、普通のmarkdownじゃないらしい。ここを見ると、

https://help.github.com/ja/articles/updating-your-markdown-processor-to-kramdown

*「GitHub Pages は、Markdown プロセッサとして kramdown だけをサポートします。」*
だそうです。

で、設定方法は、 `_config.yml` に追記する。

```yaml
kramdown:
    input: GFM
    hard_wrap: true
```

と、 `kramdown` の `hard_wrap` として設定してあげる。
ちなみに、GFMは、 `GitHub Flavored Markdown` らしい。

## sitemap

数日経っても、google検索に引っかからなかったので、調べてみると
`sitemap` が必要らしい。すでに作成されてる場合は以下で確認できる。

`https://{site}.github.io/sitemap.xml`

設定方法は、 `_config.yml` に追記する。

```yaml
plugins:
    - jekyll-sitemap
```

## Syntax highlighter

`<code>` タグの中を言語で色付けするので、`コードハイライト` とも呼ばれる機能。

```yaml
kramdown:
    syntax_highlighter: rouge
```

調べてみたが、結構面倒だった。 `_config.yml` に上を追記するだけかと思ったら、
htmlに、cssのクラスが挿入されるだけで、css自体の存在が無い。

なんかゴニョゴニョして、cssを出力できるっぽいが、意味わからなかった。
css自分で書いても良いみたいなので、下のサイトを参考に用意して、`<head>` に追加。

> GitHub Pages が Jekyll 3.0 になり、ますますブログが書きやすくなった。
https://mattn.kaoriya.net/software/20160215110235.htm
