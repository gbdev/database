# Third-party acknowledgements and notices

Created by dansciurus (Big D), with ChatGPT assistance.

Morse Boy was built with **GBDK-2020 4.5.0**, using its SDCC-based toolchain.
The ROM includes the GBDK Game Boy startup/runtime, APA graphics and text
support, joypad/timer/LCD helpers, standard memory/string/arithmetic routines,
and the bundled **IBM fixed bitmap font** (`f_ibm_full`). Large letters are
scaled from that same font; no separate large font is bundled.

The GBDK 4.5.0 licensing overview identifies the library as GPLv2 with a
linking exception. Its compiled-ROM guidance allows ROM-only distribution
without requiring game source disclosure through those library terms.
The installed SDCC license similarly describes runtime exceptions permitting
proprietary applications. These are library/toolchain terms, not a license
for the entire Morse Boy project.

The unchanged installed notices are included:

- [GBDK library license and linking exception](notices/GBDK-LIBRARY-LICENSE.txt)
- [SDCC licensing information](notices/SDCC-LICENSE.txt)

GBDK acknowledges drawing-library contributors including Pascal Felber,
Jon Fuge and Michael Hope. The linked division helper credits Michael Hope,
Sebastian 'basxto' Riedel and Philipp Klaus Krause. The font is identified by
its GBDK name; this does not assert IBM endorsement or independently settle
its earlier provenance.

The linked-component list contains no ZX0 decompressor, optional crash handler
or additional font. No compiler, emulator, emulator boot ROM, game ROM from
another title, input-interface driver or toolchain executable is distributed.

References:

- [GBDK 4.5.0 licensing overview](https://github.com/gbdk-2020/gbdk-2020/blob/4.5.0/LICENSE)
- [GBDK licensing FAQ](https://gbdk.org/docs/api/docs_faq.html)
- [GBDK IBM fixed-font source](https://github.com/gbdk-2020/gbdk-2020/blob/4.5.0/gbdk-lib/libc/targets/f_ibm_full.s)
- [GBDK project](https://github.com/gbdk-2020/gbdk-2020)
- [SDCC project](https://sdcc.sourceforge.net/)

Game Boy is a Nintendo product name. No Nintendo, IBM or other third-party
endorsement or affiliation is claimed. Morse Boy's approved noncommercial
sharing terms do not replace applicable third-party license terms. Preserve
these notices when sharing the approved unmodified ROM.
