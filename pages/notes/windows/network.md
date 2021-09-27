---
layout: default
title: Windows
---

# Windows Network

windows 10 になってからのメモ。

## ポートの開放

いままで使用してたポートが突然使えなくなるケースがある。
使用されてるポートの一覧を確認し、なかった場合は、予約(除外範囲に)されてる可能性がある。
基本、50000以降はユーザー範囲なので、50000以降を大量に予約するアプリは行儀が悪いと思う。

> へっぽこプログラマーの備忘録
https://kuttsun.blogspot.com/2020/03/systemnetsocketssocketexception.html

### 使用中ポートの一覧

`netstat -oan`

### 除外ポートを設定

`netsh int ip add excludedportrange protocol=udp startport=60001 numberofports=10`

# Windows Remote Desk Top

設定画面で保存して、テキストで開くと、オプションにはない細かい設定が出来ます。

例えば、起動と同時にサブモニタに全画面表示したい場合は、以下の設定が必要でした。
存在しないオプションは追記します。環境で調整必要です。
略字、スペース有り無しと気持ち悪いキーですが…

```json
selectedmonitors:s:1
span monitors:i:1
screen mode id:i:2
winposstr:s:0,3,-3440,0,0,1440
```

環境によっては、`selectedmonitors`だけでも平気な人も居るみたいです。

うちのは特殊みたいで、サブモニタがマイナス位置にあたるみたいで、
`winposstr`の設定で無事にサブモニタに表示できました。

> .RDP ファイルパラメーター
https://www.vwnet.jp/Windows/w7/RDP/RDP-parameters.html

## selectedmonitors

使用するモニタID。目的のIDが無い時は追加が必要。
モニタのIDは、コマンドプロンプトで下のコマンド打つとダイヤログで教えてくれる。
`mstsc.exe`はリモートデスクトップの本体っぽい？

```console
mstsc.exe /l
```

下みたいに、コンマで区切って2つ書くと、複数モニタでフルスクリーンができる。

`selectedmonitors:s:1,0`

## span monitors

0: disable, 2: enable

`1`にすると、複数モニタ使えます。

## screen mode id

1: window, 2: full-screen

`winposstr`の位置を元にフルスクリーンになる気がする。

## winposstr

左から順に、固定, 固定, 左, 上, 右, 下 

左2個は固定値らしく変更しない。
