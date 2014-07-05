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
#   Formatting conform https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml
#
try:
    from config.xconfig import Config
except ImportError:
    from config.COPYTO_config import Config
    
class Constants(Config):
    u"""Inherited by main Xierpa3 classes, to share default constants, 
    will allowing to be redefined by inheriting classes."""
    
    # Indenting output
    TAB_INDENT = ' '*2
    
    UNTITLED = 'Untitled'
    SINGLE_ATTRIBUTES = [] # Attributes that need no value in the output.
    # Types of sites
    SITETYPE_BLOG = 'blog'

    # Webtype @fontface fonts, to be used for localhost demo purposes.
    # Note that this package contains the a set of latest featured font, and may be changed in the future.
    # If using the font in this package, safest is to refer to the functional constant names below,
    # instead of making a direct reference to the family name.
    # Of course, taking your own account at //www.webtype.com is even better :)
    XIERPA3_DEMOFONTS = '//cloud.webtype.com/css/34d3e5fe-7dee-4122-9e87-ea5ee4a90a05.css'
    # Redefine this list for other font packages in inheriting theme classes.
    URL_FONTS = [] #XIERPA3_DEMOFONTS,)    
    BODYFAMILY = 'Georgia'
    HEADFAMILY = 'Verdana'
    LOGOFAMILY = HEADFAMILY
    
    # Sponsored fonts in the example sites
    URL_WEBTYPELOGO = '//data.xierpa.com.s3.amazonaws.com/xierpa3/_images/documentation/webtypelogo.png'
    
    # Xierpa ico, answered by the default adapter.getIco()
    URL_FAVICON = '//data.xierpadoc.com.s3.amazonaws.com/_images/xierpa_x.ico'
    URL_LOGO = '//data.xierpa.com.s3.amazonaws.com/_images/xierpa_x_green.png'
    # Placeholder for all images if not online.
    URL_XIERPA3RESOURCES = '/xierpa3/resources/'
    URL_IMAGEPLACEHOLDER = URL_XIERPA3RESOURCES + 'images/placeholder.png'
    
    # CSS
    URL_CSS = ['css/style.css']
    
    # Know builder id's, used to check on a specific builder of really necessary.
    # Note that these value should match with the id's of the builder classes.
    TYPE_HTML = 'html'
    TYPE_SASS = 'sass'
    TYPE_CSS = 'css'
    TYPE_PHP = 'php'
    
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

    # Media ranges and widths
    M_MOBILE_MAX = 755
    M_TABLET_MIN = M_MOBILE_MAX+1
    M_DESKTOP_MIN = 1024
    M_TABLET_MAX = M_DESKTOP_MIN-1
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
    CLASS_ARTICLE = 'article'
    CLASS_ARTICLETOP = 'articleTop'
    CLASS_AUTHOR = 'author'
    CLASS_AUTOWIDTH = 'autoWidth' # Make img tags behave right for width='auto' in all browser.
    CLASS_CAPTION = 'caption'
    CLASS_CATEGORY = 'category'
    CLASS_CATEGORYTHUMB = 'categoryThumb'
    CLASS_COLUMN = 'column'
    CLASS_CHAPTER = 'chapter'
    CLASS_CHAPTERNAVIGATION = 'chapterNavigation'
    CLASS_CONTAINER = 'container'
    CLASS_ERROR = 'error'
    CLASS_FIRST = 'first'
    CLASS_FIRST = 'first'
    CLASS_FOOTNOTE = 'footnote'
    CLASS_FOOTNOTES = 'footnotes' # List of footnotes
    CLASS_IMAGEBLOCK = 'imageBlock'
    CLASS_ITEM = 'item'
    CLASS_LAST = 'last'
    CLASS_LEAD = 'lead'
    CLASS_LEVEL = 'level'
    CLASS_MENU = 'menu'
    CLASS_MENULINK = 'menuLink'
    CLASS_MENULINKS = 'menuLinks'
    CLASS_MOBILECHAPTERNAVIGATION = 'mobileChapterNavigation'
    CLASS_NAME = 'name'
    CLASS_PAGE = 'page'
    CLASS_PULLQUOTE = 'pullquote'
    CLASS_ROW = 'row'
    CLASS_SOCIALMEDIA = 'socialMedia'
    CLASS_SUMMARY = 'summary'
    CLASS_SUMMARYBOX = 'summaryBox'
    
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
    
    # Params
    PARAM_CSS = 'css'
    PARAM_EDIT = 'edit'
    PARAM_ARTICLE = 'article'
    PARAM_CHAPTER = 'chapter' # Chapter index in the current article, starting with 0
    PARAM_AUTHOR = 'author'
    PARAM_ARTICLE = 'article'
    PARAM_CATEGORY = 'category'
    PARAM_SID = 'sid' # Session id
    PARAM_DOCUMENTATION = 'documentation'
    PARAM_FORCE = 'force' # Force the recalculation of the SASS/CSS
    PARAM_AJAX = 'ajax'
    
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
    LIST = 'list'
    
    # Pseudo CSS selectors
    FIRSTCHILD = 'first-child'
    
    # Colors
    BLACK = 'black'
    WHITE = 'white'
    
    # Builder postfixes
    # These are tested on  dispatcher method and attribute name postfix against the generic names.
    # Must containt the ATTR_POSTFIX of all available builders.
    ATTR_POSTFIXES = set(('html', 'css'))
    
    ATTR_MEDIA = 'media' # Special attribute in components to define (a list of) Media instances.
    # Template names (as parameter in url)
    TEMPLATE_INDEX = 'index'
    TEMPLATE_ARTICLE = 'article'
    TEMPLATE_DOCUMENTATION = 'documentation'
    TEMPLATE_DEFAULT = TEMPLATE_INDEX

    # Adapter
    '''
    ADAPTER_PAGETITLE = 'pageTitle'
    ADAPTER_LOGO = 'logo' 
    ADAPTER_MESSAGE = 'message'
    ADAPTER_CHAPTERS = 'chapters'
    ADAPTER_FEATUREDARTICLES = 'featuredArticles'
    ADAPTER_FOOTER = 'footer'
    ADAPTER_SOCIALMEDIA = 'socialMedia'
    ADAPTER_TAGCLOUD = 'tagCloud'
    ADAPTER_ARTICLE = 'article'
    ADAPTER_ARTICLES = 'articles'
    ADAPTER_PAGES = 'pages'
    ADAPTER_MOBILEPAGES = 'mobilePages'
    ADAPTER_MENU = 'menu'
    '''
    # Types of article selector
    SELECTOR_FEATURED = 'featured'
    
    # SASS
    SASS_NESTED = 'nested'
    SASS_EXPANDED = 'expanded'
    SASS_COMPACT = 'compact'
    SASS_COMPRESSED = 'compressed'

    SASS_STYLES = (SASS_NESTED, SASS_EXPANDED, SASS_COMPACT, SASS_COMPRESSED)
    SASS_DEFAULTSTYLE = SASS_COMPRESSED

    META_DESCRIPTION = 'description'
    META_KEYWORDS = 'keywords'
    
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

    # ---------------------------------------------------------------------------------------------------------
    #    E X T E N S I O N S

    # Text / code formats.
    EXTENSION_XML = 'xml'
    EXTENSION_XSL = 'xsl'
    EXTENSION_XSD = 'xsd'
    EXTENSION_TXT = 'txt'
    EXTENSION_CSS = 'css'
    EXTENSION_HTML = 'html'
    EXTENSION_JSON = 'json'
    EXTENSION_PY = 'py'
    EXTENSION_JS = 'js'
    EXTENSION_EPUB = 'epub'

    # Lossy web image formats.
    EXTENSION_JPG = 'jpg'
    EXTENSION_JPEG = 'jpeg'
    EXTENSION_PNG = 'png'
    EXTENSION_GIF = 'gif'

    # Common web document formats.
    EXTENSION_PDF = 'pdf'
    EXTENSION_EPS = 'eps'
    EXTENSION_ZIP = 'zip'
    EXTENSION_RAR = 'rar'
    EXTENSION_TAR = 'tar'
    EXTENSION_GZ = 'gz'
    EXTENSION_UFO = 'ufo'
    EXTENSION_TTF = 'ttf'
    EXTENSION_OTF = 'otf'

    # Lossless print formats.
    EXTENSION_TIF = 'tif'
    EXTENSION_TIFF = 'tiff'

    # Filetype sets.
    EXTENSIONS_XML = (EXTENSION_XML, EXTENSION_XSL, EXTENSION_XSD)
    EXTENSIONS_TEXT = (EXTENSION_XML, EXTENSION_XSL, EXTENSION_XSD, EXTENSION_TXT, EXTENSION_PY, EXTENSION_JS, EXTENSION_JSON)
    EXTENSIONS_WEBIMAGES = (EXTENSION_JPG, EXTENSION_JPEG, EXTENSION_PNG, EXTENSION_GIF)
    EXTENSIONS_DOCUMENTS = (EXTENSION_PDF, EXTENSION_EPS, EXTENSION_ZIP, EXTENSION_RAR, EXTENSION_TAR, EXTENSION_GZ)
    EXTENSIONS_TIFF = (EXTENSION_TIFF, EXTENSION_TIF)

    # Valid files for uploading.
    EXTENSIONS_VALIDFILES = EXTENSIONS_WEBIMAGES + EXTENSIONS_DOCUMENTS + EXTENSIONS_TIFF

    DEFAULT_EXTENSION = '' # Must be empty, or else plain url's won't work.
    IMAGE_FORMAT = EXTENSION_PNG # Default image format by ImageBuilder

    # ---------------------------------------------------------------------------------------------------------
    #    M I M E  T Y P E S

    MIMETYPES = {
        'otf': 'font/ttf', # Not standard
        'ttf': 'font/ttf', # Not standard
        'wff': 'font/woff', # Future?
        'woff': 'application/x-font-woff', # IE9 requires this

        '323': 'text/h323',
        'acx': 'application/internet-property-stream',
        'ai': 'application/postscript',
        'aif': 'audio/x-aiff',
        'aifc': 'audio/x-aiff',
        'aiff': 'audio/x-aiff',
        'asf': 'video/x-ms-asf',
        'asr': 'video/x-ms-asf',
        'asx': 'video/x-ms-asf',
        'au': 'audio/basic',
        'avi': 'video/x-msvideo',
        'axs': 'application/olescript',
        'bas': 'text/plain',
        'bcpio': 'application/x-bcpio',
        'bin': 'application/octet-stream',
        'bmp': 'image/bmp',
        'c': 'text/plain',
        'cat': 'application/vnd.ms-pkiseccat',
        'cdf': 'application/x-cdf',
        'cer': 'application/x-x509-ca-cert',
        'class': 'application/octet-stream',
        'clp': 'application/x-msclip',
        'cmx': 'image/x-cmx',
        'cod': 'image/cis-cod',
        'cpio': 'application/x-cpio',
        'crd': 'application/x-mscardfile',
        'crl': 'application/pkix-crl',
        'crt': 'application/x-x509-ca-cert',
        'csh': 'application/x-csh',
        'css': 'text/css',
        'dcr': 'application/x-director',
        'der': 'application/x-x509-ca-cert',
        'dir': 'application/x-director',
        'dll': 'application/x-msdownload',
        'dms': 'application/octet-stream',
        'doc': 'application/msword',
        'dot': 'application/msword',
        'dvi': 'application/x-dvi',
        'dxr': 'application/x-director',
        'eot': 'application/vnd.ms-fontobject',
        'eps': 'application/postscript',
        'epub': 'application/epub+zip',
        'etx': 'text/x-setext',
        'evy': 'application/envoy',
        'exe': 'application/octet-stream',
        'fif': 'application/fractals',
        'flr': 'x-world/x-vrml',
        'gif': 'image/gif',
        'gtar': 'application/x-gtar',
        'gz': 'application/x-gzip',
        'h': 'text/plain',
        'hdf': 'application/x-hdf',
        'hlp': 'application/winhlp',
        'hqx': 'application/mac-binhex40',
        'hta': 'application/hta',
        'htc': 'text/x-component',
        'htm': 'text/html',
        'html': 'text/html',
        'htt': 'text/webviewhtml',
        'ico': 'image/x-icon',
        'ief': 'image/ief',
        'iii': 'application/x-iphone',
        'ins': 'application/x-internet-signup',
        'isp': 'application/x-internet-signup',
        'jfif': 'image/pipeg',
        'jpe': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'json': 'application/json',
        'jpg': 'image/jpeg',
        'js': 'application/x-javascript',
        'latex': 'application/x-latex',
        'lha': 'application/octet-stream',
        'lsf': 'video/x-la-asf',
        'lsx': 'video/x-la-asf',
        'lzh': 'application/octet-stream',
        'm13': 'application/x-msmediaview',
        'm14': 'application/x-msmediaview',
        'm3u': 'audio/x-mpegurl',
        'man': 'application/x-troff-man',
        'mdb': 'application/x-msaccess',
        'me': 'application/x-troff-me',
        'mht': 'message/rfc822',
        'mhtml': 'message/rfc822',
        'mid': 'audio/mid',
        'mny': 'application/x-msmoney',
        'mov': 'video/quicktime',
        'movie': 'video/x-sgi-movie',
        'mp2': 'video/mpeg',
        'mp3': 'audio/mpeg',
        'mpa': 'video/mpeg',
        'mpe': 'video/mpeg',
        'mpeg': 'video/mpeg',
        'mpg': 'video/mpeg',
        'mpp': 'application/vnd.ms-project',
        'mpv2': 'video/mpeg',
        'ms': 'application/x-troff-ms',
        'mvb': 'application/x-msmediaview',
        'nws': 'message/rfc822',
        'oda': 'application/oda',
        'p10': 'application/pkcs10',
        'p12': 'application/x-pkcs12',
        'p7b': 'application/x-pkcs7-certificates',
        'p7c': 'application/x-pkcs7-mime',
        'p7m': 'application/x-pkcs7-mime',
        'p7r': 'application/x-pkcs7-certreqresp',
        'p7s': 'application/x-pkcs7-signature',
        'pbm': 'image/x-portable-bitmap',
        'pdf': 'application/pdf',
        'pfx': 'application/x-pkcs12',
        'pgm': 'image/x-portable-graymap',
        'pko': 'application/ynd.ms-pkipko',
        'pma': 'application/x-perfmon',
        'pmc': 'application/x-perfmon',
        'pml': 'application/x-perfmon',
        'pmr': 'application/x-perfmon',
        'pmw': 'application/x-perfmon',
        'png': 'image/png',
        'pnm': 'image/x-portable-anymap',
        'pot,': 'application/vnd.ms-powerpoint',
        'ppm': 'image/x-portable-pixmap',
        'pps': 'application/vnd.ms-powerpoint',
        'ppt': 'application/vnd.ms-powerpoint',
        'prf': 'application/pics-rules',
        'ps': 'application/postscript',
        'py': 'text/plain',
        'pyc': 'application/python',
        'pub': 'application/x-mspublisher',
        'qt': 'video/quicktime',
        'ra': 'audio/x-pn-realaudio',
        'ram': 'audio/x-pn-realaudio',
        'ras': 'image/x-cmu-raster',
        'rgb': 'image/x-rgb',
        'rmi': 'audio/mid',
        'roff': 'application/x-troff',
        'rtf': 'application/rtf',
        'rtx': 'text/richtext',
        'scd': 'application/x-msschedule',
        'sct': 'text/scriptlet',
        'setpay': 'application/set-payment-initiation',
        'setreg': 'application/set-registration-initiation',
        'sh': 'application/x-sh',
        'shar': 'application/x-shar',
        'sit': 'application/x-stuffit',
        'snd': 'audio/basic',
        'spc': 'application/x-pkcs7-certificates',
        'spl': 'application/futuresplash',
        'src': 'application/x-wais-source',
        'sql': 'text/plain',
        'sst': 'application/vnd.ms-pkicertstore',
        'stl': 'application/vnd.ms-pkistl',
        'stm': 'text/html',
        'svg': 'image/svg+xml',
        'sv4cpio': 'application/x-sv4cpio',
        'sv4crc': 'application/x-sv4crc',
        'swf': 'application/x-shockwave-flash',
        't': 'application/x-troff',
        'tar': 'application/x-tar',
        'tcl': 'application/x-tcl',
        'tex': 'application/x-tex',
        'texi': 'application/x-texinfo',
        'texinfo': 'application/x-texinfo',
        'tgz': 'application/x-compressed',
        'tif': 'image/tiff',
        'tiff': 'image/tiff',
        'tr': 'application/x-troff',
        'trm': 'application/x-msterminal',
        'tsv': 'text/tab-separated-values',
        'txt': 'text/plain',
        'uls': 'text/iuls',
        'ustar': 'application/x-ustar',
        'vcf': 'text/x-vcard',
        'vrml': 'x-world/x-vrml',
        'wav': 'audio/x-wav',
        'wcm': 'application/vnd.ms-works',
        'wdb': 'application/vnd.ms-works',
        'wks': 'application/vnd.ms-works',
        'wmf': 'application/x-msmetafile',
        'wps': 'application/vnd.ms-works',
        'wri': 'application/x-mswrite',
        'wrl': 'x-world/x-vrml',
        'wrz': 'x-world/x-vrml',
        'xaf': 'x-world/x-vrml',
        'xbm': 'image/x-xbitmap',
        'xla': 'application/vnd.ms-excel',
        'xlc': 'application/vnd.ms-excel',
        'xlm': 'application/vnd.ms-excel',
        'xls': 'application/vnd.ms-excel',
        'xlt': 'application/vnd.ms-excel',
        'xlw': 'application/vnd.ms-excel',
        'xml': 'text/plain', # XML
        'xsl': 'text/plain', # XSL
        'xsd': 'text/plain', # XML Schema
        'xof': 'x-world/x-vrml',
        'xpm': 'image/x-xpixmap',
        'xwd': 'image/x-xwindowdump',
        'z': 'application/x-compress',
        'zip': 'application/zip',
    }
    MIMETYPE_FONTTTF = 'font/ttf'
    MIMETYPE_CSS = MIMETYPES[EXTENSION_CSS]
    MIMETYPE_PLAIN = MIMETYPES[EXTENSION_TXT]
    MIMETYPE_HTML = MIMETYPES[EXTENSION_HTML]
    MIMETYPE_JSON = MIMETYPES[EXTENSION_JSON]
    MIMETYPE_JS = MIMETYPES[EXTENSION_JS]
    MIMETYPE_PY = MIMETYPES[EXTENSION_PY]
    MIMETYPE_XML = MIMETYPES[EXTENSION_XML]
    MIMETYPE_XSL = MIMETYPES[EXTENSION_XSL]
    MIMETYPE_XSD = MIMETYPES[EXTENSION_XSD]
    MIMETYPE_EPUB = MIMETYPES[EXTENSION_EPUB]
    MIMETYPE_PNG = MIMETYPES[EXTENSION_PNG]
    MIMETYPE_JPG = MIMETYPES[EXTENSION_JPG]
    MIMETYPE_GIF = MIMETYPES[EXTENSION_GIF]
    DEFAULT_MIMETYPE = MIMETYPE_PLAIN
