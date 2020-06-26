---
layout: default
title: Maya
---

# Basic

## Scriptノード

`Script`ノードは万能で、シーンを開く時、閉じる時、レンダリング時など、
タイミングをコントロールしながら、シーンに埋め込んだスクリプトを実行できます。
いつ頃からか忘れましたが、いまはここに、標準でframeRangeの設定が埋め込まれてたりします。

### Scriptノードの実行を回避

ファイルダイヤログのオプションで、シーンを開く時に埋め込まれてる`Script`ノードの実行を回避出来ます。
melや、pythonコマンドにも、`executeScriptNodes`フラグが用意されてます。

https://knowledge.autodesk.com/ja/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/JPN/Maya/files/GUID-203FC12C-6C80-497C-AC29-548DF6EC91B5-htm.html

### 悪用したマルウェアが流出

いま流行りのマルウェアもこの仕組を利用し、まずは環境を感染させ、順に開いたファイルを感染させ続けています。
一度感染すると、シーンから駆除しただけでは解決せず、再度シーンを開く度に復活します。
2020年05月頃から確認され、2020/06/26(土)に発動します。発動するとMayaが操作不能になります。

`Script`ノードは非常に便利なのですが、なぜかMayaは全面的なアピールをしてません。
専用のエディタや、ウインドウもなく、オマケ的な位置付けでバックグラウンドに押し込んでます。
もっと早く、Autodeskがちゃんとしたサポートをしてれば、こんな事にはならなかった感が半端ないです。

ちなみに、Autodeskが配布してるツールも、感染する前提でシーンを開かせ駆除してるので注意してください。

https://knowledge.autodesk.com/ja/support/maya/troubleshooting/caas/sfdcarticles/sfdcarticles/kA93g0000004JXR.html

今後も亜種が増えると思うので、ネットからデータをダウンロードして開く際は、
`Script`ノードを無効にして開き、`Expression Editor`のメニューから、
`Select Filter > By Script Node Name`を選択し、
`Scrip`ノードに余分なスクリプトが埋め込まれてないかを確認する事をオススメします。

`Scrip`ノードには、Brfore/Afterと、大きく2種類のタイミングがあり、両方確認する必要があります。
UIからわかりにくいので注意してください。

今回のタイプは、ファイルから感染する珍しいケースでしたが、スクリプトを実行するだけで環境を汚したり、
scriptJobで作業を妨害など、世の中には悪い事考え、実行する人が多く居るので、今後も注意が必要です。