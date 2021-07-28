import logging

import bdflib.reader
import click

from bdf2lvgl.parse import parse_font
from bdf2lvgl.codegen.c import gen_lv_font


@click.command()
@click.argument('input', type=click.File('rb'))
@click.option(
    '--output',
    '-o',
    help='generated C source code file (default to font identifier + ".c")')
@click.option(
    '--name',
    '-n',
    help='font identifier (default to font family name + height in pixels)')
@click.option(
    '--min_dense_run',
    type=int,
    default=64,
    show_default=True,
    help=
    'mininum number of consecutive unicode codepoints to be recognized as a dense range in cmap'
)
def main(input, output, name, min_dense_run):
    try:
        font = bdflib.reader.read_bdf(input)
        assert font is not None
    except AssertionError as e:
        logging.fatal(f'Failed to parse bdf; error: {e}')

    parsed = parse_font(font, name=name, min_dense_run=min_dense_run)
    if not output:
        output = parsed['name'] + '.c'

    with open(output, 'w', encoding='utf8') as fout:
        fout.write(gen_lv_font(parsed))
