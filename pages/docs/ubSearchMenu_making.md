---
layout: default
title: ubSearchMenu Making
---

# 挨拶

近況報告としては、前の会社を辞めた際に、アーティスト業は引退し、テック系CG屋に転職しました。プログラマーと言うよりは、エンジニアに近い感じです。

もともとは、ジェネラリストでしたが、当時からTAっぽい仕事が多かった気がします。
テックに移って早4年近く経ち、今はもう、画作りにほぼ関わってないので、TAですらありません。笑

転職の際に、*Python* を覚える必要があり、慌てて勉強した気がします。
世間と比べても、ちょっと遅めのデビューだったと思います。
デビューが遅かったおかげか、色々なサイトを見て勉強する事が出来ました。

特に、*PySide* の記事を多く見かけ、色々カスタマイズされたUIを見て、モチベーション高く学習を続ける事ができました。この場を借りて、情報を公開して頂いてた、多くの方にお礼を言いたいと思います。ありがとうございました。

メニューに関するネタをあまり見かけなかったので、恩返しという訳ではありませんが、
自分も情報共有に貢献出来たらと思い、記事にしました。

**このページは、Maya Advent Calendar 2019 12/3用に書かれています。**

> Maya Advent Calendar 2019
[https://qiita.com/advent-calendar/2019/maya](https://qiita.com/advent-calendar/2019/maya)

## 完成イメージ

作り方から書いてもあまりピンとこないと思うので、先に完成画像を貼っておきます。

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubSearchMenu_mayaPressMenuA.png">
</p>

*Maya* にあるメニューから検索し、アクションを実行するツールです。
せっかくなので、ある程度実用性のあるツールにしてみました。

ダウンロードと、使い方の説明は、[ツール紹介](#ツール紹介)を見てください。

# Mayaの話

*Maya* のUIは、Qtで作られてるため、目に見えてる、ほぼすべてのウィジェットに対して、*PySide* からアクセス出来ます。例えば、*Maya* の、メインウインドウを取得したいだけなら、**shiboken** や、**MayaQWidgetBaseMixin** などを使う必要はありません。オブジェクト名が分かれば、*PySide* としてWidgetを検索し、取得できます。

## shiboken

**shiboken** は、ざっくり言うと、DCCと、*PySide* を繋ぐ為のモジュールです。
DCC独自のウィジェットにアクセスしたり、取得したい時などに使う？らしいです。

*PySide* のドキュメントに、サイズが大きくて切り離した的なコメントも見かけますし、目的に対して、ちょっと大げさなのもあり、自分はこのモジュールを使った事がありません。

## MayaQWidgetBaseMixin

**MayaQWidgetBaseMixin** は、*Maya* 側が用意してる *PySide* 用のクラスです。便利なクラスですが、ペアレント先を取得する為だけに、バージョンで仕様がコロコロ変わる *Maya* のモジュールを読みたくはありません。

都度、DCCを起動してのデバッグも大変ですし、自分は、ウィジェット作成中は、
なるべく *Maya* のモジュールは読まず、スタンドアローンで動くようにしています。

## ウィジェットの検索

通常、*PySide* で作成されたウィジェットには、オブジェクト名が付いています。
オブジェクト名がわかれば、*Maya* から、ウィジェットをオブジェクトで取得する事が出来ます。

初めて *Maya* のウィジェットにアクセスする人は、ちょっと規模の大きさに戸惑うと思ったので、ウィジェットの構造が一覧で見れるビューワーがあると便利だと思い、簡単なのですが作ってみました。

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowA.png">
</p>

> [ダウンロード / ubWidgetHierarchy](https://unitbus.github.io/pages/download)

*Maya* でツールを作成する場合、既に数多くあるツール郡の中の一つとして動作する事になるので、決め打ちで、ハードコーディングしてしまった方が、レスポンス的に都合が良い事が多いです。特にメニュー系などは、都度検索して遅くするより、速度面を優先して意識したいところです。

ちなみに、*Maya* のメインウインドウ名は、**MayaWindow** になります。
目的のウィジェットが事前に分かれば、後は名前で検索するだけです。

## windowの取得

`objectName()` や、`windowTitle()` から取得する方法があります。
この方法は、他のDCCでも使えるので、覚えておくと便利だと思います。

> Maya / PySide / MainWindowの取得
[https://unitbus.github.io/pages/notes/maya/pyside#mainwindowの取得](https://unitbus.github.io/pages/notes/maya/pyside#mainwindowの取得)

## menuBarの取得

今回は、parent先はmenuBarなので、menuBarを取得したいのですが、**MayaWindow** の、menuBarには `objectName()` が設定されてないので直接取得する事が出来ません。

また、**MayaWindow** は、`QMainWindow` を使わず、`QWidget` で作成されてるため、`QMainWindow.menuBar()` メソッドが存在せず、取得できません。
`QWidget` から辿って、`QMenuBar` を探す必要があります。

``` python
from PySide2.QtGui import *

def getTopLevelWidget(name):
    
    for widget in QApplication.topLevelWidgets():
        
        if widget.objectName() == name:
            return widget
    
    return None

# QApplicationにぶら下がってる、mayaのウインドウを探す
window = getTopLevelWidget('MayaWindow')

# menuBarを探して、objectとして取得
menuBar = window.findChild(QMenuBar)
```

他にも、**HelpMenu** を先に取得し、親ウィジェットを探す方法もあったりしますが、脱線するので説明割愛。

## メモ

`children()`, `findChildren()` 等で取得したオブジェクトは、基本、自身とペアレント関係に無い場合は、関数や、クラスをまたいで利用できません。

`Internal C++ object ~ already deleted.` みたいなエラーが出る時がそれです。自分は *オブジェクトの寿命が切れた* とか言って、良く席でひとり唸ってます。

エラーが出たら、素直に、関数内で再検索してから使いましょう。
DCC系ツールで、コード整理中に関数をまとめたりしてると、意外と良くハマるので書いておきます。

# PySide

これで、準備が整いました。後は *Maya* ではなく、*PySide* の話になります。

## モジュールの読み込み

自分は、Pysideを読む時は、こんな感じで書いてます。

``` python
# 分岐必要ある時は付けたりします
isPySide2 = False

try:
    from PySide2.QtWidgets import * 
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    isPySide2 = True

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
```

**PySide2** を上に書いてるのは、読み込む優先度を上げる為です。
*PySide* をtryに書くと、*PySide* がなかったら…、と言う意味になります。

`PYTHONPATH` に *PySide* が含まれてた場合、*Maya* の推奨のバージョン無視して *PySide* を使う可能性がある為です。

逆の事も言えますが、*maya2014* とかで、**Python2** 用にわざわざ自分でコンパイルして、`PYTHONPATH` に、**PySide2** のパスを通す奴は、まず居ないと思います。

## QMenu

`QMenu` は、`QDialog` みたいに、自身をアプリケーションのように振る舞う事ができ、他のスレッドを待機させる事が出来る、`exec_()` メソッドが用意されてます。

待機させる処理を、イベントループといい、スタンドアローンを作る際に、`QApplication` でオマジナイみたいに使ってるアレと同じです。

`QMenu` だと、 `popup()` メソッドも用意されてて、同じような動作します。
こちらは、目的の位置を指定する事で、マウスカーソルの位置に表示させる事ができます。

`QMenu` のドキュメント見ると、`exec_()` は、`popup()` をオーバーライドしてるだけで、多分、カーソルの位置を引数で渡した場合は、同じコマンドが実行されてると思います。`exec_()` は引数省略出来ますが、`popup()` は出来ません。

これを利用して、右クリックメニューや、ショートカットで起動する、簡易ランチャー的な物などを作る事が可能になります。

## QAction

`QAction` は、簡単にアクション(メニューコマンド)を作れるテンプレートみたいなもので、非常に便利ですが、アイコンと、チェックボックス位しかカスタマイズ出来ません。

`QWidgetAction` を使うと、自分で好きなウィジェットでアクションを作る事が可能です。`QWidgetAction` は、`QAction`を継承してるので、通常のアクションと同じように扱え、メニューに追加できます。

*Maya* メニューは、ツールオプションがアイコンで用意されてるので、`QWidgetAction` を利用して作られてるみたいです。

## アクションの検索

なぜ、*Maya* の機能を使わずに、*PySide* だけで、こんなツールが作れるかと言うと、`mel` や、`maya.cmds` で作成したウインドウや、コントロールも、すべてQtに変換されて作られてるからです。

なので、名前を付けておけば、*PySide* の `QWidget` として取得出来ます。
いったんオブジェクトとして取得できれば、後は、*PySide* の機能をフルに扱う事が出来ます。

*Maya* のコマンドは、いわば、*PySide* の、warpperみたいな役割をしています。
ぶっちゃけ、さほど便利になってないので、wrapperと言うより、旧MELコマンドの、ウインドウや、コントロールを、Qtで再現してるだけと言った感じですが…。

存在しないFrameLayoutとかは、独自UIとして実装されてますが、作成するとQWidgetとして取得出来るので、自分の *PySide* ツールに組み込む事も可能です。

## 履歴の登録

せっかくアクションを、`QAction` として、オブジェクトで取得したので、自前の `QMenu` に入れてしまいます。

同じコマンドを何度登録しても、`QAction` の実態はひとつなので、同じメニューに二回目以上登録しても、順番が新しくなるだけで重複しません。この挙動は、まさに履歴にそっくりなので、そのまま使ってます。

`QAction` は、元々複数のウィジェットで使い回す想定の仕組みになってるので、まったく同じアクションを、`QToolBar`, `QMenu`, `QSystemTrayIcon` などで、同時に共存させる事が出来ます。超便利です。

melからのアクセスだと、*ペアレントを変える＝移動* なので、こう言った融通が効きません。

# ツール紹介

## ダウンロード

以上説明した技術を使い、ツールを作ってみました。
こちらからダウンロードできます。

> [Dwonload / Maya / Python / ubSearchMenu](https://unitbus.github.io/pages/download)

ダウンロードしたファイルは、`Documents/maya/scripts` に置いてください。
スクリプトエディタで以下のコマンドを実行するとメニューに追加されます。

``` python
import ubSearchMenu
ubSearchMenu.show()
```

## ショートカットに登録

ショートカット用のコマンドも用意してあります。
カーソルの位置にメニューを出せるので、登録しておくと便利かと思います。

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubSearchMenu_mayaPressHotkeyA.png">
</p>

自分は、 **Hide All UI Elements** は使わないので、 **[Ctrl + Space]** に登録してます。`Hotkey Editor > Rantime Command Editor` から、 **Python** を選んで、下のコマンドを登録してください。

```python
import ubSearchMenu
ubSearchMenu.popMenu()
```

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubSearchMenu_mayaHotkeyEditorA.png">
</p>

## 補足

*Maya* のメニューは表面だけ作成されてて、アクセス時にMELコマンドで作成される仕様の物が多いです。表面的なメニューは、インポート時にロードするようにしましたが、実際に一度メニューの場所までアクセスしないと、検索に出てこないコマンドもあるかと思います。

よく使うメニューが隠れてる場合は、**ScriptEditor > Echo ALL** で表示される、メニュー作成コマンドを見つけて、自分で足してください。

初回起動時に、数秒ロードが入るので、遅いと感じる人は、逆に、使わないメニューコマンドをコメントアウトしちゃってください。

少し書き換えれば、他のDCCでも使えると思います。`SearchMenu` クラスは、*PySide* だけで書いてあるので、そのまま使えると思います。*Maya* のウィジェットを探してる部分だったりを、DCC別に合わせて書き換える感じです。

*Nuke* は、試してませんが、多分、同じ要領でイケると思います。

*Houdini* は、ほぼ自前UIなので、*PySide* でアクセスできる部分が少ないです。メニューバーも独自仕様なので、追加するには、houモジュール経由でアクセスするしかありません。

## 余談

履歴の保存とか出来れば便利かな、とも思いましたが、記事のボリュームが結構大きくなったのでやめました。需要あれば考えますが、独自のカスタマイズを望む方は、お仕事として相談して頂けると嬉しいです。笑

# 最後に

ちまたに溢れるCGネタを肴に盛り上がれたらと思い、*Slack* 始めました。
お気軽に参加してください。参加の仕方がわからない方は、Twitterのダイレクトメッセージをして貰えれば招待送りします。

> Unitbus Slack.
> [https://unitbus.slack.com](https://unitbus.slack.com)

> UnitBus Twitter.
> [https://twitter.com/UnitBus](https://twitter.com/UnitBus)

お仕事の相談も募集してます。フルタイム勤務は無理ですが、細かいツールの依頼や、ワークフローの改善案など、おチカラになれそうな相談事あればご連絡ください。
お仕事の話も、メールで頂くより、Slackのダイレクトメッセージで頂けると嬉しいです。
