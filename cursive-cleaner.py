#MenuTitle: Cursive Anchor Cleaner
# -*- coding: utf-8 -*-

__doc__="""
Goes through all layers and removes anchors in all glyphs.
"""

import GlyphsApp
import vanilla

class RemoveAnchorsUI:
    def __init__(self):
        # Create the main window
        self.w = vanilla.FloatingWindow((300, 320), "Remove Anchors")

        # Exception glyphs input
        self.w.exceptionLabel = vanilla.TextBox((15, 15, -15, 20), "Exception Glyphs (comma-separated):")
        self.w.exceptionInput = vanilla.EditText((15, 40, -15, 20))

        # Anchor removal options (checkboxes)
        self.w.entryCheck = vanilla.CheckBox((15, 70, -15, 20), "Remove 'entry'", callback=self.checkboxCallback)
        self.w.exitCheck = vanilla.CheckBox((15, 95, -15, 20), "Remove 'exit'", callback=self.checkboxCallback)
        self.w.topCheck = vanilla.CheckBox((15, 120, -15, 20), "Remove 'top'", callback=self.checkboxCallback)
        self.w.bottomCheck = vanilla.CheckBox((15, 145, -15, 20), "Remove 'bottom'", callback=self.checkboxCallback)
        self.w.topVariantCheck = vanilla.CheckBox((15, 170, -15, 20), "Remove 'top_$'", callback=self.checkboxCallback)
        self.w.bottomVariantCheck = vanilla.CheckBox((15, 195, -15, 20), "Remove 'bottom_$'", callback=self.checkboxCallback)
        self.w.fullCleanupCheck = vanilla.CheckBox((15, 220, -15, 20), "Full Cleanup", callback=self.checkboxCallback)

        # Buttons
        self.w.cancelButton = vanilla.Button((15, -40, 100, 20), "Cancel", callback=self.cancelCallback)
        self.w.okButton = vanilla.Button((-115, -40, 100, 20), "OK", callback=self.okCallback)

        # Open the window
        self.w.open()

    def checkboxCallback(self, sender):
        # When "Full Cleanup" is checked, uncheck all other checkboxes
        if sender == self.w.fullCleanupCheck and self.w.fullCleanupCheck.get():
            self.w.entryCheck.set(False)
            self.w.exitCheck.set(False)
            self.w.topCheck.set(False)
            self.w.bottomCheck.set(False)
            self.w.topVariantCheck.set(False)
            self.w.bottomVariantCheck.set(False)
        # If any other checkbox is checked, uncheck "Full Cleanup"
        elif sender != self.w.fullCleanupCheck and sender.get():
            self.w.fullCleanupCheck.set(False)

    def cancelCallback(self, sender):
        # Close the window without doing anything
        self.w.close()

    def okCallback(self, sender):
        # Get the exception glyphs from the input field
        exceptionGlyphs = [name.strip() for name in self.w.exceptionInput.get().split(',')]

        # Get the selected options for anchor removal
        remove_entry = self.w.entryCheck.get()
        remove_exit = self.w.exitCheck.get()
        remove_top = self.w.topCheck.get()
        remove_bottom = self.w.bottomCheck.get()
        remove_top_variant = self.w.topVariantCheck.get()
        remove_bottom_variant = self.w.bottomVariantCheck.get()
        full_cleanup = self.w.fullCleanupCheck.get()

        # Perform the anchor removal based on the user's input
        font = Glyphs.font
        removedSomething = False

        for glyph in font.glyphs:
            # Skip the glyphs that are in the exception list
            if str(glyph.name) in exceptionGlyphs:
                continue

            # Check if any components of the glyph are in the exception list
            should_skip_glyph = False
            for layer in glyph.layers:
                for component in layer.components:
                    if component.componentName in exceptionGlyphs:
                        should_skip_glyph = True
                        break
                if should_skip_glyph:
                    break

            # Skip this glyph if it or any of its components are in the exception list
            if should_skip_glyph:
                continue

            for layer in glyph.layers:
                # Full Cleanup (remove all anchors)
                if full_cleanup:
                    # Delete all anchors from the layer
                    if layer.anchors:
                        layer.anchors = {}  # Remove all anchors
                        removedSomething = True
                else:
                    # Remove specific anchors based on the checked boxes
                    if remove_entry and 'entry' in layer.anchors:
                        del layer.anchors['entry']
                        removedSomething = True
                    if remove_exit and 'exit' in layer.anchors:
                        del layer.anchors['exit']
                        removedSomething = True
                    if remove_top and 'top' in layer.anchors:
                        del layer.anchors['top']
                        removedSomething = True
                    if remove_bottom and 'bottom' in layer.anchors:
                        del layer.anchors['bottom']
                        removedSomething = True
                    if remove_top_variant or remove_bottom_variant:
                        # Remove top_$ and bottom_$ variants
                        for anchorName in list(layer.anchors.keys()):
                            if remove_top_variant and anchorName.startswith('top_'):
                                del layer.anchors[anchorName]
                                removedSomething = True
                            if remove_bottom_variant and anchorName.startswith('bottom_'):
                                del layer.anchors[anchorName]
                                removedSomething = True

        # Give feedback to the user
        if removedSomething:
            Glyphs.showNotification("Success", "Anchors have been successfully removed.")
        else:
            Glyphs.showNotification("No Anchors Removed", "No anchors were removed. Check the glyphs and anchors.")

        # Close the window
        self.w.close()

# Run the script and open the UI
RemoveAnchorsUI()
