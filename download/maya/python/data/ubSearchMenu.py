# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
    # Dependencies:
    #     Python2.
    # 
    # Description:
    #     Maya Custom Menu Widget.
    # 
    # Configuration:
    #     Maya2016 - 2019.
    # 
    # Author:
    #     (C) 2019 Co, UnitBus.
    # 
    # Version:
    #     1.0.0, 2019/11/26
    #
    # Exsample:
    #     import ubSearchMenu
    #     ubSearchMenu.appendMayaMenu()
    #
    #     # shortcut runtime command.
    #     import ubSearchMenu
    #     ubSearchMenu.popMenu()

from __future__ import print_function
from __future__ import unicode_literals

import sys

try:
    import PySide2
    from PySide2.QtWidgets import * 
    from PySide2.QtCore import *
    from PySide2.QtGui import *

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *

class SearchMenu(QMenu):
    
    def __init__(self, title, parent=None):
        super(SearchMenu, self).__init__(title, parent=parent)
        
        self.setObjectName('ubSearchMenu')
        self.setTearOffEnabled(False)
        self.setBaseSize(160, 24)
        
        self.__lineEdit = None
        self.__recentActions = []
        self.__actionTexts = []
        
        # init.
        self._initWidget()
        self._updateActions()
    
    # signal.
    def _returnPressedFunc(self, *args, **kwargs):
        text = self.__lineEdit.text()
        
        # for action in getChildActions(self.parent()):
        
        menuBar = self.parent()
        
        for menu in menuBar.findChildren(QMenu):
            widgets = getDeepChildren(menu, results=[], depth=0, depthLimit=6)
            actions = [w for w in widgets if isinstance(w, (QAction, QWidgetAction))]
            
            for action in actions:
                
                if text != action.text():
                    continue
                
                print(text, action)
                action.trigger()
                
                self.addRecentAction(action)
                self.setVisible(False)
                return
    
    def _updateActions(self):
        self.__actionTexts = []
        menuBar = self.parent()
        
        for menu in menuBar.findChildren(QMenu):
            widgets = getDeepChildren(menu, results=[], depth=0, depthLimit=6)
            self.__actionTexts += [w.text() for w in widgets if isinstance(w, (QAction, QWidgetAction))]
        
        completer = QCompleter(self.__actionTexts, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        
        self.__lineEdit.setCompleter(completer)
    
    # method.
    def _initWidget(self):
        widget = QWidget(self)
        widget.setMinimumWidth(160)
        widget.setObjectName('ubSearchWidget')
        
        lineEdit = QLineEdit(widget)
        lineEdit.setPlaceholderText(r'<Enter wildcard>')
        lineEdit.setFocus(Qt.TabFocusReason)
        lineEdit.returnPressed.connect(self._returnPressedFunc)
        self.__lineEdit = lineEdit
        
        styleText = ''
        styleText += r'QPushButton{{background-color: none;}} '
        
        button = QPushButton(widget)
        button.setText('')
        button.setIcon(QPixmap(':/refresh'))
        button.setIconSize(QSize(16, 16))
        button.setMaximumSize(QSize(16, 16))
        button.setFlat(True)
        button.setStyleSheet(styleText)
        button.pressed.connect(self._updateActions)
        button.setToolTip(u'検索候補に出てこない場合は押してください')
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)
        layout.addWidget(lineEdit)
        layout.addWidget(button)
        
        action = QWidgetAction(self)
        action.setDefaultWidget(widget)
        action.setObjectName('ubSearchAction')
        self.addAction(action)
    
    def addRecentAction(self, action):
        
        if not self.__recentActions:
            separator = QWidgetAction(self)
            separator.setDefaultWidget(QLabel('Recent Action'))
            separator.setObjectName('ubRecentAction')
            
            self.addAction(separator)
            self.addSeparator()
        
        self.__recentActions = [action]
        self.addAction(action)
    
    def lineEdit(self):
        return self.__lineEdit

# 再帰的に子を検索
def getDeepChildren(widget, results=[], depth=0, depthLimit=6):
    
    if depth >= depthLimit:
        return results
    
    if hasattr(widget, 'update'):
        widget.update()
    
    if not hasattr(widget, 'children'):
        return results
    
    results += widget.findChildren(QAction)
    
    for child in widget.children():
        
        if not child.children():
            continue
        
        getDeepChildren(child, results=results, depth=depth+1, depthLimit=depthLimit)
    
    return results

def getTopLevelWidget(name):
    
    for widget in QApplication.topLevelWidgets():
        
        if widget.objectName() == name:
            return widget
    
    return None

# maya shortcut commnd.
def popMenu():
    window = getTopLevelWidget('MayaWindow')
    menuBar = window.findChild(QMenuBar)
    
    menu = menuBar.findChild(QMenu, 'ubSearchMenu')
    menu = menu or SearchMenu('Search', menuBar)
    
    lineEdit = menu.lineEdit()
    lineEdit.setFocus(Qt.TabFocusReason)
    lineEdit.selectAll()
    
    menu.popup(QCursor.pos())

# maya append menuBar.
def show():
    window = getTopLevelWidget('MayaWindow')
    menuBar = window.findChild(QMenuBar)
    print('menuBar:', menuBar)
    
    menu = menuBar.findChild(QMenu, 'ubSearchMenu')
    
    if menu:
        menu.deleteLater()
        print('Rebuild ubSearchMenu.')
    
    menu = SearchMenu('Search', menuBar)
    menuBar.addMenu(menu)
