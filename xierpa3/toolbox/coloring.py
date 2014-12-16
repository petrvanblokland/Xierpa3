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
#     coloring.py
#
import decimal
import colorsys
import re
from xierpa3.toolbox.transformer import TX
from xierpa3.imaging import color

RGBTUPLE = re.compile('rgb\(([\d]+), ?([\d]+), ?([\d]+)\)', re.I)
RGBATUPLE = re.compile('rgb\(([\d]+), ?([\d]+), ?([\d]+)\, ?([\d\.]+) ?\)', re.I)
CMYKTUPLE = re.compile('cmyk\(([\d]+), ?([\d]+), ?([\d]+), ?([\d]+)\)', re.I)
UHEXTUPLE = re.compile('^0x([\0-9a-f]+)$', re.I)
HEXTUPLE = re.compile('^#?([\0-9a-f]+)$', re.I)
BWLEVEL = 380
BWRGBWEIGHT = (1, 1, 1)

BWRGBWEIGHT = (decimal.Decimal('0.7'), decimal.Decimal('1.3'), decimal.Decimal('0.8'))
BWLEVEL = 180

COLOR_NAMES = {
    'aliceblue': '#F0F8FF',
    'antiquewhite': '#FAEBD7',
    'aqua': '#00FFFF',
    'aquamarine': '#7FFFD4',
    'azure': '#F0FFFF',
    'beige': '#F5F5DC',
    'bisque': '#FFE4C4',
    'black': '#000000',
    'blanchedalmond': '#FFEBCD',
    'blue': '#0000FF',
    'blueviolet': '#8A2BE2',
    'brown': '#A52A2A',
    'burlywood': '#DEB887',
    'cadetblue': '#5F9EA0',
    'chartreuse': '#7FFF00',
    'chocolate': '#D2691E',
    'coral': '#FF7F50',
    'cornflowerblue': '#6495ED',
    'cornsilk': '#FFF8DC',
    'crimson': '#DC143C',
    'cyan': '#00FFFF',
    'darkblue': '#00008B',
    'darkcyan': '#008B8B',
    'darkgoldenrod': '#B8860B',
    'darkgray': '#A9A9A9',
    'darkgreen': '#006400',
    'darkkhaki': '#BDB76B',
    'darkmagenta': '#8B008B',
    'darkolivegreen': '#556B2F',
    'darkorange': '#FF8C00',
    'darkorchid': '#9932CC',
    'darkred': '#8B0000',
    'darksalmon': '#E9967A',
    'darkseagreen': '#8FBC8F',
    'darkslateblue': '#483D8B',
    'darkslategray': '#2F4F4F',
    'darkturquoise': '#00CED1',
    'darkviolet': '#9400D3',
    'deeppink': '#FF1493',
    'deepskyblue': '#00BFFF',
    'dimgray': '#696969',
    'dodgerblue': '#1E90FF',
    'firebrick': '#B22222',
    'floralwhite': '#FFFAF0',
    'forestgreen': '#228B22',
    'fuchsia': '#FF00FF',
    'gainsboro': '#DCDCDC',
    'ghostwhite': '#F8F8FF',
    'gold': '#FFD700',
    'goldenrod': '#DAA520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#ADFF2F',
    'honeydew': '#F0FFF0',
    'hotpink': '#FF69B4',
    'indianred ': '#CD5C5C',
    'indigo ': '#4B0082',
    'ivory': '#FFFFF0',
    'khaki': '#F0E68C',
    'lavender': '#E6E6FA',
    'lavenderblush': '#FFF0F5',
    'lawngreen': '#7CFC00',
    'lemonchiffon': '#FFFACD',
    'lightblue': '#ADD8E6',
    'lightcoral': '#F08080',
    'lightcyan': '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgray': '#D3D3D3',
    'lightgreen': '#90EE90',
    'lightpink': '#FFB6C1',
    'lightsalmon': '#FFA07A',
    'lightseagreen': '#20B2AA',
    'lightskyblue': '#87CEFA',
    'lightslategray': '#778899',
    'lightsteelblue': '#B0C4DE',
    'lightyellow': '#FFFFE0',
    'lime': '#00FF00',
    'limegreen': '#32CD32',
    'linen': '#FAF0E6',
    'magenta': '#FF00FF',
    'maroon': '#800000',
    'mediumaquamarine': '#66CDAA',
    'mediumblue': '#0000CD',
    'mediumorchid': '#BA55D3',
    'mediumpurple': '#9370DB',
    'mediumseagreen': '#3CB371',
    'mediumslateblue': '#7B68EE',
    'mediumspringgreen': '#00FA9A',
    'mediumturquoise': '#48D1CC',
    'mediumvioletred': '#C71585',
    'midnightblue': '#191970',
    'mintcream': '#F5FFFA',
    'mistyrose': '#FFE4E1',
    'moccasin': '#FFE4B5',
    'navajowhite': '#FFDEAD',
    'navy': '#000080',
    'oldlace': '#FDF5E6',
    'olive': '#808000',
    'olivedrab': '#6B8E23',
    'orange': '#FFA500',
    'orangered': '#FF4500',
    'orchid': '#DA70D6',
    'palegoldenrod': '#EEE8AA',
    'palegreen': '#98FB98',
    'paleturquoise': '#AFEEEE',
    'palevioletred': '#DB7093',
    'papayawhip': '#FFEFD5',
    'peachpuff': '#FFDAB9',
    'peru': '#CD853F',
    'pink': '#FFC0CB',
    'plum': '#DDA0DD',
    'powderblue': '#B0E0E6',
    'purple': '#800080',
    'red': '#FF0000',
    'rosybrown': '#BC8F8F',
    'royalblue': '#4169E1',
    'saddlebrown': '#8B4513',
    'salmon': '#FA8072',
    'sandybrown': '#F4A460',
    'seagreen': '#2E8B57',
    'seashell': '#FFF5EE',
    'sienna': '#A0522D',
    'silver': '#C0C0C0',
    'skyblue': '#87CEEB',
    'slateblue': '#6A5ACD',
    'slategray': '#708090',
    'snow': '#FFFAFA',
    'springgreen': '#00FF7F',
    'steelblue': '#4682B4',
    'tan': '#D2B48C',
    'teal': '#008080',
    'thistle': '#D8BFD8',
    'tomato': '#FF6347',
    'turquoise': '#40E0D0',
    'violet': '#EE82EE',
    'wheat': '#F5DEB3',
    'white': '#FFFFFF',
    'whitesmoke': '#F5F5F5',
    'yellow': '#FFFF00',
    'yellowgreen': '#9ACD32',
}
class Color:
    u"""
    
    <list>
        <sep>Initialize the color from hex value, rgb or cmyk tuple.<br/>
            Or from string ``rgb(r,g,b)`` or ``cmyk(c,m,y,k)``</sep>
        <sep>Initialize output format as either ``cmyk``, ``rgb``, ``hex`` or ``uhex``</sep>
        <sep>Otherwise raise an error</sep>
    </list>
    <note>There still are, though hardly visible, slight differences through the color conversions, e.g. ``Color('#b20071')`` returns the color ``#b20070``.</note>

    <python>
    Color('#b20071')<br/>
    Color((178,0,112))<br/>
    Color((0, 0.7, 0.26, 0.3))<br/>
    Color('rbg(178,0,112)')<br/>
    Color(('cmyk(0, 0.7, 0.26, 0.3)')<br/>
    Color('#b20071','rgb')<br/>
    Color('#b20071','cmyk')<br/>
    c = Color('#b20071')<br/>
    print c.lighten(30)<br/>
    >>> #fe16a9<br/>
    print c.lighten(30).desaturate(40)<br/>
    >>> #d0439c<br/>
    print c<br/>
    >>> #b20070<br/>
    
    </python>
    
    """
    RGB = 'rgb'
    CMYK = 'cmyk'
    RGBA = 'rgba'

    def __init__(self, col, format="hex", bw=None, bwrgb=None):

        self.alpha = 1
        self.bwlevel = bw or BWLEVEL
        self.bwrgb = bwrgb or BWRGBWEIGHT

        if isinstance(col, (long, float, int)):
            col = hex(col)
        elif isinstance(col, Color):
            col = col.hex
        if format in ('cmyk', 'rgb', 'hex', 'uhex'):
            self.format = format
        else:
            raise ValueError('[Color] Wrong format "%s". Should be in %s' % (format, repr(('cmyk', 'rgb', 'hex', 'uhex'))))
        try:
            if isinstance(col, basestring):
                # Convert unreliable HTML/CSS color name to hex value and process from there.
                col = COLOR_NAMES.get(col, col)

                if ',' in col:
                    self.c = TX.list2IntFloatList(col)
                elif HEXTUPLE.match(col):
                    if len(col) == 4:
                        col = '#%s%s%s' % (col[1]*2, col[2]*2, col[3]*2)
                    self.c = col
                elif UHEXTUPLE.match(col):
                    col = col[2:]
                    if len(col) == 4:
                        col = '#%s%s%s' % (col[1]*2, col[2]*2, col[3]*2)
                    self.c = col
                elif RGBTUPLE.match(col):
                    mrgb = RGBTUPLE.match(col)
                    self.c = (int(mrgb.group(1)), int(mrgb.group(2)), int(mrgb.group(3)))
                elif RGBATUPLE.match(col):
                    mrgb = RGBTUPLE.match(col)
                    self.c = (int(mrgb.group(1)), int(mrgb.group(2)), int(mrgb.group(3)))
                    self.alpha = float(mrgb.group(4))
                elif CMYKTUPLE.match(col):
                    mcmyk = CMYKTUPLE.match(col)
                    self.c = (int(mcmyk.group(1)), int(mcmyk.group(2)), int(mcmyk.group(3)), int(mcmyk.group(4)))
                else:
                    ValueError('[Color] Unknown color format "%s"' % color)
            else:
                self.c = col
                if len(self.c) == 3 and sum(self.c) <= 3:
                    # Test for 0-1 values - RGB values should be 0-255
                    self.c = list(self.c)
                    for i in range(3):
                        if self.c[i] <= 1 and self.c[i] / 2 == float(self.c[i]) / 2:
                            self.c[i] *= 255
                            self.c[i] = int(self.c[i])
                    self.c = tuple(self.c)
        except:
            raise ValueError('[Color] Wrong color format "%s"' % color)

        rgbint = color.rgb(self.c)
        self.r, self.g, self.b = color._int2rgbtuple(rgbint)
        self.h, self.l, self.s = _rgb2hls(self.r, self.g, self.b)

    def __getattr__(self, key):
        method = '_' + key
        if hasattr(self, method):
            return getattr(self, method)()
        return self.__dict__[key]

    def __cmp__(self, color):
        if color is None:
            return False
        return `self.value` == color.value
 
    def __ne__(self, color):
        return self.value == color.value
    
    def __coerce__(self, color):
        return None

    def _r(self):
        return self.r

    def _g(self):
        return self.g

    def _b(self):
        return self.b

    def __str__(self):
        return repr(self)

    def __nonzero__(self):
        return 1

    def __radd__(self, s):
        return s + self.hex

    def __add__(self, s):
        return self.hex + s

    def __getslice__(self, i, j):
        return repr(self)[max(0, i):max(0, j):]
        # return None

    def __repr__(self):
        result = _hls2colorformat(self.h, self.l, self.s, self.format)
        if self.format == 'rgb':
            return 'rgb' + repr(result)
        elif self.format == 'rgba' and self.alpha < 1:
            return 'rgba' + repr(result).rstrip(')') + (', %0.1f)' % float(self.alpha))
        elif self.format == 'cmyk':
            return 'cmyk' + repr(result)
        return result

    def value(self):
        return `self`

    def __sub__(self, color):
        c = Color(color)
        # return self.r,col.r, self.g,col.g, self.b,col.b
        return self.r - c.r + self.g - c.g + self.b - c.b

    def _get(self):
        result = _hls2colorformat(self.h, self.l, self.s, self.format)
        return result

    def _getlist(self):
        result = _hls2colorformat(self.h, self.l, self.s, self.format)
        return list(result)

    def _rgb(self, alpha=None):
        u"""
        
        The ``c.rgb`` returns the color as e.g. rgb(254, 63, 103).
        Or add ``alpha`` as e.g. ``c.rgb(0.5)`` the color is returned as rgba(254, 63, 103, 0.5).
        
        """
        f = self.format
        a = self.alpha
        if alpha is not None:
            self.alpha = alpha
            self.format = 'rgba'
        else:
            self.format = 'rgb'
        c = repr(self)
        self.format = f
        self.alpha = a
        return c

    _rgba = _rgb

    def _cmyk(self):
        u"""
        
        The ``c.cmyk`` returns the color as e.g. rgb(254, 63, 103)
        
        """
        f = self.format
        self.format = 'cmyk'
        c = repr(self)
        self.format = f
        return c

    def _hex(self):
        u"""
        
        The ``c.hex`` returns the color as e.g. #fe3f67
        
        """
        f = self.format
        self.format = 'hex'
        c = repr(self)
        self.format = f
        return c

    def _uhex(self):
        u"""
        
        The ``c.hex`` returns the color as e.g. 0xfe3f67
        
        """
        f = self.format
        self.format = 'uhex'
        c = repr(self)
        self.format = f
        return c

    def _negative(self):
        u"""
        
        The ``c.negativebw`` returns white Color if the color is dark, and  black if color is light.
        
        """
        v = self.r * self.bwrgb[0] + self.g * self.bwrgb[1] + self.b * self.bwrgb[2]
        if v < self.bwlevel:
            return -1
        return 1

    def _negativebw(self):
        u"""
        
        The ``c.negativebw`` returns white Color if the color is dark, and  black if color is light.
        
        """
        # v = self.r*self.bwrgb[0] + self.g*self.bwrgb[1] + self.b*self.bwrgb[2]
        if self.negative < 1:
            c = '#ffffff'
        else:
            c = '#000000'
        return Color(c, self.format)

    def setformat(self, format):
        u"""
        
        The ``c.setformat()`` change the output format - if ``format`` is either
        ``cmyk``,``rgb`` or ``hex``
        
        """
        if format in ('cmyk', 'rgb', 'hex', 'uhex'):
            return Color(_hls2colorformat(self.h, self.l, self.s, self.format), format=format)
        else:
            raise ValueError('''[Color] Cannot set color format. "%s" doesn't exist.''' % format)

    def setrgb(self, red=None, green=None, blue=None):
        u"""
        
        The ``c.setrgb()`` set the red, green and blue channel of the color.
        
        """
        if isinstance(red, (tuple, list)):
            r, g, b = red
        else:
            r = red or self.r
            g = green or self.g
            b = blue or self.b
        h, l, s = _rgb2hls(r, g, b)
        return Color(_hls2colorformat(h, l, s, self.format), format=self.format)

    def saturate(self, v):
        u"""
        
        The ``c.saturate()`` returns a new ``Color`` object, that is saturated with with ``v`` ranging [0:100].
        
        """
        v = int(v)
        if v < 0:
            return self.desaturate(-v)
        s = _valueincrease(self.s, v)
        return Color(_hls2colorformat(self.h, self.l, s, self.format), format=self.format)

    def desaturate(self, v):
        u"""
        
        The ``c.desaturate()`` returns a new ``Color`` object, that is desaturated with with ``v`` ranging [0:100].
        
        """
        v = int(v)
        if v < 0:
            return self.saturate(-v)
        s = _valuedecrease(self.s, v)
        return Color(_hls2colorformat(self.h, self.l, s, self.format), format=self.format)

    def lighten(self, v):
        u"""
        
        The ``c.lighten()``  returns a new ``Color`` object, that is lightened with with ``v`` ranging [0:100].
        
        """
        v = int(v)
        if v < 0:
            return self.darken(-v)
        l = _valueincrease(self.l, v)
        return Color(_hls2colorformat(self.h, l, self.s, self.format), format=self.format)

    def darken(self, v):
        u"""
        
        The ``c.darken()``  returns a new ``Color`` object, that is darkened with with ``v`` ranging [0:100].
        
        """
        v = int(v)
        if v < 0:
            return self.lighten(-v)
        l = _valuedecrease(self.l, v)
        return Color(_hls2colorformat(self.h, l, self.s, self.format), format=self.format)

    def change(self, lightness=0, saturation=0, hue=0):
        u"""
        
        The ``c.change()`` returns a new ``Color`` object, that is changed with<br/>
        ``lightness`` ranging [-100:100] (default is ``0``),<br/>
        ``saturation`` ranging [-100:100] (default is ``0``),<br/>
        ``hue`` ranging [0:254] (default is ``0``),
        
        """
        l = _valuechange(self.l, lightness)
        s = _valuechange(self.s, saturation)
        hue = int(hue or 0) / 255.0
        h = self.h + hue
        while h < 0:
            h += 1.0
        while h > 1:
            h -= 1.0
        return Color(_hls2colorformat(h, l, s, self.format), format=self.format)

    def mix(self, mix='BGR'):
        u"""
        
        The ``c.mix()`` returns a new ``Color`` object with mixed RGB channels.<br/>
        ``mix``
        
        """
        baseseq = 'rgb'
        mix = mix.lower()
        if not 'r' in mix or 'b' not in mix or 'g' not in mix or len(mix) != 3:
            raise ValueError('''[Color] Cannot mix color rgb channels as "%s".''' % mix)
        mixcolor = []
        color = _hls2rgbtuple((self.h, self.l, self.s))
        for m in mix:
            i = baseseq.index(m)
            mixcolor.append(color[i])
        return Color(_returncolorformat(tuple(mixcolor), self.format), format=self.format)

    def oppositehue(self):
        u"""
        
        The ``c.oppositehue()`` returns a new ``Color`` object with the opposite color on the hue circle, 
        while the lightness and saturation is unchanged.
        
        """
        return Color(_hls2colorformat(1 - self.h, self.l, self.s, self.format), format=self.format)

    def opposite(self):
        u"""
        
        The ``c.opposite()`` returns a new ``Color`` object with opposite r,g and b channels.<br/>
        E.g. if the red channel of the color is 203, it will be changed to 51
        
        """
        r, g, b = _hls2rgbtuple((self.h, self.l, self.s))
        rgb = (254 - r, 254 - g, 254 - b)
        return Color(_returncolorformat(rgb, self.format), format=self.format)

