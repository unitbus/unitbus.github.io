# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
    # Dependencies:
    #     Python2.
    # 
    # Description:
    #     Widget Hierarchy.
    # 
    # Configuration:
    #     Maya2016 - 2019.
    # 
    # Author:
    #     (C) 2019 Co, UnitBus.
    # 
    # Version:
    #     0.1.0, 2019/11/25
    #
    # Exsample:
    #     import ubWidgetHierarchy
    #     ubWidgetHierarchy.show()

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

def makeTreeItem(widget, parent=None, depth=0, depthLimit=10):
    
    def makeColumns(widget):
        text = '<noattr>'
        text = widget.text() if hasattr(widget, 'text') else text
        text = widget.title() if hasattr(widget, 'title') else text
        text = widget.windowTitle() if hasattr(widget, 'windowTitle') else text
        
        columns = [
            widget.objectName() or '<empty>',
            text,
            unicode(type(widget)),
            ]
        return columns
    
    if depth >= depthLimit:
        return None
    
    if not hasattr(widget, 'children'):
        return None
    
    item = QTreeWidgetItem(parent, makeColumns(widget))
    
    for child in widget.children():
        
        if child.children():
            makeTreeItem(child, parent=item, depth=depth+1, depthLimit=depthLimit)
        
        else:
            subItem = QTreeWidgetItem(item, makeColumns(child))
    
    return item

def hierarchyWindow(parent):
    topWidgets = sorted(QApplication.topLevelWidgets(), key=lambda x: x.objectName())
    topItems = [makeTreeItem(w) for w in topWidgets]
    
    treeWidget = QTreeWidget()
    treeWidget.setColumnCount(2)
    treeWidget.setHeaderLabels(['name', 'text/title', 'type'])
    treeWidget.addTopLevelItems(topItems)
    
    window = QMainWindow(parent)
    window.setCentralWidget(treeWidget)
    window.resize(640, 640)
    window.setObjectName('ubHierarchyWindow')
    window.setWindowTitle('ubHierarchyWindow')
    return window

def show():
    window = hierarchyWindow(None)
    window.show()
