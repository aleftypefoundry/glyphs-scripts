#MenuTitle: Cursive Anchor Cleaner
# -*- coding: utf-8 -*-

__doc__="""
Goes through all layers and removes entry/exit anchors in all glyphs.
"""

import GlyphsApp
import vanilla

class RemoveAnchorsUI:
    def __init__(self):
        # Create the main window
        self.w = vanilla.FloatingWindow((300, 200), "Remove Anchors")

        # Exception glyphs input
        self.w.exceptionLabel = vanilla.TextBox((15, 15, -15, 20), "Exception Glyphs (comma-separated):")
        self.w.exceptionInput = vanilla.EditText((15, 40, -15, 20))

        # Anchor removal options
        self.w.anchorOption = vanilla.RadioGroup((15, 70, -15, 40), ["Remove 'entry' only", "Remove 'exit' only", "Remove both"], isVertical=True)
        self.w.anchorOption.set(2)  # Default: "Remove both"

        # Buttons
        self.w.cancelButton = vanilla.Button((15, -40, 100, 20), "Cancel", callback=self.cancelCallback)
        self.w.okButton = vanilla.Button((-115, -40, 100, 20), "OK", callback=self.okCallback)

        # Open the window
        self.w.open()

    def cancelCallback(self, sender):
        # Close the window without doing anything
        self.w.close()

    def okCallback(self, sender):
        # Get the exception glyphs from the input field
        exceptionGlyphs = self.w.exceptionInput.get().split(',')

        # Get the selected anchor removal option
        option = self.w.anchorOption.get()

        # Perform the anchor removal based on the user's input
        font = Glyphs.font
        removedSomething = False

        for glyph in font.glyphs:
            # Skip the glyphs that are in the exception list
            # Convert glyph name to string and strip any whitespace around exceptionGlyphs items
            if str(glyph.name) in exceptionGlyphs:
                print("Skipping glyph: %s" % glyph.name)
                continue
            #if glyph.name in exceptionGlyphs:
            #    continue
            print("Processing glyph: %s" % glyph.name)
            for layer in glyph.layers:
                # Check which anchors to remove based on the selected option
                if option == 0:
                    del layer.anchors['entry']
                    removedSomething = True
                elif option == 1:
                    del layer.anchors['exit']
                    removedSomething = True
                elif option == 2:
                    # Remove both anchors if they exist
                    #if 'entry' in layer.anchors:
                    del layer.anchors['entry']
                        #removedSomething = True
                    #if 'exit' in layer.anchors:
                    del layer.anchors['exit']
                    removedSomething = True

        # Give feedback to the user
        print("Removed something: %s" % removedSomething)
        if removedSomething:
            Glyphs.showNotification("Success", "Anchors have been successfully removed.")
        else:
            Glyphs.showNotification("No Anchors Removed", "No anchors were removed. Check the glyphs and anchors.")

        # Close the window
        self.w.close()

# Run the script and open the UI
RemoveAnchorsUI()