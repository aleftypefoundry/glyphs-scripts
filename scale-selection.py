#MenuTitle: Scale Glyphs
# -*- coding: utf-8 -*-

__doc__="""
Scale selected glyphs by a percentage.
"""

import GlyphsApp
import vanilla
from Foundation import NSAffineTransform

def validateInput(inputValue):
    try:
        value = float(inputValue)
        return value >= 0
    except ValueError:
        return False

def scaleGlyphs(sender):
    # Validate the user input
    if not validateInput(w.scaleInput.get()):
        raise ValueError("Invalid input. Please enter a valid number.")
        return

    # Get the scale factor from the user input
    scaleFactor = float(w.scaleInput.get()) / 100.0

    # Get the current font
    font = Glyphs.font

    # Get selected glyphs
    selectedGlyphs = [l.parent for l in font.selectedLayers]

    # Iterate through each selected glyph
    for glyph in selectedGlyphs:
        for layer in glyph.layers:
            # Record the original width
            original_width = layer.width

            # Calculate the new width after scaling
            new_width = original_width * scaleFactor

            # Scale the glyph
            layer.applyTransform([
                scaleFactor, # x scale factor
                0.0, # x skew factor
                0.0, # y skew factor
                scaleFactor, # y scale factor
                0.0, # x position
                0.0  # y position
            ])

            # Update anchor positions
            for anchor in layer.anchors:
                anchor.position = (anchor.position.x * scaleFactor, anchor.position.y * scaleFactor)

            # Update sidebearings
            print(layer.LSB)
            print(layer.RSB)
            # Adjust the RSB
            adjustment = (original_width - new_width) / 2  # The adjustment value to keep the glyph centered
            layer.RSB -= adjustment
            layer.LSB *= scaleFactor
            print(adjustment)
            print(layer.LSB)
            print(layer.RSB)
    # Close the window
    w.close()
# Create a window for user input
w = vanilla.FloatingWindow((200, 70), "Scale Glyphs")

# Add a text input field and a button to the window
w.scaleInput = vanilla.EditText((10, 10, -10, 20), "100")
w.scaleButton = vanilla.Button((10, 40, -10, 20), "Scale", callback=scaleGlyphs)

# Open the window
w.open()
