#ifndef LEVELMANAGER_H
#define LEVELMANAGER_H

#define LEVEL_MAX 23

#include "levels/level000.h"
#include "levels/level000_Objects.h"
#include "levels/level001.h"
#include "levels/level001_Objects.h"
#include "levels/level002.h"
#include "levels/level002_Objects.h"
#include "levels/level003.h"
#include "levels/level003_Objects.h"
#include "levels/level004.h"
#include "levels/level004_Objects.h"
#include "levels/level005.h"
#include "levels/level005_Objects.h"
#include "levels/level006.h"
#include "levels/level006_Objects.h"
#include "levels/level007.h"
#include "levels/level007_Objects.h"
#include "levels/level008.h"
#include "levels/level008_Objects.h"
#include "levels/level009.h"
#include "levels/level009_Objects.h"
#include "levels/level010.h"
#include "levels/level010_Objects.h"
#include "levels/level011.h"
#include "levels/level011_Objects.h"
#include "levels/level012.h"
#include "levels/level012_Objects.h"
#include "levels/level013.h"
#include "levels/level013_Objects.h"
#include "levels/level014.h"
#include "levels/level014_Objects.h"
#include "levels/level015.h"
#include "levels/level015_Objects.h"
#include "levels/level016.h"
#include "levels/level016_Objects.h"
#include "levels/level017.h"
#include "levels/level017_Objects.h"
#include "levels/level018.h"
#include "levels/level018_Objects.h"
#include "levels/level019.h"
#include "levels/level019_Objects.h"
#include "levels/level020.h"
#include "levels/level020_Objects.h"
#include "levels/level021.h"
#include "levels/level021_Objects.h"
#include "levels/level022.h"
#include "levels/level022_Objects.h"
#include "levels/level023.h"
#include "levels/level023_Objects.h"


void initGameMap(UINT8 *level, UINT8 *objects, UINT8 p, UINT8 pC, UINT8 reset);

void loadLevel(UINT8 levelNumber, UINT8 reset)
{
	switch(levelNumber)
	{
		case 0:
			functionLength[0] = 2;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level000, levelObjects000, NOPAINT, NOPAINT, reset);
			break;
		case 1:
			functionLength[0] = 3;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level001, levelObjects001, NOPAINT, NOPAINT, reset);
			break;
		case 2:
			functionLength[0] = 4;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level002, levelObjects002, NOPAINT,  NOPAINT, reset);
			break;
		case 3:
			functionLength[0] = 5;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level003, levelObjects003, NOPAINT,  NOPAINT, reset);
			break;
		case 4:
			functionLength[0] = 4;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level004, levelObjects004, NOPAINT, NOPAINT, reset);
			break;
		case 5:
			functionLength[0] = 4;
			functionLength[1] = 2;
			functionLength[2] = 2;
			initGameMap(level005, levelObjects005, NOPAINT, NOPAINT, reset);
			break;
		case 6:
			functionLength[0] = 7;
			functionLength[1] = 2;
			functionLength[2] = 0;
			initGameMap(level006, levelObjects006, NOPAINT, NOPAINT, reset);
			break;
		case 7:
			functionLength[0] = 2;
			functionLength[1] = 5;
			functionLength[2] = 0;
			initGameMap(level007, levelObjects007, PAINT, RED, reset);
			break;
		case 8:
			functionLength[0] = 4;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level008, levelObjects008, NOPAINT, NOPAINT, reset);
			break;
		case 9:
			functionLength[0] = 4;
			functionLength[1] = 2;
			functionLength[2] = 0;
			initGameMap(level009, levelObjects009, NOPAINT, NOPAINT, reset);
			break;
		case 10:
			functionLength[0] = 7;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level010, levelObjects010, NOPAINT, NOPAINT, reset);
			break;
		case 11:
			functionLength[0] = 7;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level011, levelObjects011, PAINT, RED, reset);
			break;
		case 12:
			functionLength[0] = 5;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level012, levelObjects012, PAINT, BLU, reset);
			break;
		case 13:
			functionLength[0] = 5;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level013, levelObjects013, NOPAINT, NOPAINT, reset);
			break;
		case 14:
			functionLength[0] = 4;
			functionLength[1] = 4;
			functionLength[2] = 0;
			initGameMap(level014, levelObjects014, NOPAINT, NOPAINT, reset);
			break;
		case 15:
			functionLength[0] = 6;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level015, levelObjects015, NOPAINT, NOPAINT, reset);
			break;
		case 16:
			functionLength[0] = 5;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level016, levelObjects016, NOPAINT, NOPAINT, reset);
			break;
		case 17:
			functionLength[0] = 9;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level017, levelObjects017, NOPAINT, NOPAINT, reset);
			break;
		case 18:
			functionLength[0] = 7;
			functionLength[1] = 7;
			functionLength[2] = 0;
			initGameMap(level018, levelObjects018, NOPAINT, NOPAINT, reset);
			break;
		case 19:
			functionLength[0] = 4;
			functionLength[1] = 4;
			functionLength[2] = 0;
			initGameMap(level019, levelObjects019, NOPAINT, NOPAINT, reset);
			break;
		case 20:
			functionLength[0] = 6;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level020, levelObjects020, NOPAINT, NOPAINT, reset);
			break;
		case 21:
			functionLength[0] = 5;
			functionLength[1] = 5;
			functionLength[2] = 5;
			initGameMap(level021, levelObjects021, NOPAINT, NOPAINT, reset);
			break;
		case 22:
			functionLength[0] = 6;
			functionLength[1] = 0;
			functionLength[2] = 0;
			initGameMap(level022, levelObjects022, NOPAINT, NOPAINT, reset);
			break;
		case 23:
			functionLength[0] = 3;
			functionLength[1] = 3;
			functionLength[2] = 2;
			initGameMap(level023, levelObjects023, PAINT, RED, reset);
			break;
		default:
			return;
	}
	currentMode = 0;
}

