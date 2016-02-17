# awl.tests.test_colours.py

from django.test import TestCase

from awl.css_colours import is_colour, PREDEFINED

# ============================================================================

class ColourTests(TestCase):
    def test_colours_true(self):
        items = [
            # short hex
            '#000', '#fff', '#FFF', '#123', '#456', '#789', '#abc', '#def', 
            '#ABC', '#DEF', 

            # long hex
            '#000000', '#ffffff', '#FFFFFF', '#123456', '#789abc', 
            '#defABC', '#DEF000',

            # rgb
            'rgb(0,0,0)', ' rgb ( 0 , 0 , 0 ) ', 'rgb(255,255,255)', 
            ' rgb ( 255 , 255 , 255 ) ',

            # rgba
            'rgba(0,0,0,0)', 'rgba(0,0,0,0.1)', ' rgba ( 0 , 0 , 0 , 0 ) ',
            ' rgba ( 0 , 0 , 0 , 0.1 ) ', 'rgba(255,255,255,1)', 
            'rgba(255,255,255,1.0)', ' rgba ( 255 , 255 , 255 , 1 ) ',
            ' rgba ( 255 , 255 , 255 , 1.0 ) ',

            # hsl
            'hsl(0,0%,0%)', ' hsl ( 0 , 0 % , 0 % ) ', 'hsl(255,120%,120%)', 
            ' hsl ( 255 , 120 % , 120 % ) ',

            # hsla
            'hsla(0,0%,0%,0)', 'hsla(0,0%,0%,0.1)', 
            ' hsla ( 0 , 0 % , 0 % , 0 ) ',
            ' hsla ( 0 , 0 % , 0 % , 0.1 ) ', 'hsla(255,120%,120%,1)', 
            'hsla(255,120%,120%,1.0)', ' hsla ( 255 , 120 % , 120 % , 1 ) ',
            ' hsla ( 255 , 140 % , 140 % , 1.0 ) ',
        ]
        items.extend(PREDEFINED)

        for item in items:
            self.assertTrue(is_colour(item), '%s was not True' % item)

    def test_colours_false(self):
        items = ['#ff', '#ffff', '#fffff', '#fffffff', 'rgb(0,0,0,0)', 
            'rgba(0,0,0)', 'hsl(0,0,0)', 'hsl(0,0%,0%,0)', 
            'hsla(0,0,0)', 'hsla(0,0%,0%)',
        ]

        for item in items:
            self.assertFalse(is_colour(item), '%s was not False' % item)
