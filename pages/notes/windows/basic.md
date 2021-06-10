---
layout: default
title: Windows
---

# Windows Basic

windows 10 の内容を中心にメモ。

## エクスプローラーのツリーで、ドライブが二重表示

windowsUpdateするたびの元に戻される。
レジストリエディターから削除するしかない。
レジストリの操作は自己責任で。

1. win + R キーで、**regedit** 起動。パスフィールドへ、下のパスをコピペ。
`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\DelegateFolders`
3. コピペで飛ばないので、一文字消すと予測候補出るので、選択すると **DelegateFolders** まで表示される。
4. **{F5FB2C77-0E2F-4A16-A381-3E560C68BC83}** を削除。

> Windows 10 ファイルエクスプローラー上で重複に表示されているドライブアイコン１つだけに表示する
> https://www.billionwallet.com/goods/windows10/win10-duplicate-drive-icon.html


## アイコンの表示がおかしい時

アイコンのキャッシュを削除できるコマンドらしい。

```bat
ie4uinit.exe -ClearIconCache
```

windowsでアイコンを作成する時は、 **Greenfish Icon Editor** がお勧め。
自分は、 **portable version** をダウンロード。

> Greenfish Software.org ダウンロードページ
> http://greenfishsoftware.org/gfie.php#apage

**「windowsアイコンを作成する」**をしないと、
ショートカットアイコンがおかしくなったりするので注意。


## タスクバーにピン留め

ウインドウを閉じ、ピン留めしたアイコンを、**shift + 右クリック** で、ピン留めアイコンのプロパティを開ける。
アイコンをグレースケールにしておけば、起動後は元の色付きアイコンで表示されるので、ストアアプリっぽく使える。

windows7でやると、アクティブなアイコンが表示されないので意味がない。
むしろ常にグレースケールになるので注意。逆に、タスクトレイのアイコンがおかしくなった時は、ここを疑う。


# Windows Font

設定画面からも出来るっぽいが、下のフォルダに放るだけでもOK。

`C:\Windows\Fonts`

## Source Han Code JP

等幅で日本語が扱える、オススメのフォント。アドビの人が公開してるらしい。
比率は **2:3** と、アルファベットの間隔が広くスクリプト向き。
標準では入ってないので、ダウンロードが必要。

> [Adobe Fonts: source-han-code-jp](https://github.com/adobe-fonts/source-han-code-jp)

フォント本体のダウンロードは下から。
https://github.com/adobe-fonts/source-han-code-jp/blob/master/README-JP.md#download-the-fonts

OTFフォルダに入ってる、.otfファイルを、fontフォルダに放るとインストール始まります。
`It.otf` はイタリックでした。

日本語名だと、 **源ノ角ゴシック Code JP** らしいです。
日本語アプリだと、日本名知らないと探せないかも…。

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
