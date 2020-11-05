import re

WEB_COLOUR_MAP = {
    'AliceBlue':'#F0F8FF',
    'AntiqueWhite':'#FAEBD7',
    'Aqua':'#00FFFF',
    'Aquamarine':'#7FFFD4',
    'Azure':'#F0FFFF',
    'Beige':'#F5F5DC',
    'Bisque':'#FFE4C4',
    'Black':'#000000',
    'BlanchedAlmond':'#FFEBCD',
    'Blue':'#0000FF',
    'BlueViolet':'#8A2BE2',
    'Brown':'#A52A2A',
    'BurlyWood':'#DEB887',
    'CadetBlue':'#5F9EA0',
    'Chartreuse':'#7FFF00',
    'Chocolate':'#D2691E',
    'Coral':'#FF7F50',
    'CornflowerBlue':'#6495ED',
    'Cornsilk':'#FFF8DC',
    'Crimson':'#DC143C',
    'Cyan':'#00FFFF',
    'DarkBlue':'#00008B',
    'DarkCyan':'#008B8B',
    'DarkGoldenRod':'#B8860B',
    'DarkGray':'#A9A9A9',
    'DarkGrey':'#A9A9A9',
    'DarkGreen':'#006400',
    'DarkKhaki':'#BDB76B',
    'DarkMagenta':'#8B008B',
    'DarkOliveGreen':'#556B2F',
    'Darkorange':'#FF8C00',
    'DarkOrchid':'#9932CC',
    'DarkRed':'#8B0000',
    'DarkSalmon':'#E9967A',
    'DarkSeaGreen':'#8FBC8F',
    'DarkSlateBlue':'#483D8B',
    'DarkSlateGray':'#2F4F4F',
    'DarkSlateGrey':'#2F4F4F',
    'DarkTurquoise':'#00CED1',
    'DarkViolet':'#9400D3',
    'DeepPink':'#FF1493',
    'DeepSkyBlue':'#00BFFF',
    'DimGray':'#696969',
    'DimGrey':'#696969',
    'DodgerBlue':'#1E90FF',
    'FireBrick':'#B22222',
    'FloralWhite':'#FFFAF0',
    'ForestGreen':'#228B22',
    'Fuchsia':'#FF00FF',
    'Gainsboro':'#DCDCDC',
    'GhostWhite':'#F8F8FF',
    'Gold':'#FFD700',
    'GoldenRod':'#DAA520',
    'Gray':'#808080',
    'Grey':'#808080',
    'Green':'#008000',
    'GreenYellow':'#ADFF2F',
    'HoneyDew':'#F0FFF0',
    'HotPink':'#FF69B4',
    'IndianRed':'#CD5C5C',
    'Indigo':'#4B0082',
    'Ivory':'#FFFFF0',
    'Khaki':'#F0E68C',
    'Lavender':'#E6E6FA',
    'LavenderBlush':'#FFF0F5',
    'LawnGreen':'#7CFC00',
    'LemonChiffon':'#FFFACD',
    'LightBlue':'#ADD8E6',
    'LightCoral':'#F08080',
    'LightCyan':'#E0FFFF',
    'LightGoldenRodYellow':'#FAFAD2',
    'LightGray':'#D3D3D3',
    'LightGrey':'#D3D3D3',
    'LightGreen':'#90EE90',
    'LightPink':'#FFB6C1',
    'LightSalmon':'#FFA07A',
    'LightSeaGreen':'#20B2AA',
    'LightSkyBlue':'#87CEFA',
    'LightSlateGray':'#778899',
    'LightSlateGrey':'#778899',
    'LightSteelBlue':'#B0C4DE',
    'LightYellow':'#FFFFE0',
    'Lime':'#00FF00',
    'LimeGreen':'#32CD32',
    'Linen':'#FAF0E6',
    'Magenta':'#FF00FF',
    'Maroon':'#800000',
    'MediumAquaMarine':'#66CDAA',
    'MediumBlue':'#0000CD',
    'MediumOrchid':'#BA55D3',
    'MediumPurple':'#9370D8',
    'MediumSeaGreen':'#3CB371',
    'MediumSlateBlue':'#7B68EE',
    'MediumSpringGreen':'#00FA9A',
    'MediumTurquoise':'#48D1CC',
    'MediumVioletRed':'#C71585',
    'MidnightBlue':'#191970',
    'MintCream':'#F5FFFA',
    'MistyRose':'#FFE4E1',
    'Moccasin':'#FFE4B5',
    'NavajoWhite':'#FFDEAD',
    'Navy':'#000080',
    'OldLace':'#FDF5E6',
    'Olive':'#808000',
    'OliveDrab':'#6B8E23',
    'Orange':'#FFA500',
    'OrangeRed':'#FF4500',
    'Orchid':'#DA70D6',
    'PaleGoldenRod':'#EEE8AA',
    'PaleGreen':'#98FB98',
    'PaleTurquoise':'#AFEEEE',
    'PaleVioletRed':'#D87093',
    'PapayaWhip':'#FFEFD5',
    'PeachPuff':'#FFDAB9',
    'Peru':'#CD853F',
    'Pink':'#FFC0CB',
    'Plum':'#DDA0DD',
    'PowderBlue':'#B0E0E6',
    'Purple':'#800080',
    'RebeccaPurple':'#663399',
    'Red':'#FF0000',
    'RosyBrown':'#BC8F8F',
    'RoyalBlue':'#4169E1',
    'SaddleBrown':'#8B4513',
    'Salmon':'#FA8072',
    'SandyBrown':'#F4A460',
    'SeaGreen':'#2E8B57',
    'SeaShell':'#FFF5EE',
    'Sienna':'#A0522D',
    'Silver':'#C0C0C0',
    'SkyBlue':'#87CEEB',
    'SlateBlue':'#6A5ACD',
    'SlateGray':'#708090',
    'SlateGrey':'#708090',
    'Snow':'#FFFAFA',
    'SpringGreen':'#00FF7F',
    'SteelBlue':'#4682B4',
    'Tan':'#D2B48C',
    'Teal':'#008080',
    'Thistle':'#D8BFD8',
    'Tomato':'#FF6347',
    'Turquoise':'#40E0D0',
    'Violet':'#EE82EE',
    'Wheat':'#F5DEB3',
    'White':'#FFFFFF',
    'WhiteSmoke':'#F5F5F5',
    'Yellow':'#FFFF00',
    'YellowGreen':'#9ACD32',
}