# # S u b r o u t i n e s

def _hls2colorformat(h, l, s, format):
    c = _hls2rgbtuple((h, l, s))
    return _returncolorformat(c, format)

def _hls2rgbtuple(hls):
    r, g, b = _hls2rgb(hls)
    return int(r * 255), int(g * 255), int(b * 255)

def _rgb2hls(r, g, b):
    return colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

def _hls2rgb(hls):
    # cannot use convertcolor - it checks on tuple length
    h, l, s = hls
    return colorsys.hls_to_rgb(h, l, s)

def _returncolorformat(c, format):
    if format is not None:
        if format == 'hex':
            return _col2hex(c)
        if format == 'uhex':
            return _col2hex(c, '0x')
        if format == 'cmyk':
            c, m, y, k = color._rgb2cmyk(c)
            return c, m, y, k
        return c
    return c

def _col2hex(c, hx='#'):
    if not isinstance(c, (tuple, list)):
        return c
    # hx = '#'
    for i in c:
        h = hex(int(i))[2:]
        if len(h) == 1:
            h = '0' + h
        hx += h
    return hx.upper()

def _valueincrease(c, v):
    c += (1 - c) * v / 100.0
    return c

def _valuedecrease(c, v):
    c -= c * v / 100.0
    return c

def _valuechange(c, v):
    if v:
        v = int(v)
        if v < 0:
            return _valuedecrease(c, -v)
        else:
            return _valueincrease(c, v)
    else:
        return c

