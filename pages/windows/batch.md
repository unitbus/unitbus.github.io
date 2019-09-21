---
layout: default
title: Windows
---

# Batch

昔からある、コマンドプロンプトの書式をテキスト化したもの。
window10になって、powerShellがメイン？になったらしいが、まだbatchも現役。

## 環境変数

```
set
```

とだけ打つと、現在の環境変数の一覧が返される。

```
set maya
```

と打つと、mayaと名前が付く変数だけにフィルタされ、リストが返る。
これ知っておくと便利。

```
set name=unitbus
```

=で値を指定することで、コマンドプロンプト内や、
bat内で、一時的に使用したり、変更出来たりする。
すでに使われてないかを気を付ける必要がある。

```
set PATH=%PATH%;C:/test
```

追加したい場合は、自身を加えて、セミコロンで追記する。

システムに影響与えるには `setx` を使う。

## シンボリックリンクと、ジャンクション

シンボリックリンクは管理者権限無いと作成出来ない。
ジャンクションにすれば気軽に作れる。作成するコマンドは一緒。

```
mklink /J C:\Users\%USERNAME%\AppData\Roaming\Mozilla U:\%USERNAME%\appdata\roaming\Mozilla
```

## 改行して、複数行で書く

batで、１つのコマンドに複数行にしたい場合は、行末に「^」を入れるとできる。

## echo

メッセージを表示したい時に使う。

```
@echo 日本語
```

@を使うと、入力したコマンドの表示を隠す事が出来る。
メッセージ自体は表示されるので、二重に表示されるような見た目にならない。

ログを人に読ませたい時は、batの一行目で、echo自体を無効にしておけば良い。

```
@echo off
echo 日本語
```

改行だけを表示したい時は、 `echo.` を使う。

```
echo.
```

`echo` だけだと、現在のエコー設定を表示されので注意。


## メッセージボックス

vbsファイルを生成する必要があるが、一行で出す事は可能。

```
echo msgbox "メッセージ",vbCritical,"タイトル" > %TEMP%/msgbox_tmp.vbs & %TEMP%/msgbox_tmp.vbs
```

## 文字の置き換え

```
set moji=検索文字
set moji=%moji:検索=置換%
echo %moji%
```

## 文字列の一部を削除(スライス)

```
@echo off
set value=test.ext
echo %value:~-4%
```

## 別のバッチファイル内の pause を無効化する。

右のバッチの結果を、エコーするって感じで回避できる。

```
echo|"F:\tmp\convertA.bat"
echo|"F:\tmp\convertB.bat"
```

### 参考

> Qiita: コマンドプロンプトの自分用メモ
https://qiita.com/yuji38kwmt/items/6866fbcb3175ef1c897a

## 日付

`%date%` に、`2019/09/22` みたいな形で、日付は格納されてる。
`/` を取りたい時は、スライスを利用( `20190922` )。

```
echo %date%
set date_raw=%date%
set date_now=%date_raw:~-10,4%%date_raw:~-5,2%%date_raw:~-2,2%
echo %date_now%
```

## 時間

`%time%` に、 ` 1:06:55.71` みたいな形で、時間は格納されてる。
`010655` みたいに、ファイル名とかに使う時は、クセが強いので、ちょっとメンドイ。

```
echo %time%
set time_raw=%time: =0%
set time_now=%time_raw:~0,2%%time_raw:~3,2%%time_raw:~6,2%
echo %time_now%
```
