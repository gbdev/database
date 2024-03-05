#ifndef CONSTANTS_H
#define CONSTANTS_H
#include <gb/gb.h>
#include <gb/cgb.h>
#include <stdio.h>
#include <time.h>
#include "turtleTiles.h"
#include "turtleSprites.h"
#include "palettes.h"
#include "gameMap.h"
#include "gameMapPalette.h"
#include "bin.h"
#include "cgbOnlyTiles.h"
#include "cgbOnlyMap.h"
#include "titleScreen.h"
#include "titleScreenPalette.h"
#include "credits.h"
#include "creditsPalette.h"
#include "stack.h"


#define NOPAINT 0
#define PAINT 7

#define NOP BIN_00000000
#define FWD BIN_00000001
#define TCW BIN_00000010
#define CCW BIN_00000011
#define RF1 BIN_00000100
#define RF2 BIN_00000101
#define RF3 BIN_00000110
#define PAI BIN_00000111

#define RED BIN_00000001
#define GRE BIN_00000010
#define BLU BIN_00000011

typedef struct
{
	UINT8 x;
	UINT8 y;
	UINT8 dir;
} POSITION;

enum DIRECTION {UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3};

#endif