LOWER_WEB_COLOUR_MAP = {k.lower():v for k, v in WEB_COLOUR_MAP.items()}


HEX_MATCH = re.compile(
    """               # #fff or #FBF01B
    \#                   # starts with #
    ([a-fA-F0-9]{3})     # excatly 3 hex digits
    $                    # and nothing more
    |                    # OR
    \#
    ([a-fA-F0-9]{6})     # exactly 6 hex digits
    $                    # and nothing more
    """, re.VERBOSE)


RGB_MATCH = re.compile(
    """                # rgb(0, 12, 123)
    ^[rR][gG][bB]      # starts with "rgb"
    \s*\(\s*           # spaces ( spaces
    \d{1,3}            # 1-3 digits
    \s*,\s*            # spaces comma spaces
    \d{1,3}            # 1-3 digits
    \s*,\s*            # spaces comma spaces
    \d{1,3}            # 1-3 digits
    \s*\)$             # spaces ) EOS
    """, re.VERBOSE)


RGBA_MATCH = re.compile(
    """                # rgba(0, 12, 123, 0.3)
    ^[rR][gG][bB][aA]  # starts with "rgb"
    \s*\(\s*           # spaces ( spaces
    \d{1,3}            # 1-3 digits
    \s*,\s*            # spaces comma spaces
    \d{1,3}            # 1-3 digits
    \s*,\s*            # spaces comma spaces
    \d{1,3}            # 1-3 digits
    \s*,\s*            # spaces comma spaces
    \d+                # first digit of opacity
    (\.\d+)?           # one or more digit after optional decimal place
    \s*\)$             # spaces ) EOS
    """, re.VERBOSE)


