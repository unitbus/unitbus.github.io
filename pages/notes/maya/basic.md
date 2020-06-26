---
layout: default
title: Maya
---

# Basic

## Scriptノードの実行を回避

ファイルダイヤログのオプションで、シーンを開く時に埋め込まれてる`Script`ノードの実行を回避出来ます。
melや、pythonコマンドにも、`executeScriptNodes`フラグが用意されてます。

https://knowledge.autodesk.com/ja/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/JPN/Maya/files/GUID-203FC12C-6C80-497C-AC29-548DF6EC91B5-htm.html

`Script`ノードは万能で、シーンを開く時、閉じる時、レンダリング時など、
タイミングをコントロールしながら、埋め込んだ'Script'を実行できます。
いつ頃からか忘れましたが、いまはここに、標準でframeRangeの設定が埋め込まれてたりします。

いま流行りのマルウェアもこの仕組を利用し、まずは環境を感染させ、順に開いたファイルに感染を広げさせてます。
Autodeskが配布してるツールも、感染前提で駆除してるので注意してください。

今後も亜種が増えると思うので、ネットからデータをダウンロードして開く際は、`Script`ノードを無効にして開き、`Expression Editor`のメニューから、`Select Filter > By Script Node Name`で、`Scrip`ノードに余分なスクリプトが埋め込まれてないかを確認する事をオススメします。

※ `Scrip`ノードには、Brfore/Afterと、タイミングが2種類あるので、両方確認する必要があります。