void getDrawingPos(UINT8 function, UINT8 commandNumber)
{
	switch(function)
	{
		case 0:
			functionLines = (commandNumber + 1)/6 + 1;
			break;
		case 1:
			functionLines = ((functionLength[0] + 1) / 6 +1) + (commandNumber + 1)/6 + 1 - (functionLength[0] == 5?1:0);
			break;
		case 2:
			functionLines = ((functionLength[0] + 1) / 6 +1) + ((functionLength[1] + 1) / 6 +1) + (commandNumber + 1)/6 + 1 - (functionLength[0] == 5?1:0) - (functionLength[1] == 5?1:0);
			break;
	}
	functionColumn = (commandNumber + 1)%6;
}

void initGameMap(UINT8 *level, UINT8 *objects, UINT8 p, UINT8 pC, UINT8 reset)
{
	UINT8 blank[] = {0, 0};
	DISPLAY_OFF;
	paint = 0;
	paintColor = pC;
	functionLines = 0;
	functionColumn = 0;
	objectives = 0;
	speed = 0;
	stackInit(&retStack);
	pos.x = 0;
	pos.y = 0;
	if(reset)
	{
		for(i = 0; i < 10; i++)
			function1[i] = 0; function1Cond[i] = 0; function2[i] = 0; function2Cond[i] = 0; function3[i] = 0; function3Cond[i] = 0;
		VBK_REG = 1;
		set_bkg_tiles(0, 0, 20, 18, gameMapPalette);
		VBK_REG = 0;
		set_bkg_tiles(0, 0, 20, 18, gameMap);
		instructions = 3;
		for(i = 0; i < 3; i++)
		{
			if(functionLength[i])
			{
				instructions++;
				set_bkg_tiles(16, 3 + instructions, 1, 1, &tiles[44 + i]);
				functionColumn = 1;
				functionLines++;
				set_bkg_tiles(14, 10 + functionLines, 1, 1, &tiles[29 + i]);
				for(j = 0; j < functionLength[i]; j++)
				{
					if(functionColumn == 6)
					{
						functionColumn = 0;
						functionLines++;
					}
					set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[32]);
					functionColumn++;
				}
			}
		}
	} else {
		for(i = 1; i<20; i++)
			set_bkg_tiles(i, 1, 1, 2, blank);
	}
	set_bkg_tiles(1, 3, 12, 11, level);
	
	//SPRITES init
	for(i = 0; i < spriteCount; i++)
	{
		set_sprite_tile(i, 0);
		set_sprite_prop(i, 0);
		move_sprite(i, 0, 0);
	}	
	spriteCount = 2;
	set_sprite_tile(1, 7);
	for(i = 0; i < 132; i++)
		levelObjects[i] = 0;
	for(i = 0; i < 11; i++) {
		for(j = 0; j < 12; j++)
		{
			if(objects[12 * i + j] > 1 && objects[12 * i + j] < 6)
			{
				pos.dir = objects[12 * i + j] - 2;
				set_sprite_tile(0, objects[12 * i + j]);
				set_sprite_prop(0, 0);
				move_sprite(0, 8 * j + 16, 8 * i + 40);
				levelObjects[12 * i + j] = 0;
				pos.y = i;
				pos.x = j;
			} else if(objects[12 * i + j]){
				set_sprite_tile(spriteCount, 1);
				set_sprite_prop(spriteCount, 0);
				move_sprite(spriteCount, 8 * j + 16, 8 * i + 40);
				levelObjects[12 * i + j] = spriteCount;
				objectives++;
				spriteCount++;
			}
		}
	}
	for(i = 0; i < 132; i++)
		levelMap[i] = level[i];
			
	if(p)
	{
		paint = instructions;
		instructions++;
		VBK_REG = 1;
		set_bkg_tiles(16, 3 + instructions, 1, 1, &tiles[2*paintColor]);
		VBK_REG = 0;
		set_bkg_tiles(16, 3 + instructions, 1, 1, &tiles[10]);
	}
	SHOW_SPRITES;
	SHOW_BKG;
	DISPLAY_ON;
}

