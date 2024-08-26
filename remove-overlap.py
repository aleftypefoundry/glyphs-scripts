#MenuTitle: Remove Overlap in All Layers
# -*- coding: utf-8 -*-

__doc__="""
Goes through all layers and removes overlap in all glyphs.
"""

import GlyphsApp

font = Glyphs.font

for glyph in font.glyphs:
    for layer in glyph.layers:
        layer.removeOverlap()

