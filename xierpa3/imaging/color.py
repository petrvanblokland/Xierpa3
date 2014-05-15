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
#    color.py
#
#    Define of base class for graphics node (gnode) behavior. A tree of gnodes
#    is the result of rendering a si: by the typesetter.
#
#    @@@ To be done: Debug pantone colors
#
#
#    Format of the color attributes:
#         color="0.4"                    Used as gray
#         color="[0.2, 0.4, 0, 0]        Used as CMYK set    0 <= cmyk <= 1
#         color="0x33ff55"            RGB                    0x000000 <= rgb <= 0xffffff
#         color="#44aa22                RGB                    #000000 <= rgb <= #ffffff
#         color="red"                    RGB                    All html colors
#         color="#red"                RGB                    All html colors
#         color="p1345"                RGB                    All pantone colors
#         color="[33, 144, 244]"        RGB                    [0, 0, 0] <= rgb <= [255, 255, 255]
#         color="[0x11, 0, 0xff]"        RGB                    [0, 0, 0] <= rgb <= [0xff, 0xff, 0xff]
#

# from xpyth.tables.colors import colorname2rgb    # Name table with HTML colors
# from xpyth.tables.colors import pantone2cmyk    # Name table with pantone names

MAXCOLOR = 256L * 256 * 256
ISRGBFLAG = 'rgb'                # Flags are used to check on color type in order to avoid double conversion
ISCMYKFLAG = 'cmyk'
ERRORCOLOR = 0xff0000          # red as error code in color conversions or "None", causing an exception

def colorname2rgb(color):
    # TODO: Make this one?
    return color

def pantone2cmyk():
    # TOD: Make this one?
    pass

def convertcolor(value, astuple=None):
    """    Convert a color

        >>> convertcolor(12345)
        (12345, 'rgb')
        >>> convertcolor((50, 50, 50))
        (3289650L, 'rgb')
        >>> convertcolor('orange')
        (16753920, 'rgb')
        >>> convertcolor('black')
        (0, 'rgb')
        >>> convertcolor((0.5, 0.5, 0.5, 0))
        ((0.5, 0.5, 0.5, 0), 'cmyk')
        >>> convertcolor('P123')
        ([0, 0.23999999999999999, 0.93999999999999995, 0], 'cmyk')
        >>> convertcolor('P300')
        ([1, 0.44, 0, 0], 'cmyk')
    """

    if value is None:
        raise ValueError, ('Color value is None')

    if isinstance(value, basestring):
        if not value:
            return 0, ISRGBFLAG        # Black as default for empty string

        if value[0] == '#':
            value = value[1:]    # Remove html '#' symbol

            # Test for color="#red" - no need for this test ... ?
            # try:
            #    return colorname2rgb[value], ISRGBFLAG
            # except KeyError:
            #    pass

        # Test for color="334455"
        try:
            v = eval('0x' + value) # Evaluate the hex string
            if astuple:
                return _int2rgbtuple(v), ISRGBFLAG
            return int(v), ISRGBFLAG
        except:
            pass

        # Test for color="0x333333"
        try:
            v = eval(value)
            if astuple:
                return _int2rgbtuple(v), ISRGBFLAG
            return int(v), ISRGBFLAG
        except (ValueError, SyntaxError, NameError):
            pass

        # Test for color="red"
        try:
            v = colorname2rgb(value)
            if astuple:
                return _int2rgbtuple(v), ISRGBFLAG
            return int(v), ISRGBFLAG
        except KeyError:
            pass

        # Test for color="p1345"
        if value and value[0] in 'pP':
            try:
                return pantone2cmyk[value[1:].lower()], ISCMYKFLAG
            except KeyError:
                raise ValueError, ('Pantone color does not exist: "%s"' % value)

        raise ValueError, ('Unknown color format: "%s"' % value)

    elif isinstance(value, (float, int, long)):
        if 0 <= value and value <= MAXCOLOR:
            if astuple:
                return _int2rgbtuple(v), ISRGBFLAG
            return value, ISRGBFLAG

    elif isinstance(value, (tuple, list)) and len(value) == 3:
        if astuple:
            return value, ISRGBFLAG
        v = _rgbtuple2int(value)
        if v > MAXCOLOR:
            raise ValueError, ('Color value too high: "%s"' % v)
        return v, ISRGBFLAG

    elif isinstance(value, (list, tuple)) and len(value) == 4:
        if astuple:
            return value, ISCMYKFLAG
        for v in value:
            if not (0 <= v <= 1):            # Test on v, not value
                return None    , 'bad cmyk'    # Need an extra parameter to be unpacked
        return value, ISCMYKFLAG

    raise ValueError, ('Color could not be converted. Unknown format "%s"' % value)

def convert2colortuple(value):
    return convertcolor(value, 1)[0]

def bw(value):
    """    Convert any valid color format black and white rgb tuple
    
        >>> bw((0, 4, 210))
        (71.333333333333329, 71.333333333333329, 71.333333333333329)
        >>> bw([0, 4, 210])
        (71.333333333333329, 71.333333333333329, 71.333333333333329)
    """
    r, g, b = _int2rgbtuple(rgb(value))
    g = (r + g + b) / 3.0
    return g, g, g

