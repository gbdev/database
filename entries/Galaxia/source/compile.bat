rgbasm -ogalaxia.obj galaxia.asm
xlink  -mgalaxia.map -ngalaxia.sym compile.lnk
rgbfix -v -p galaxia.gbc
