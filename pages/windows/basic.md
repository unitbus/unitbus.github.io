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

### 参考

> Windows 10 ファイルエクスプローラー上で重複に表示されているドライブアイコン１つだけに表示する
> https://www.billionwallet.com/goods/windows10/win10-duplicate-drive-icon.html

# Windows Font

設定画面からも出来るっぽいが、下のフォルダに放るだけでもOK。

`C:\Windows\Fonts`

## Source Han Code JP

等幅で日本語が扱える、オススメのフォント。アドビの人が公開してるらしい。
比率は `2:3` と、アルファベットの間隔が広くスクリプト向き。
標準では入ってないので、ダウンロードが必要。

> Adobe Fonts: source-han-code-jp
> https://github.com/adobe-fonts/source-han-code-jp

フォント本体のダウンロードは下から。
https://github.com/adobe-fonts/source-han-code-jp/blob/master/README-JP.md#download-the-fonts

OTFフォルダに入ってる、.otfファイルを、fontフォルダに放るとインストール始まります。
`It.otf` はイタリックでした。

日本語名だと、 `源ノ角ゴシック Code JP` らしいです。
日本語アプリだと、日本名知らないと探せないかも…。