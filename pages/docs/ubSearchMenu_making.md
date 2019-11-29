---
layout: default
title: ubSearchMenu Making
---

# 挨拶

近況報告としては、前の会社を辞めた際に、アーティストは引退し、テック系CG屋に転職しました。
もともとは、ジェネラリストで、TAっぽい仕事が多かったですが、テックに移って4年近く経ち、
今はもう、画作りにほぼ関わってないので、TAですらありません。笑

転職と共に、Pythonを覚える必要があり、世間と比べても、ちょっと遅めのデビューとなりました。
デビューが遅かったおかげか、色々なサイトを見て勉強させて頂く事が出来ました。

特に、PySideの記事を多く見かけ、色々カスタマイズされたUIを見て、
モチベーション高く学習を続ける事ができました。
この場を借りて、多くの方にお礼を言いたいと思います。ありがとうございました。

メニューに関するネタをあまり見かけなかったので、恩返しという訳ではありませんが、
自分も情報共有に貢献出来たらと思い、記事にしました。

**このページは、Maya Advent Calendar 2019 12/3用に書かれています。**

> Maya Advent Calendar 2019
https://qiita.com/advent-calendar/2019/maya

## 完成イメージ

作り方だけ書いてもあまりピンとこないと思うので、ある程度実用性のあるツールにしてみました。
Mayaの他のメニューからアクションを探し、実行するツールです。
ダウンロードと、使い方の説明は、[ツール紹介](#ツール紹介)を見てください。

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubSearchMenu_mayaPressMenuA.png">
</p>

# Mayaの話

MayaのUIは、Qtで作られてるため、すべてのウィジェットに、PySideからアクセス出来ます。
例えば、Mayaの、メインウインドウを取得したいだけなら、
**shiboken** や、**MayaQWidgetBaseMixin** を使う必要はありません。
オブジェクト名がわかれば、PySideとしてWidgetを検索し、取得できます。

## shiboken

**shiboken** は、ざっくり言うと、DCCとPySideを繋ぐ為のモジュールです。
DCC独自のウィジェットにアクセスしたい時などに使う？らしいです。

PySideが、サイズが大きくて切り離した的なコメントも見かけますし、
目的に対して、ちょっと大げさなのもあり、自分はこのモジュールを使った事がありません。

## MayaQWidgetBaseMixin

**MayaQWidgetBaseMixin** は、Maya側が用意してるPySide用のクラスです。
便利なクラスですが、ペアレント先を取得する為だけに、
バージョンで仕様がコロコロ変わるMayaのモジュールを読みたくはありません。

都度DCCを起動したりデバッグも大変ですし、自分は、ウィジェット作成中は、
なるべくMayaのモジュールは読まず、スタンドアローンで動くようにしています。

## PySideのウィジェットを探す

通常、PySideで作成されたウィジェットには、オブジェクト名が付いています。
オブジェクト名がわかれば、Mayaから、ウィジェットをオブジェクトで取得する事が出来ます。

Mayaでツールを作成する場合、既に数多くあるツールの中の一つとして動作するので、
決め打ちで、ハードコーディングしてしまった方が、レスポンス的に都合が良く、
特にメニュー系などは、都度検索するよりも、速度的にも重要な場面が多いです。

初めてMayaのウィジェットにアクセスする際に、
一覧で見れるビューワーがあると便利だと思い作っていました。

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubWidgetHierarchy_windowA.png">
</p>

> [ダウンロード / ubWidgetHierarchy](https://unitbus.github.io/pages/download)

ちなみに、Mayaのメインウインドウ名は、**MayaWindow** になります。
目的のウィジェットが事前に分かれば、後は名前で検索するだけです。

## windowの取得

`objectName()` や、`windowTitle()` から取得する方法があります。
この方法は、他のDCCでも使えるので、覚えておくと便利だと思います。

> [Maya / PySide / MainWindowの取得](https://unitbus.github.io/pages/notes/maya/pyside#mainwindowの取得)

## menuBarの取得

今回は、parent先はmenuBarなので、menuBarを取得したいのですが、
**MayaWindow** の、menuBarには `objectName()` が設定されてません。

また、**MayaWindow** は、`QMainWindow` を使わず、`QWidget` で作成されてるため、
`QMainWindow.menuBar()` メソッドが存在せず、取得できません。

なので、`QWindow` から、辿って探す必要があります。

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

`children()`, `findChildren()` 等で取得したオブジェクトは、
基本、自身とペアレント関係に無い場合は、関数をまたいで利用できません。

`Internal C++ object ~ already deleted.` みたいなエラーが出る時がそれです。
自分は *オブジェクトの寿命が切れた* とか言って、良く席で唸ってます。

素直に、関数内で再検索してから使いましょう。
DCC系ツールで、コード整理中に関数をまとめたりしてると、意外とハマるので書いておきます。

# PySide

これで、準備が整いました。後はMayaではなく、PySideの話になります。

## モジュールの読み込み

自分はこんな感じで書いてます。

``` python
try:
    from PySide2.QtWidgets import * 
    from PySide2.QtCore import *
    from PySide2.QtGui import *

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
```

**PySide2** を上に書いてるのは、読み込む優先度を上げる為です。
*PySide* をtryに書くと、*PySide* がなかったら…、と言う意味になります。

PYTHONPATHに *PySide* が含まれると、Mayaの推奨のバージョン無視して
*PySide* を使う可能性がある為です。

逆の事も言えますが、maya2014とかで、Python2用にわざわざ自分でコンパイルして、
PySide2にパス通す奴は、まず居ないと思います。

## QMenu

`QMenu` は、`QDialog` みたいに、自身をアプリケーションのように振る舞う事ができ、
他のスレッドを待機させる事が出来る、`exec_()` メソッドが用意されてます。

待機させる処理を、イベントループといい、スタンドアローンを作る際に、
`QApplication` でオマジナイみたいに使ってるアレと同じです。

`QMenu` だと、 `popup()` メソッドも用意されてて、同じような動作します。
こちらは、目的の位置を指定する事で、マウスカーソルの位置に表示させる事ができます。

`QMenu` のドキュメント見ると、`exec_()` は、`popup()` をオーバーライドしてるだけで、
多分、カーソルの位置を引数で渡した場合は、同じコマンドが実行されてると思います。
`exec_()` は引数省略出来ますが、`popup()` は出来ません。

これを利用して、右クリックメニューや、ショートカットで起動するランチャー的な物などを作る事が可能になります。

## QAction

`QAction` は、簡単にアクション(メニューコマンド)を作れるテンプレートみたいなもので、非常に便利ですが、
アイコンと、チェックボックス位しかカスタマイズ出来ません。

`QWidgetAction` を使うと、自分で好きなウィジェットでアクションを作る事が可能です。
`QWidgetAction` は、`QAction`を継承してるので、通常のアクションと同じように扱え、メニューに追加できます。

Mayaメニューの、ツールオプションボックスは、これを利用して作られてました。

## アクションの検索

なぜ、Mayaなのに、PySideだけで、こんなツールが作れるかと言うと、
melや、maya.cmdsで作成したウインドウや、コントロールもすべてQtで作られてるからです。

なので、名前を付けておけば、PySideの `QWidget` として取得出来ます。
いったんオブジェクトとして取得できれば、以降PySideの機能をフルに扱う事が出来ます。

Mayaのコマンドは、いわば、PySideのwarpperみたいな役割をしています。
ぶっちゃけ、さほど便利になってないので、wrapperと言うより、
旧MELコマンドの、ウインドウや、コントロールを再現してるだけと言った感じですが…。

## 履歴の登録

せっかくアクションを、`QAction` として、オブジェクトで取得したので、自前の `QMenu` に入れてしまいます。

同じコマンドを何度登録しても、`QAction` の実態はひとつなので、二回目以降は順番が新しくなるだけです。
この挙動は、まさに履歴にそっくりなので、そのまま使ってます。

`QAction` は、元々複数のウィジェットで使い回す想定の仕組みになってるので、まったく同じオブジェクトを、
`QToolBar`, `QMenu`, `QSystemTrayIcon` などで、同時に共存させる事が出来ます。超便利です。

melからのアクセスだと、*ペアレントを変える＝移動* なので、こう言った融通が効きません。

# ツール紹介

## ダウンロード

以上説明した技術を使い、ちょっと実用性を持たせ作成したツールを作ってみました。
こちらからダウンロードできます。

> [Dwonload / Maya / Python / ubSearchMenu](https://unitbus.github.io/pages/download)

ダウンロードしたファイルは、`Documents/maya/scripts` に置いてください。
スクリプトエディタで以下のコマンドを実行するとメニューに追加されます。

```python
import ubSearchMenu
ubSearchMenu.show()
```

## ショートカットに登録

ショートカット用のコマンドも用意してあります。
カーソルの位置にメニューを出せるので、登録しておくと便利かと思います。

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubSearchMenu_mayaPressHotkeyA.png">
</p>

自分は、 **Hide All UI Elements** は使わないので、 **[Ctrl] + [Space]** に登録してます。
`Hotkey Editor > Rantime Command Editor` から、 **Python** を選んで、下のコマンドを登録してください。

```python
import ubSearchMenu
ubSearchMenu.popMenu()
```

<p class="resizeimage">
<img src="https://unitbus.github.io/images/docs/ubSearchMenu_mayaHotkeyEditorA.png">
</p>

## 補足
Mayaのメニューは表面だけ作成されてて、アクセス時にMELコマンドで作成される仕様の物が多いです。
表面的なメニューは、インポート時にロードするようにしましたが、
実際に一度アクセスしないと出てこないコマンドもあるかと思います。

よく使うメニューが隠れてる場合は、**ScriptEditor > Echo ALL** で出てくる、
メニュー作成コマンドを見つけて、自分で足してください。

初回起動時に、数秒ロードが入るので、遅いと感じる人は、
逆に、使わないメニューコマンドをコメントアウトしちゃってください。

ほぼ、PySideだけで書いてあるので、少し書き換えれば、他のDCCでも使えると思います。
`Class` はそのまま使えると思います。mayaのウィジェットを探してる部分だったりをDCCに合わせて書き換える感じです。

Nukeは、試してませんが、多分、同じ要領でイケると思います。

Houdiniは、ほぼ自前UIなので、PySideでアクセスできる部分が少ないです。
メニューバーも独自仕様なので、追加するには、houモジュール経由でアクセスするしかありません。

## 余談

履歴の保存とか出来れば便利かな、とも思いましたが、
記事のボリュームが結構大きくなったのでやめました。

需要あれば考えます。独自のカスタマイズを望む方は、
お仕事として相談して頂けると嬉しいです。笑


# 最後に

ちまたに溢れるCGネタを肴に盛り上がれたらと思い、Slack始めました。
お気軽に参加してください。

> Unitbus Slack.
> https://unitbus.slack.com

お仕事の相談も募集してます。フルタイム勤務は無理ですが、細かいツールの依頼や、
ワークフローの改善案など、おチカラになれそうな相談事あればご連絡ください。

> UnitBus Twitter.
> https://twitter.com/UnitBus
