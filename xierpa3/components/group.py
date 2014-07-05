# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    group.py
#
from xierpa3.components.container import Container
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint
from xierpa3.attributes import Perc

class Group(Container):
    pass

class ItemGroup(Group):
    u"""The <b>ItemGroup</b> implements a group with automatic responsive behavior for groups of items. 
    Defined by a range of widths, a group of items is scaled to stay on the same line. If the screen width
    changes, then then the <b>clear</b> attribute is shifted value, so the line break takes place between another 
    set of items."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Group.C 
    
    BLUEPRINT = BluePrint(
        # Selection stuff
        itemStart=0, 
        itemCount=12, # Index of first and last selected thumbnail for this component
        # Layout stuff
        colWidth=12,
        # Group stuff
        groupBackgroundColor=None, # Background image of the item row.
        # Range of items in one row and the corresponding widths
        #itemRange=range(3, 6),
        #mediaWidths=(C.M_MOBILE_MAX)
        columns=5,
    )
    def buildBlockRow(self, b):
        s = self.style
        b.div(class_=self.C.CLASS_ROW, width=s.rowWidth or Perc(100))
        mediaStyles = Media(max=self.C.M_MOBILE_MAX, display=s.mobileRowDisplay or self.C.BLOCK, float=self.NONE,
                 minwidth=0, width=self.C.AUTO, paddingleft=0, paddingright=0, margin=0)

        for index in range(s.itemCount):
            # Build all child components of the generic group.
            #print index, s.columns, index % s.columns, index % s.columns == s.columns-1
            colIndex = index % s.columns
            classIndex = '%s%d' % (s.class_ or 'itemGroup', colIndex)
            if index % s.columns == 0:
                clear = self.C.BOTH
            else:
                clear = self.C.NONE
            b.div(class_=(self.C.CLASS_ITEM, classIndex), width=Perc(100/s.columns), 
                float=self.C.LEFT, clear=clear, media=mediaStyles,
            )
            for component in self.components:
                saveItemStart = component.style.itemStart
                component.style.itemStart = index
                component.build(b)
                component.style.itemStart = saveItemStart
            b._div(comment=self.CLASS_ITEM)
        b._div(comment=self.CLASS_ROW)
   
    