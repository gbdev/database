#include "constants.h"

UINT8 function1[10];
UINT8 function2[10];
UINT8 function3[10];
UINT8 function1Cond[10];
UINT8 function2Cond[10];
UINT8 function3Cond[10];
UINT8 OMGWTFBBQ;//Doesn't work if there is not a var here (F1 length would stay at 0) O_o
UINT8 functionLength[3];
UINT8 tiles[57];
UINT8 levelMap[132];
UINT8 levelObjects[132];
UINT8 i, j, functionLines, functionColumn, spriteCount, paint, paintColor, instructions, currentMode, objectives, speed;
INT8 currentLevel;
POSITION pos;
STACK retStack;
UINT8 joyState = 0;

#include "levelManager.h"
#include "commandManager.h"

void main()
{
	objectives = 1;
	if(_cpu == 0x11)
	{
		for(i = 0;i < 57; i++)
			tiles[i] = i;
		set_bkg_palette(0, 8, &turtleTilesPalette[0]);
		set_sprite_palette(0,5,&turtleSpritesPalette[0]);
		SPRITES_8x8;
		set_sprite_data(0, 8, turtleSprites);
		//objectives = 1;
		currentLevel = 0;
		speed = 3;
		while(1)
		{
			joyState = 0;
			waitpadup();
			set_sprite_tile(0, 0);
			move_sprite(0, 0, 0);
			set_sprite_tile(1, 0);
			move_sprite(1, 0, 0);
			currentLevel = dispTitleScreen();
			DISPLAY_OFF;
			set_bkg_data(0, 57, &turtleTiles[0]);
			DISPLAY_ON;
			loadLevel(currentLevel,1);
			while(selectCommands())
				loadLevel(currentLevel,0);
			currentLevel = ++currentLevel%(LEVEL_MAX+1);
		}
	} else {
		set_bkg_data(0, 36, &cgbOnlyTiles[0]);
		set_bkg_tiles(0, 0, 20, 18, &cgbOnlyMap[0]);
		SHOW_BKG;
	}
}
