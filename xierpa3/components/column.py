# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#    column.py
#
from xierpa3.components.container import Container
from xierpa3.attributes import Em
from xierpa3.descriptors.media import Media
from xierpa3.descriptors.blueprint import BluePrint

class Column(Container):

    CC = Container
    
    BLUEPRINT = BluePrint( 
        classColumn=CC.CLASS_COLUMN, doc_classColumn=u'Class name of the column.',
        # Layout stuff
        colWidth=4, doc_colWidth=u'Default amount of columns for this component.', 
        columnWidthMobile=CC.AUTO, doc_columnWidthMobile=u'Column width for mobile.',
        # Column stuff
        columnMarginLeft=None, doc_columnMarginLeft=u'Column margin left.',
        columnMarginLeftMobile=0, doc_columnMarginLeftMobile=u'Column margin left for mobile.',
        columnMarginRight=Em(1), doc_columnMarginRight=u'Column margin right.',
        columnMarginRightMobile=0, doc_columnMarginRightMobile=u'Column margin right for mobile.',
        columnMarginTop=Em(1), doc_columnMarginTop=u'Column margin top.',
        columnPaddingRight=0, doc_columnPaddingRight=u'Column padding right.',
        columnPaddingRightMobile=Em(1), doc_columnPaddingRightMobile=u'Column padding right for mobile.',
        columnPaddingLeft=0, doc_columnPaddingLeft=u'Column padding left.',
        columnPaddingLeftMobile=Em(0.5), doc_columnPaddingLeftMobile=u'Column padding left for mobile.',
        columnFloat=CC.LEFT, doc_columnFloat=u'Column float.', 
        columnFloatMobile=CC.NONE, doc_columnFloatMobile=u'Column float for mobile.', 
        columnDisplay=CC.BLOCK, doc_columnDisplay=u'Column display.',
        columnDisplayMobile=None, doc_columnDisplayMobile=u'Column display for mobile.',
        columnMinHeight=0, doc_columnMinHeight=u'Column minimal height.', 
    )
    def buildBlock(self, b):
        u"""Build the block of a column. Note that for clarity fontsize and lineheight are defined
        for each part separated, relation the overall container fontsize and lineheight.
        Classes inheriting from <b>Column</b> should implement <b>self.buildBlock</b>."""
        s = self.style
        colClass = self.getColClass(s.colWidth)
        b.block(self)
        b.div(class_=colClass, marginright=s.columnMarginRight, width=s.colWidth, 
            marginleft=s.columnMarginLeft, margintop=s.columnMarginTop,
            paddingleft=s.columnPaddingLeft, float=s.columnFloat, 
            display=s.columnDisplay,   
            media=(
            	Media(width=s.columnWidthMobile,
				display=s.columnDisplayMobile, 
                float=s.columnFloatMobile, 
                marginleft=s.columnMarginLeftMobile, 
                marginright=s.columnMarginRightMobile, 
                paddingleft=s.columnPaddingLeftMobile, 
                paddingright=s.columnPaddingRightMobile,),
        ))
        self.buildColumn(b)
        b._div(comment=colClass)
        b._block(self) 
        
    def buildColumn(self, b):
        b.error('Classes inheriting from <b>Column</b> should implement <b>self.buildColumn(b)</b>.')
        