HSL_MATCH = re.compile(
    """                # hsl(120, 5%, 100%)
    ^[hH][sS][lL]      # starts with "hsl"
    \s*\(\s*           # spaces ( spaces
    \d{1,3}            # 1-3 digits for Hue
    \s*,\s*            # spaces comma spaces
    \d{1,3}\s*%        # 1-3 digits spaces "%" for Saturation
    \s*,\s*            # spaces comma spaces
    \d{1,3}\s*%        # 1-3 digits spaces "%" for Lightness
    \s*\)$             # spaces ) EOS
    """, re.VERBOSE)


HSLA_MATCH = re.compile(
    """                # hsla(120, 5%, 100%, 0.3)
    ^[hH][sS][lL][aA]  # starts with "hsla"
    \s*\(\s*           # spaces ( spaces
    \d{1,3}            # 1-3 digits for Hue
    \s*,\s*            # spaces comma spaces
    \d{1,3}\s*%        # 1-3 digits spaces "%" for Saturation
    \s*,\s*            # spaces comma spaces
    \d{1,3}\s*%        # 1-3 digits spaces "%" for Lightness
    \s*,\s*            # spaces comma spaces
    \d+                # first digits of opacity
    (\.\d+)?           # optional one or more decimal digits
    \s*\)$             # spaces ) EOS
    """, re.VERBOSE)


def is_colour(value):
    """Returns True if the value given is a valid CSS colour, i.e. matches one
    of the regular expressions in the module or is in the list of
    predetefined values by the browser.
    """
    global LOWER_WEB_COLOUR_MATH, HEX_MATCH, RGB_MATCH, RGBA_MATCH, HSL_MATCH 
    global HSLA_MATCH
    value = value.strip()

    # hex match
    if HEX_MATCH.match(value) or RGB_MATCH.match(value) or \
            RGBA_MATCH.match(value) or HSL_MATCH.match(value) or \
            HSLA_MATCH.match(value) or value in LOWER_WEB_COLOUR_MAP.keys():
        return True

    return False


def colour_to_rgb(colour):
    """Takes a web colour name or hex value and returns a tuple containing the
    corresponding decimal RGB values

    :param colour: web colour name (e.g. "pink") or hex colur (e.g. "#f0f", 
                   "#f2d5e3"
    :returns: tuple with decimal RGB values
    """
    if not colour.startswith('#'):
        # Convert to hex first
        try:
            colour = LOWER_WEB_COLOUR_MAP[colour.lower()]
        except KeyError:
            raise AttributeError('Unknown colour name')

    if len(colour) == 7:
        arr = int(colour[1:3], base=16)
        gee = int(colour[3:5], base=16)
        bee = int(colour[5:], base=16)

        return (arr, gee, bee)

    elif len(colour) == 4:
        arr = int(colour[1]*2, base=16)
        gee = int(colour[2]*2, base=16)
        bee = int(colour[3]*2, base=16)

        return (arr, gee, bee)


    raise AttributeError('Bad hex colour')


def colour_to_rgb_string(colour):
    """Takes a web colour name or hex value and returns an rgb() string that 
    can be used in a CSS file. 

    :param colour: web colour name (e.g. "pink") or hex colur (e.g. "#f0f", 
                   "#f2d5e3"
    :returns: CSS rgb() function string (e.g. rgb(102, 51, 153) )
    """
    arr, gee, bee = colour_to_rgb(colour)
    return f'rgb({arr}, {gee}, {bee})'
