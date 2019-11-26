<!-- このファイルはMarkdown形式で書かれています。-->

<!-- TOC -->

- [挨拶](#挨拶)
- [完成イメージ](#完成イメージ)
- [Mayaの話](#mayaの話)
    - [shiboken](#shiboken)
    - [MayaQWidgetBaseMixin](#mayaqwidgetbasemixin)
    - [PySideのウィジェットを探す](#pysideのウィジェットを探す)
    - [windowの取得](#windowの取得)
    - [menuBarの取得](#menubarの取得)
    - [メモ](#メモ)
- [PySide](#pyside)
    - [QMenu](#qmenu)
    - [QAction](#qaction)
- [ツールの紹介](#ツールの紹介)
    - [ダウンロード](#ダウンロード)
    - [ショートカットに登録](#ショートカットに登録)
- [最後に](#最後に)

<!-- /TOC -->

# 挨拶

近況報告としては、前の会社を辞めた際に、アーティストは引退し、テック側に転職しました。
もともとは、ジェネラリストで、TAっぽい仕事が多かったですが、テックに移って4年近く経ち、
今はもう、画作りにほぼ関わってないので、TAですらありません。笑

転職と共に、Pythonを覚える必要があり、世間と比べても、ちょっと遅めのデビューとなりました。
デビューが遅かったおかげか、色々なサイトを見て勉強させて頂く事が出来ました。

特に、色々カスタマイズされたPySideの記事を見かけ、モチベーション高く学習する事ができました。
この場を借りてお礼を言いたいと思います。ありがとうございました。

メニューに関するネタをあまり見かけなかったので、恩返しという訳ではありませんが、
情報共有に貢献出来たらと思い、記事にしました。

# 完成イメージ

作り方だけ書いてもあまりピンとこないと思うので、ある程度実用性のあるツールにしてみました。
Mayaの他のメニューからアクションを探し、実行するツールです。
ダウンロードと、使い方の説明は、[ツール紹介](#ツール紹介)を見てください。

![mayaPressMenuA](https://unitbus.github.io/pages/maya/images/ubSearchMenu_mayaPressMenuA.png) 

# Mayaの話

MayaのUIは、Qtで作られてるため、すべてのウィジェットに、PySideからアクセス出来ます。
例えば、Mayaの、メインウインドウを取得したいだけなら、
`shiboken` や、`MayaQWidgetBaseMixin` を使う必要はありません。
オブジェクト名がわかれば、PySideとしてWidgetを検索し、取得できます。

## shiboken

`shiboken` は、ざっくり言うと、DCCとPySideを繋ぐ為のモジュールです。
DCC独自のウィジェットにアクセスしたい時などに使う？らしいです。
目的に対して、ちょっと大げさなのもあり、自分はこのモジュールを使った事がありません。

## MayaQWidgetBaseMixin

`MayaQWidgetBaseMixin` は、Maya側が用意してるPySide用のクラスです。
便利なクラスですが、parent先を取得する為だけに、
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
一覧で見れるビューワーがあると便利だと思い用意しました。

<img src="https://unitbus.github.io/pages/maya/images/ubWidgetHierarchy_windowA.png" width="50%">

> ダウンロード / ubWidgetHierarchy.py
https://unitbus.github.io/pages/download

余談ですが、melや、maya.cmdsで作成したウインドウも、
名前を付けておけば、PySideの `QWidget` として取得出来ます。

目的のウィジェットが事前に分かれば、後は名前で検索するだけです。
いったんオブジェクトとして取得できれば、以降PySideの機能をフルに扱う事が出来ます。

Mayaのメインウインドウ名は、`MayaWindow` になります。

## windowの取得

`objectName()` や、`windowTitle()` から取得する方法があります。
この方法は、他のDCCでも使えるので、覚えておくと便利だと思います。

> Maya / PySide / MainWindowの取得
https://unitbus.github.io/pages/maya/pyside#mainwindowの取得

## menuBarの取得

今回は、parent先はmenuBarなので、menuBarを取得したいのですが、
`MayaWindow` の、menuBarには `objectName()` が設定されてません。

また、`MayaWindow` は、`QMainWindow` を使わず、`QWidget` で作成されてるため、
`QMainWindow.menuBar()` メソッドが存在せず、取得できません。

なので、`QWindow` から探す必要があります。

``` python
from PySide2.QtGui import *

def getMayaWidget(name):
    
    for widget in QApplication.topLevelWidgets():
        
        if widget.objectName() == name:
            return widget
    
    return None

window = getMayaWidget('MayaWindow')
menuBar = window.findChild(QMenuBar)
```

他にも、`HelpMenu` を先に取得し、親ウィジェットを探す方法もあります。

## メモ

`children()`, `findChildren()` 等で取得したオブジェクトは、
基本、自身とペアレント関係に無い場合は、関数をまたいで利用できません。

`Internal C++ object ~ already deleted.` みたいなエラーが出る時がそれです。

素直に、関数内で再検索してから使いましょう。
ちょっとハマったので、書いておきます。

# PySide

これで、準備が整いました。後はMayaではなく、PySideの話になります。

## QMenu

`QMenu` は、`QDialog` みたいに、自身をアプリケーションのように振る舞う事ができ、
他のスレッドを待機させる事が出来る、`exec_()` メソッドが用意されてます。

待機させる処理を、イベントループといい、スタンドアローンのを作る時に、
`QApplication` でオマジナイみたいに使ってるアレと同じです。

`QMenu` だと、 `popup()` メソッドも用意されてて、同じような動作します。
こちらは、目的の位置を指定する事で、マウスカーソルの位置に表示させる事ができます。

これを利用して、右クリックメニューや、ショートカットで起動するランチャー的な物などを作る事が可能になります。

## QAction

`QAction` は、簡単にアクションを作れるテンプレートみたいなもので、非常に便利ですが、
アイコンと、チェックボックス位しかカスタマイズ出来ません。

`QWidgetAction` を使うと、自分で好きなウィジェットでアクションを作る事が可能です。
`QWidgetAction` は、`QAction`を継承してるので、通常のアクションと同じように扱え、メニューに追加できます。

Mayaのメニューツールのオプションボックスは、これを利用して配置されてます。

# ツールの紹介

## ダウンロード

以上説明した技術を使い、ちょっと実用性を持たせ作成したツールを作ってみました。
こちらからダウンロードできます。

> Dwonload / Maya / Python / ubSearchMenu
https://unitbus.github.io/pages/download

ダウンロードしたファイルは、`Documents/maya/scripts` に置いてください。
スクリプトエディタで以下のコマンドを実行するとメニューに追加されます。

```python
import ubSearchMenu
ubSearchMenu.popMenu()
```

Mayaのメニューの仕様で、一度アクセスしないと出てこないコマンドもあります。
PySideだけで書かれてるので、対象のウィジェット名を変えれば、他のDCCでも使えると思います。

履歴の保存とか出来れば便利かな、とも思いましたが、
記事のボリュームが結構大きくなったのでやめました。
需要あれば考えます。

## ショートカットに登録

ショートカット用のコマンドも用意してあります。
カーソルの位置にメニューを出せるので、登録しておくと便利かと思います。

![ubSearchMenu_mayaPressHotkeyA](https://unitbus.github.io/pages/maya/images/ubSearchMenu_mayaPressHotkeyA.png)

自分は、 `Hide All UI Elements` は使わないので、 `Ctrl + Space` に登録してます。
`Hotkey Editor > Rantime Command Editor` で、 `Python` で下のコマンド登録してください。

```python
import ubSearchMenu
ubSearchMenu.popMenu()
```

<img src="https://unitbus.github.io/pages/maya/images/ubSearchMenu_mayaHotkeyEditorA.png" width="50%">

# 最後に

ちまたに溢れるCGネタを肴に盛り上がれたらと思い、Slack始めました。
お気軽に参加してください。

https://unitbus.slack.com 

お仕事の相談も募集してます。フルタイム勤務は無理ですが、細かいツールの依頼や、
ワークフローの改善案の相談など、おチカラになれそうな事あればご連絡ください。
