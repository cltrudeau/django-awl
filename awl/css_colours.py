import re

PREDEFINED = ('aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
    'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet',
    'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral',
    'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
    'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta',
    'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon',
    'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise',
    'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue',
    'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
    'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow',
    'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki',
    'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue',
    'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray',
    'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue',
    'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
    'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue',
    'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue',
    'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue',
    'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace',
    'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod',
    'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff',
    'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red',
    'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
    'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
    'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle',
    'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow',
    'yellowgreen'
)


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
    global PREDEFINED, HEX_MATCH, RGB_MATCH, RGBA_MATCH, HSL_MATCH, HSLA_MATCH
    value = value.strip()

    # hex match
    if HEX_MATCH.match(value) or RGB_MATCH.match(value) or \
            RGBA_MATCH.match(value) or HSL_MATCH.match(value) or \
            HSLA_MATCH.match(value) or value in PREDEFINED:
        return True

    return False
