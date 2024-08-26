# MenuTitle: Generate Webfonts with CSS
# -*- coding: utf-8 -*-

__doc__ = """
Generates webfonts (WOFF2) from instances (or selected instances) with css file.
"""

import os
import vanilla
from AppKit import NSOpenPanel, NSFileHandlingPanelOKButton
from GlyphsApp import Glyphs

# Access the current font
font = Glyphs.font


class ExportDialog:
    def __init__(self):
        # Window 'self.w':
        windowWidth = 560
        windowHeight = len(font.instances) + 170
        self.w = vanilla.FloatingWindow(
            (windowWidth, windowHeight),
            "Web Exporter",
            autosaveName="com.atf.WebExporter",
        )

        # UI elements:
        linePos, inset, lineHeight = 10, 15, 22
        indent = 75

        # Label and checkbox for "Available Instances" and "Export All":
        self.w.label_weights = vanilla.TextBox(
            (inset, linePos + 2, -inset, 14), "Available Instances:", sizeStyle="small"
        )
        self.w.checkbox_all = vanilla.CheckBox(
            (inset + 160, linePos, 100, 20),
            "Export All",
            value=True,
            callback=self.toggle_all,
            sizeStyle="small",
        )
        linePos += lineHeight

        # Initialize the checkboxes attribute
        self.checkboxes = []

        # Add checkboxes for the font's available instances
        checkboxes_views = []
        for i, instance in enumerate(font.instances):
            if instance.active:
                checkbox = vanilla.CheckBox(
                    (0, 0, -10, 20),
                    instance.name,
                    value=instance.active,
                    callback=self.toggle_instance,
                    sizeStyle="small",
                )
                checkboxes_views.append(checkbox)
                self.checkboxes.append(checkbox)

        # Group for instances checkboxes:
        self.w.instances_group = vanilla.Box(
            (inset, linePos, -inset, 3 * len(font.instances))
        )
        self.w.instances_group.stack_view = vanilla.HorizontalStackView(
            (0, 0, -0, -0), checkboxes_views, spacing=4, edgeInsets=(4, 0, 0, 4)
        )
        linePos += 5 * len(font.instances)

        # Label and button for choosing the output directory:
        self.w.outputBox = vanilla.Box(
            (inset, linePos, -inset, 5 * len(font.instances))
        )

        self.w.outputBox.label_dir = vanilla.TextBox(
            "auto", "Output directory:", sizeStyle="small"
        )

        self.w.outputBox.text_dir = vanilla.TextBox("auto", "", sizeStyle="small")

        self.w.outputBox.button_dir = vanilla.Button(
            "auto",
            "Browse",
            sizeStyle="regular",
            callback=self.choose_dir,
        )

        self.w.outputBox.verticalStack = vanilla.VerticalStackView(
            "auto",
            views=[
                dict(view=self.w.outputBox.label_dir),
                dict(view=self.w.outputBox.text_dir),
            ],
            alignment="leading",
            spacing=4,
        )

        self.w.outputBox.horizontalStack = vanilla.HorizontalStackView(
            (0, 0, 0, 0),
            views=[
                dict(view=self.w.outputBox.verticalStack),
                dict(view=self.w.outputBox.button_dir),
            ],
            spacing=4,
            edgeInsets=(4, 0, 0, 4),
        )

        linePos += 10 + 5 * len(font.instances)

        # Segmented button for cancel and export:
        self.w.segmented_button = vanilla.SegmentedButton(
            "auto",
            [dict(title="Cancel"), dict(title="Export")],
            sizeStyle="regular",
            callback=self.segmented_button_callback,
        )

        # Text box for displaying errors:
        self.w.text_error = vanilla.TextBox("auto", "", sizeStyle="mini")

        self.w.exportHorizontalStack = vanilla.HorizontalStackView(
            (inset, linePos, -inset, 3 * len(font.instances)),
            views=[
                dict(view=self.w.text_error),
                dict(view=self.w.segmented_button),
            ],
            alignment="leading",
            spacing=4,
            edgeInsets=(4, 0, 0, 4),
        )

        # Open window and focus on it:
        self.w.open()
        self.w.makeKey()

    def toggle_all(self, sender):
        # Get the value of the "Export All" checkbox
        value = self.w.checkbox_all.get()
        # Set the value of all instance checkboxes to the value of the "Export All" checkbox
        for checkbox in self.checkboxes:
            checkbox.set(value)

    def toggle_instance(self, sender):
        # If any instance checkbox is unchecked, uncheck the "Export All" checkbox
        if not all(checkbox.get() for checkbox in self.checkboxes):
            self.w.checkbox_all.set(False)

    def choose_dir(self, sender):
        # Open a directory selection dialog
        panel = NSOpenPanel.openPanel()
        panel.setCanChooseFiles_(False)
        panel.setCanChooseDirectories_(True)
        if panel.runModal() == NSFileHandlingPanelOKButton:
            # Get the selected directory
            output_dir = panel.URL().path()

            # Update the text box with the selected directory
            self.w.outputBox.text_dir.set(output_dir)

    def export(self, sender):
        # Check if at least one instance is checked
        if not any(checkbox.get() for checkbox in self.checkboxes):
            # Output an error message if no instances are checked
            self.w.text_error.set("Please select at least one instance to export.")
            return

        # Get the output directory from the user input
        output_dir = self.w.outputBox.text_dir.get()

        # Check if the output directory is selected
        if not output_dir:
            # Output an error message if no output directory is selected
            self.w.text_error.set("Please select an output directory.")
            return

        try:
            # Create a subfolder named 'fonts'
            output_dir = os.path.join(output_dir, "fonts")
            os.makedirs(output_dir, exist_ok=True)

            # Loop over each checkbox
            for i, checkbox in enumerate(self.checkboxes):
                if checkbox.get():
                    # Get the corresponding instance of the font
                    instance = font.instances[i]

                    # Define the path to the webfont file
                    font_path = os.path.join(
                        output_dir, "{}.woff2".format(instance.name)
                    )

                    # Generate the webfont
                    instance.generate(FontPath=font_path, Containers=[WOFF2])

                    # Define the CSS code
                    css_code = """
                    @font-face {{
                        font-family: '{}';
                        src: url('fonts/{}.woff2') format('woff2');
                        font-weight: {};
                        font-style: {};
                    }}
                    """.format(
                        font.familyName,
                        instance.name,
                        instance.weightClass,
                        instance.widthClass,
                    )

                    # Write the CSS code to a file
                    with open(os.path.join(output_dir, "../font.css"), "a") as f:
                        f.write(css_code)

            # Close the dialog window
            self.w.close()

            # Show a notification
            Glyphs.showNotification("Export Webfonts", "Export successful.")
        except Exception as e:
            # Display the error in the text box
            self.w.text_error.set(str(e))

    def cancel(self, sender):
        # Close the dialog window
        self.w.close()

    def segmented_button_callback(self, sender):
        # Get the selected segment
        selected_segment = sender.get()
        # If "Cancel" is selected
        if selected_segment == 0:
            self.cancel(sender)
        # If "Export" is selected
        elif selected_segment == 1:
            self.export(sender)


# Create a new export dialog
ExportDialog()
