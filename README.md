# BDF2LVGL: Convert bitmap font in BDF format to LVGL format

When using [LVGL][] to develop GUI for low-resolution screens (e.g. 128x64 black-and-white), small yet legible (5x11, 6x13, etc.) pixel-perfect bitmap fonts are very desirable.
Many open-source bitmap fonts are distributed in the BDF format. However the LVGL's built-in converter only supports rasterizing from TTF.
This tool attempts to solve that problem.

[LVGL]: https://lvgl.io/

## Usage

1. Install Python 3.9 and [Poetry](https://python-poetry.org/).
2. Clone this repo.
3. `cd` into repo root
4. `poetry run bdf2lvgl path/to/your/font.bdf`

This will hopefully generate a `.c` file under the current working directory.

You can also use `poetry run bdf2lvgl --help` to see options.


## Limitations

- Only tested on a few fonts.
- No char range filtering --- generated file contains every codepoint defined in the input file.
  (However, you can easily use [FontForge](https://fontforge.org) to add/remove/change the glyphs in a BDF file)


## Links to some good fonts

- [Creep2](https://github.com/raymond-w-ko/creep2/blob/69dc0de03d89f31b8074981cec0be45d4aceb245/creep2-11.bdf)
- [Cozette](https://github.com/slavfox/Cozette) includes many [NerdFonts](https://www.nerdfonts.com) symbols.
