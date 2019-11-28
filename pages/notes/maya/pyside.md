---
layout: default
title: Maya
---

# PySide

## MayaのWidget一覧

PySideから見た、Mayaのウィジェットを一覧で見れるビューワー。

[Widget一覧](https://unitbus.github.io/pages/notes/python/pyside#widget一覧)

## MainWindowの取得

`QWidget.objectName()` から取得

``` python
from PySide2.QtGui import *

def getTopLevelWidget(name):
    
    for widget in QApplication.topLevelWidgets():
        
        if widget.objectName() == name:
            return widget
    
    return None

getTopLevelWidget('MainWindow')
```

`QWidget.windowTitle()` から取得

``` python
from PySide2.QtGui import *

def getTopLevelWidget(title):
    
    for widget in QApplication.topLevelWidgets():
        
        if title in widget.windowTitle():
            return widget
    
    return None

getTopLevelWidget('Autodesk Maya')
```
