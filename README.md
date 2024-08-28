# About

These are Python scripts intended for font production in the [Glyphs font editor](http://glyphsapp.com/).

## Installation

I recommend to use git for getting the scripts, because it is easier for you to keep them up to date. Use this git command for cloning the repository into your *Scripts* folder:

```bash
git clone https://github.com/aleftypefoundry/glyphs-scripts ~/Library/Application\ Support/Glyphs/Scripts/atf/
```

If the terminal scares you, feel free to use one of the many readily available git clients, e.g. the free [Source Tree](https://www.sourcetreeapp.com) or [GitHub Desktop](https://desktop.github.com).

After you installed the ATF scripts, you can **update** this script repository (and all the others you have in your *Scripts* folder) by running *Scripts > mekkablue > App > Update git Repositories in Scripts Folder.*

# Troubleshooting

Please report problems and request features [as a GitHub issue](/issues). Make sure you have the latest version of the scripts and your app is up to date. And please, always **indicate both your Glyphs and macOS version.** Thank you.

# Requirements

The scripts require a recent version of Glyphs 3.x running on macOS 10.9 or later. I can only test them and make them work in the latest version of the software. If a script is not working for you, please first update to the latest version of the script.

# About the Scripts

All the scripts show a **tooltip** when you hover the mouse pointer over their menu entry. In scripts with a GUI, most UI elements (checkboxes, text entry fields, etc.) have tooltips as well. This way you get the explanation you need right where it counts.

* **Cursive Cleaner:** Removes `entry` and `exit` anchors from glyphs. Can handle exceptions glyphs.
* **Generate Webfonts:** Generates webfonts (WOFF2) from instances (or selected instances) with css file.
* **Remove Overlap:** Removes overlap in all glyphs.
* **Scale Selection:** Scales the selected glyphs by a factor.

# License

This project is licensed under the [MLP 2.0](https://opensource.org/licenses/MLP-2.0) license. You are free to use, modify and distribute the scripts. If you do, please keep the ATF header intact and consider linking back to this repository. Thank you.

# Change Log

- 26-08-2024: Initial release.
- 28-08-2024: Updated `Cursive Cleaner` script:
  - Added support for more anchors.
  - Added support for skipping marks.
  - Exceptions now includes components using the exception glyphs.