def rgb(value):
    """    Convert any valid color format to rbg integer
    
        >>> rgb((0, 4, 210))
        1234L
        >>> rgb([0, 4, 210])
        1234L
        >>> rgb([0.1, 0.1, 0.2, 0.2])
        11776921L
        >>> rgb('#335566')
        3364198
        >>> rgb('P300')
        36863L
        >>> rgb('blue')
        255
    """
    cvalue, type = convertcolor(value)
    if cvalue is None:
        raise ValueError, ('Unknown color type: "%s"' % value)
    if type == ISRGBFLAG:
        return cvalue
    elif type == ISCMYKFLAG:
        return _rgbtuple2int(_cmyk2rgb(cvalue))

def hexrgb(value):
    """    Convert any valid color format to rbg integer
    
        >>> hexrgb((0, 4, 210))
        '0004d2'
        >>> hexrgb([0, 4, 210])
        '0004d2'
        >>> hexrgb([0.1, 0.1, 0.2, 0.2])
        'b3b399'
        >>> hexrgb('#335566')
        '335566'
        >>> hexrgb('P300')
        '008fff'
        >>> hexrgb('blue')
        '0000ff'
    """
    return '%06x' % rgb(value)

def cmyk(value):
    """    Convert any valid color format to cmyk tuple
    
        >>> cmyk((0, 4, 210))
        (0.82352941176470584, 0.80784313725490198, 0, 0.17647058823529416)
        >>> cmyk([0, 4, 210])
        (0.82352941176470584, 0.80784313725490198, 0, 0.17647058823529416)
        >>> cmyk([0.1, 0.1, 0.2, 0.2])
        [0.10000000000000001, 0.10000000000000001, 0.20000000000000001, 0.20000000000000001]
        >>> cmyk('#335566')
        (0.20000000000000007, 0.066666666666666763, 0, 0.59999999999999998)
        >>> cmyk('P300')
        [1, 0.44, 0, 0]
        >>> cmyk('blue')
        (1, 1, 0, 0)
    """
    cvalue, type = convertcolor(value)
    if cvalue is None:
        raise ValueError, ('Unknown color type: "%s"' % value)
    if type == ISCMYKFLAG:
        return cvalue
    elif type == ISRGBFLAG:
        return _rgb2cmyk(_int2rgbtuple(cvalue))

def _rgbtuple2int(t):
    """    Convert from a RGB color tuple to RGB integer

        >>> _rgbtuple2int((0, 4, 210))
        1234L
        >>> _rgbtuple2int((0, 48, 57))
        12345L
        >>> _rgbtuple2int((0, 214, 216))
        55000L
        >>> _rgbtuple2int((6, 241, 88))
        455000L
    """
    r = int(round(t[0]))                                # Not all r,g,b values are necessarily
    g = int(round(t[1]))                                # integers, eg from _cmyk2rgb
    b = int(round(t[2]))                                # so we round and truncate them
    return long(r) * 65536 + g * 256 + b

def _int2rgbtuple(i):
    """    Convert from a RGB color integer to RGB tuple

        >>> _int2rgbtuple(1234)
        (0, 4, 210)
        >>> _int2rgbtuple(12345)
        (0, 48, 57)
        >>> _int2rgbtuple(55000)
        (0, 214, 216)
        >>> _int2rgbtuple(455000)
        (6, 241, 88)
    """
    if not isinstance(i, int):                # We need to have an integer here
        try:                                # so we try to make it
            i = int(i)                        # otherwise return and error message
        except:
            raise ValueError, ('Value is not an integer: "%s"' % `i`)
    return (i >> 16) & 0xff, (i >> 8) & 0xff, i & 0xff

def _cmyk2rgb((c, m, y, k), density=1):
    """    Convert from a CMYK color tuple to an RGB color tuple
        From the Adobe Postscript Ref. Manual 2nd ed. Page 306
        
        >>> _cmyk2rgb((1, 1, 1, 1))
        (0.0, 0.0, 0.0)
        >>> _cmyk2rgb((0, 0, 0, 0))
        (255.0, 255.0, 255.0)
        >>> _cmyk2rgb((0.2, 0.6, 0.8, 0.2))
        (153.0, 50.999999999999986, 0.0)
    """
    r = 1.0 - min(1.0, c + k)
    g = 1.0 - min(1.0, m + k)
    b = 1.0 - min(1.0, y + k)
    return (r * 255, g * 255, b * 255)

def _rgb2cmyk((r, g, b)):
    """One way to get cmyk from rgb."

        >>> _rgb2cmyk((100, 100, 100))
        (0, 0, 0, 0.60784313725490202)
        >>> _rgb2cmyk((0, 0, 0))
        (0, 0, 0, 1)
        >>> _rgb2cmyk((1, 1, 1))
        (0, 0, 0, 0.99607843137254903)
        
    """
    c = 1 - (r / 255.0)
    m = 1 - (g / 255.0)
    y = 1 - (b / 255.0)
    k = min(c, m, y)
    c = min(1, max(0, c - k))
    m = min(1, max(0, m - k))
    y = min(1, max(0, y - k))
    k = min(1, max(0, k))
    return float(c), float(m), float(y), float(k)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