# # T e s t s

if __name__ == "__main__":
    col = Color((178, 0, 112), 'rgb')
    print 'rgb-tuple of (178,0,112)', col
    col = Color(col.rgb, 'rgb')
    print 'rgb-tuple of (178,0,112)', col
    print 'rgb-tuple', col.lighten(50)
    col = Color('rgb(178,0,112)')
    print 'rgb-tuple as string', col.lighten(50)
    col = Color((0, 0.7, 0.26, 0.3), 'cmyk')
    print 'cmyk-tuple', col.lighten(50)
    col = Color('0, 0.7, 0.26, 0.3')
    print col.lighten(50)
    col = Color('178,0,112')
    print col.lighten(50)
    print col.darken(30)
    col = Color('#b20071')
    print col.lighten(50)
    print col.darken(30)
    col = Color('#b20071', 'rgb')
    print repr(col)
    col = Color('#b20071')
    col.setformat('rgb')
    print 'format changed to rgb', str(col)
    col.setformat('hex')
    print 'format changed to hex', str(col)
    col.setformat('cmyk')
    print 'format changed to cmyk', str(col)
    col = Color('#804068')
    print str(col)
    print col.change(30, 20, 255)
    print col.change(30, 20, -255)
    print col.change(30, 20)
    print col.change(hue= -30)
    # c35b9c
    col.setrgb(254)
    # -> #fe3f67 @@@ Note: Photoshop would say it should be #fe3f66
    print repr(col), str(col), col
    # col = Color('#804068','ds')
    print col.rgb
    print col.cmyk
    print col.hex
    print col.uhex
    col = Color('#804068', 'uhex')
    print col
    col = Color('#804068')
    print 'opposite of #804068:', col.opposite()
    print 'oppositehue of #804068:', col.oppositehue()
    col = Color((178, 0, 112), 'rgb')
    print 'mix of (178,0,112):', col.mix()
    col = Color('#b20071')
    print col.lighten(30)
    print col.lighten(30).desaturate(40)
    # print col.mix('bgre')
    # >>> ValueError: [Color] Cannot mix color rgb channels as "bgre".
    print 'cccc', Color('#ffdd00') - '#ffcc00'
    print Color('#dddddd').negativebw
    print Color('#aaaaaa').negativebw
    print Color('#888888').negativebw
    print Color('#cc66cc').negativebw
