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
#   constants.py
#
try:
    from config.xconfig import Config
except ImportError:
    from config.COPYTO_config import Config
    
class C(Config):

    UNTITLED = 'Untitled'
    SINGLE_ATTRIBUTES = [] # Attributes that need no value in the output.
    # Types of sites
    SITETYPE_BLOG = 'blog'

    # Known component names.
    C_TITLE = 'title'

    USE_SCHEDULERVERBOSE = False
    SCHEDULER_SLEEPTIME = 5.0
    SCHEDULER_STATUS_IDLE = 'idle'
    SCHEDULER_STATUS_RUN = 'run'

    # Link window targets
    TARGET_EXTERN = 'extern'
    
    # Menu options
    MENU_VERTICAL = 'vertical'
    MENU_HORIZONTAL = 'horizontal' # Default

    # Media ranges
    M_MOBILE = 767
    M_TABLET = 900
    M_DESKTOP_MIN = M_MOBILE
    M_DESKTOP = 1023
    MAXWIDTH = 1140

    # ID's
    ID_HEADER = 'header'
    ID_LOGO = 'logo'
    ID_NAV = 'nav'
    ID_NAVIGATIONWRAP = 'navigation-wrap'
    ID_MOBILENAVWRAP = 'nav-wrap'
    ID_MENUICON = 'menu-icon'
    ID_HOME = 'home'
    
    # Classes
    CLASS_PAGE = 'page'
    CLASS_ERROR = 'error'
    CLASS_MENU = 'menu'
    CLASS_MENULINK = 'menuLink'
    CLASS_MENULINKS = 'menuLinks'
    CLASS_CONTAINER = 'container'
    CLASS_AUTOWIDTH = 'autoWidth' # Make img tags behave right for width='auto' in all browser.
    CLASS_FIRST = 'first'
    CLASS_LAST = 'last'
    CLASS_ROW = 'row'
    CLASS_CHAPTER = 'chapter'
    CLASS_CHAPTERNAVIGATION = 'chapterNavigation'
    CLASS_MOBILECHAPTERNAVIGATION = 'mobileChapterNavigation'
    CLASS_NAME = 'name'
    CLASS_AUTHOR = 'author'
    CLASS_CATEGORY = 'category'
    CLASS_CATEGORYTHUMB = 'categoryThumb'
    CLASS_SUMMARY = 'summary'
    CLASS_SUMMARYBOX = 'summaryBox'
    CLASS_ARTICLE = 'article'
    CLASS_ARTICLETOP = 'articleTop'
    CLASS_FOOTNOTE = 'footnote'
    CLASS_FOOTNOTES = 'footnotes' # List of footnotes
    CLASS_LEVEL = 'level'
    CLASS_LEAD = 'lead'
    CLASS_FIRST = 'first'
    CLASS_ITEM = 'item'
    CLASS_IMAGEBLOCK = 'imageBlock'
    CLASS_CAPTION = 'caption'
    CLASS_SOCIALMEDIA = 'socialMedia'
    
    CLASS_1COL = 'oneCol'
    CLASS_2COL = 'twoCol'
    CLASS_3COL = 'threeCol'
    CLASS_4COL = 'fourCol'
    CLASS_5COL = 'fiveCol'
    CLASS_6COL = 'sixCol'
    CLASS_7COL = 'sevenCol'
    CLASS_8COL = 'eightCol'
    CLASS_9COL = 'nineCol'
    CLASS_10COL = 'tenCol'
    CLASS_11COL = 'elevenCol'
    CLASS_12COL = 'twelveCol'

    MAXCOL = 12
    COL2CLASS = {
        1: CLASS_1COL, 2: CLASS_2COL, 3: CLASS_3COL, 4: CLASS_4COL, 5: CLASS_5COL, 6: CLASS_6COL,
        7: CLASS_7COL, 8: CLASS_8COL, 9: CLASS_9COL, 10: CLASS_10COL, 11: CLASS_11COL, 12: CLASS_12COL,
    }
    C100 = '100%'
    
    # Params
    PARAM_CSS = 'css'
    PARAM_EDIT = 'edit'
    PARAM_ARTICLE = 'article'
    PARAM_CHAPTER = 'chapter' # Chapter index in the current article, starting with 0
    PARAM_FORCECSS = 'forcecss' # Force the recalculation of the SASS/CSS
    PARAM_AUTHOR = 'author'
    PARAM_ARTICLE = 'article'
    PARAM_CATEGORY = 'category'
    PARAM_SID = 'sid' # Session id
    
    # Tag
    TAG_BLOCK = 'div' # Default tag for blocks

    # Image
    IMG_DEFAULTBORDER = 0

    # CSS Constants
    ITALIC = 'italic'
    VERTICAL = 'vertical' # Menu
    BLOCK = 'block'
    INLINEBLOCK = 'inline-block'
    INLINE = 'inline'
    NONE = 'none'
    BOTH = 'both'
    HIDDEN = 'hidden'
    AUTO = 'auto'
    BOTTOM = 'bottom'
    UNDERLINE = 'underline'
    ABSOLUTE = 'absolute'
    RELATIVE = 'relative'
    UPPERCASE = 'uppercase'
    POINTER = 'pointer'
    BOLD = 'bold'
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    MIDDLE = 'middle'
    NORMAL = 'normal'
    REPEAT = 'repeat'
    BASELINE = 'baseline'
    DECIMAL = 'decimal'
    
    # Pseudo CSS selectors
    FIRSTCHILD = 'first-child'
    
    # Colors
    BLACK = 'black'
    WHITE = 'white'
    
    # Builder postfixes
    # These are tested on  dispatcher method and attribute name postfix against the generic names.
    # Must containt the ATTR_POSTFIX of all available builders.
    ATTR_POSTFIXES = set(('html', 'css'))
    
    # Template names (as parameter in url)
    TEMPLATE_INDEX = 'index'
    TEMPLATE_ARTICLE = 'article'
    TEMPLATE_DOCUMENTATION = 'documentation'
    TEMPLATE_DEFAULT = TEMPLATE_INDEX

    # Adapter
    ADAPTER_PAGETITLE = 'pageTitle'
    ADAPTER_LOGO = 'logo' 
    ADAPTER_MESSAGE = 'message'
    ADAPTER_CHAPTERS = 'chapters'
    ADAPTER_FEATUREDARTICLES = 'featuredArticles'
    ADAPTER_FOOTER = 'footer'
    ADAPTER_SOCIALMEDIA = 'socialMedia'
    ADAPTER_TAGCLOUD = 'tagCloud'
    ADAPTER_ARTICLE = 'article'
    ADAPTER_PAGES = 'pages'
    ADAPTER_MOBILEPAGES = 'mobilePages'
    ADAPTER_MENU = 'menu'
    
    # SASS
    SASS_NESTED = 'nested'
    SASS_EXPANDED = 'expanded'
    SASS_COMPACT = 'compact'
    SASS_COMPRESSED = 'compressed'

    SASS_STYLES = (SASS_NESTED, SASS_EXPANDED, SASS_COMPACT, SASS_COMPRESSED)
    SASS_DEFAULTSTYLE = SASS_COMPRESSED

    # ---------------------------------------------------------------------------------------------------------
    #     S E S S I O N  K E Y S

    SESSION_ID = PARAM_SID
    SESSION_SESSIONEXPIRATIONTIME = 600 # 10 minutes for normal usage of the site
    SESSION_EDITEXPIRATIONTIME = 3600 # 1 hour for editing mode.
    SESSION_SIDDIGITS = 64 # Number of digits chunks for the session id (64 digits default)
    # Don't make too high or else it will not fit in the cookie
    SESSION_LANGUAGE = 'language'
    SESSION_TYPESTAMPRANDOMRANGE = 10000000 # Random range added to a session timestamp

    # ---------------------------------------------------------------------------------------------------------
    #    D A T A B A S E
    #
    #    Standard table and field names
    #
    TABLE_XREF = 'xref'
    TABLE_ADDRESS = 'address'    
    
    FIELD_XSRCTABLE = 'xsrc'
    FIELD_XSRCFIELD = 'xsrc'
    FIELD_XREFSRCID = 'srcId'

    FIELD_XDSTTABLE = 'xdst'
    FIELD_XDSTFIELD = 'dstId'
    FIELD_XREFDSTID = 'dstId'
    
    # ---------------------------------------------------------------------------------------------------------
    #    B R O W S E R  S T U F F

    BROWSER_UNKNOWN = 'browser_unknown'
    BROWSER_SAFARI = 'browser_safari'
    BROWSER_FIREFOX = 'browser_firefox'
    BROWSER_CAMINO = 'browser_camino'
    BROWSER_IE = 'browser_ie'
    BROWSER_OPERA = 'browser_opera'
    BROWSER_NETSCAPE = 'browser_netscape'
    BROWSER_CHROME = 'browser_chrome'
    BROWSER_IPHONE = 'browser_iphone'

    BROWSER_OSMAC = 'browser_os_mac'
    BROWSER_OSWINDOWS = 'browser_os_windows'

    # Prefixes are automatically inserted, if it is used in the attribute dictionary.
    PREFIXES = ('webkit', 'ms', 'moz', 'o')
    PREFIXES_EXTENDES = PREFIXES + ('xv', 'epub', 'apple', 'khtml', 'safari', 'chrome', 'wap')

    FALSEVALUES = ('', 0, '0', 'f', 'F', 'none', 'None', 'NONE', 'false', 'False', 'FALSE', 'n', 'N', 'no', 'No', 'NO',
                   None, False)
    TRUEVALUES = (1, '1', 't', 'T', 'true', 'True', 'TRUE', 'y', 'Y', 'yes', 'Yes', 'YES', True)
    BOOLVALUES = FALSEVALUES + TRUEVALUES

    # ---------------------------------------------------------------------------------------------------------
    #     X S L

    XSL_XMLCONVERSIONS = (int, float, long, tuple, list, dict, bool)

