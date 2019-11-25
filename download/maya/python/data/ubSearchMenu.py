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
    #     1.0.0, 2019/12/03
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
import pprint
import traceback

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
        
        self.setTearOffEnabled(False)
        self.setBaseSize(60, 24)
        self.setObjectName('ubSearchMenu')
        
        self.__lineEdit = None
        self.__recentActions = []
        self.__actionTexts = [a.text() for a in getChildActions(parent)]
        self._initWidget(parent)
    
    def _initWidget(self, parent):
        widget = QWidget(self)
        widget.setBaseSize(120, 24)
        widget.setMinimumWidth(120)
        widget.setObjectName('ubSearchWidget')
        
        completer = QCompleter(self.__actionTexts, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        
        lineEdit = QLineEdit(widget)
        lineEdit.setPlaceholderText(r'<Enter wildcard>')
        lineEdit.setCompleter(completer)
        lineEdit.setFocus(Qt.TabFocusReason)
        lineEdit.returnPressed.connect(self.returnPressedFunc)
        self.__lineEdit = lineEdit
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(4)
        layout.addWidget(lineEdit)
        
        action = QWidgetAction(self)
        action.setDefaultWidget(widget)
        action.setObjectName('ubSearchAction')
        self.addAction(action)
    
    def lineEdit(self):
        return self.__lineEdit
    
    def appendAction(self, action):
        
        if not self.__recentActions:
            separator = QWidgetAction(self)
            separator.setDefaultWidget(QLabel('Recent Action'))
            separator.setObjectName('ubRecentAction')
            
            self.addAction(separator)
            self.addSeparator()
        
        self.__recentActions = [action]
        self.addAction(action)
    
    # signal.
    def returnPressedFunc(self, *args, **kwargs):
        text = self.__lineEdit.text()
        parent = self.parent()
        
        for action in getChildActions(parent):
            
            if text != action.text():
                continue
            
            print(text, action)
            action.trigger()
            
            self.appendAction(action)
            self.setVisible(False)
            return

# actionを検索
def getChildActions(menuBar):
    actions = []
    
    for menu in menuBar.findChildren(QMenu):
        action = menu.defaultAction()
        action and action.activate()
        
        widgets = getDeepChildren(menu, results=[])
        actions += [w for w in widgets if isinstance(w, (QAction, QWidgetAction))]
    
    return actions

# 再帰的に子を検索
def getDeepChildren(widget, results=[], depth=0, depthLimit=10):
    
    if depth >= depthLimit:
        return results
    
    hasattr(widget, 'update') and widget.update()
    
    if not hasattr(widget, 'children'):
        return results
    
    results += widget.findChildren(QAction)
    
    for child in widget.children():
        
        if not child.children():
            continue
        
        getDeepChildren(child, results=results, depth=depth+1, depthLimit=depthLimit)
    
    return results

# maya.
def getMayaWidget(name):
    widgets = QApplication.topLevelWidgets()
    
    for widget in widgets:
        if widget.objectName() == name:
            return widget
    
    return None

# maya shortcut commnd.
def popMenu():
    # menuBar = getMayaWidget('MainHelpMenu').parent()
    
    window = getMayaWidget('MayaWindow')
    menuBar = window.findChild(QMenuBar)
    
    menu = menuBar.findChild(QMenu, 'ubSearchMenu')
    menu = menu or SearchMenu('Search', menuBar)
    menu.lineEdit().setFocus(Qt.TabFocusReason)
    menu.popup(QCursor.pos())

# maya append menuBar.
def show():
    # menuBar = getMayaWidget('MainHelpMenu').parent()
    
    window = getMayaWidget('MayaWindow')
    menuBar = window.findChild(QMenuBar)
    print('menuBar:', menuBar)
    
    menu = menuBar.findChild(QMenu, 'ubSearchMenu')
    
    if menu:
        menu.deleteLater()
        print('Rebuild ubSearchMenu.')
    
    menu = SearchMenu('Search', menuBar)
    menuBar.addMenu(menu)

# standalone debug.
def sample():
    mainApp = QApplication(sys.argv)
    
    def rightClickFunc(pos):
        searchMenu.lineEdit().setFocus(Qt.TabFocusReason)
        searchMenu.popup(QCursor.pos())
    
    # 右クリックメニュー
    window = QMainWindow()
    window.setContextMenuPolicy(Qt.CustomContextMenu)
    window.customContextMenuRequested.connect(rightClickFunc)
    window.show()
    
    # メニュー
    testMenu = QMenu('Test')
    testMenu.addAction('actionA')
    testMenu.addAction('actionB')
    testMenu.addAction('actionC')
    
    searchMenu = SearchMenu('Search', window)
    
    # メニューバー
    menuBar = window.menuBar()
    menuBar.addMenu(testMenu)
    menuBar.addMenu(searchMenu)
    
    mainApp.exec_()

if __name__ == '__main__':
    sample()
