import numpy as np


def parse_font(font, *, name=None, min_dense_run=64):
    family = font.properties[b'FAMILY_NAME']
    ascent = font.properties[b'FONT_ASCENT']
    descent = font.properties[b'FONT_DESCENT']
    height = ascent + descent
    if not name:
        name = family.lower().decode("utf-8") + str(height)

    font_glyphs = sorted(font.glyphs, key=lambda g: g.codepoint)
    bbs = [(g.advance, g.bbW, g.bbH, g.bbX, g.bbY) for g in font_glyphs]
    bitmaps = [glyph_to_bitmap(g) for g in font_glyphs]
    codepoints = [g.codepoint for g in font_glyphs]
    cp_runs = codepoints_to_runs(codepoints)
    cp_parts = dense_sparse(cp_runs, min_dense_run)
    return {
        'family': family,
        'name': name,
        'descent': descent,
        'height': height,
        'codepoints': codepoints,
        'bitmaps': bitmaps,
        'bbs': bbs,
        'cp_parts': cp_parts,
    }


def glyph_to_bitmap(glyph):
    w = glyph.bbW
    h = glyph.bbH
    total_bits = w * h
    total_bytes = (total_bits + 7) // 8
    result = [0] * total_bytes

    for (byte, bit), pixel in zip(
        ((byte, bit) for byte in range(total_bytes)
         for bit in range(7, -1, -1)),
        (px for row in glyph.iter_pixels() for px in row)):

        result[byte] |= pixel << bit

    return result


def dense_sparse(runs, min_dense_run):
    result = []
    curr_sparse_base = -1
    curr_sparse = []
    n = runs.shape[0]
    base = np.cumsum(np.concatenate(([1], (runs[:, 1]))))

    def add_sparse():
        nonlocal curr_sparse_base
        nonlocal curr_sparse
        if curr_sparse:
            result.append(
                (curr_sparse[0], curr_sparse[-1] - curr_sparse[0] + 1,
                 curr_sparse_base, curr_sparse))
            curr_sparse_base = -1
            curr_sparse = []

    for i in range(n):
        start, count = runs[i]
        if count >= min_dense_run:
            add_sparse()
            result.append((start, count, base[i], None))
        else:
            if curr_sparse_base < 0:
                curr_sparse_base = base[i]
            curr_sparse.extend(range(start, start + count))
    add_sparse()
    return result


def codepoints_to_runs(codepoints):
    # magic number only needs to be bigger than 1
    xs = np.array([0, *codepoints, codepoints[-1] + 2])
    jumps = (np.where(np.diff(xs) > 1)[0])
    return np.vstack((xs[jumps[:-1] + 1], np.diff(jumps))).T