UINT8 dispTitleScreen()
{
	UINT8 choice = 0;
	UINT8 lvl = currentLevel;
	UINT8 cont = 1;
	
	DISPLAY_OFF;
	set_bkg_data(0, 58, &cgbOnlyTiles[0]);
	VBK_REG = 1;
	set_bkg_tiles(0, 0, 20, 18, &titleScreenPalette[0]);
	VBK_REG = 0;
	set_bkg_tiles(0, 0, 20, 18, &titleScreen[0]);
	set_bkg_tiles(16, 5, 1, 1, &tiles[lvl/100 + 37]);
	set_bkg_tiles(17, 5, 1, 1, &tiles[(lvl%100)/10 + 37]);
	set_bkg_tiles(18, 5, 1, 1, &tiles[lvl%10 + 37]);
	DISPLAY_ON;
	
	while(cont)
	{
		while(!joyState)
			joyState = joypad();
		if(!choice)
		{
			if(joyState&J_UP || joyState&J_DOWN)
			{
				set_bkg_tiles(1, 5, 1, 1, &tiles[52]);
				set_bkg_tiles(1, 7, 1, 1, &tiles[55]);
				choice = 1;
			}
			if(joyState&J_LEFT)
			{
				lvl = (lvl==0?LEVEL_MAX:--lvl);
			}
			if(joyState&J_RIGHT)
			{
				lvl = ++lvl%(LEVEL_MAX+1);
			}
			if(joyState&J_START || joyState&J_A)
				cont = 0;
			set_bkg_tiles(16, 5, 1, 1, &tiles[lvl/100 + 37]);
			set_bkg_tiles(17, 5, 1, 1, &tiles[(lvl%100)/10 + 37]);
			set_bkg_tiles(18, 5, 1, 1, &tiles[lvl%10 + 37]);
		} else {
			if(joyState&J_UP || joyState&J_DOWN)
			{
				set_bkg_tiles(1, 5, 1, 1, &tiles[53]);
				set_bkg_tiles(1, 7, 1, 1, &tiles[54]);
				choice = 0;
			}
			if(joyState&J_START || joyState&J_A)
			{
				VBK_REG = 1;
				set_bkg_tiles(0, 0, 20, 18, &creditsPalette[0]);
				VBK_REG = 0;
				set_bkg_tiles(0, 0, 20, 18, &credits[0]);
				while(joyState)
					joyState = joypad();
				while(!(joyState&J_START || joyState&J_A))
					joyState = joypad();
				DISPLAY_OFF;
				set_bkg_data(0, 58, &cgbOnlyTiles[0]);
				VBK_REG = 1;
				set_bkg_tiles(0, 0, 20, 18, &titleScreenPalette[0]);
				VBK_REG = 0;
				set_bkg_tiles(0, 0, 20, 18, &titleScreen[0]);
				DISPLAY_ON;
				choice = 0;
				set_bkg_tiles(16, 5, 1, 1, &tiles[lvl/100 + 37]);
				set_bkg_tiles(17, 5, 1, 1, &tiles[(lvl%100)/10 + 37]);
				set_bkg_tiles(18, 5, 1, 1, &tiles[lvl%10 + 37]);
			}
		}
		while(joyState)
			joyState = joypad();
	}
	return lvl;
}

#endif
