#ifndef COMMANDMANAGER_H
#define COMMANDMANAGER_H

UINT8 runInstructions()
{
	UINT8 comm, cond, inc;
	UINT8 funcN;
	UINT8 commN;
	UINT8 IP = 0;
	UINT8 blank[] = {0, 0};
	funcN = 0;
	commN = 0;
	stackInit(&retStack);
	while(1)
	{
		if(joypad()&J_B)
			return 1;
		inc = 1;
		funcN = IP/10;
		commN = IP%10;
		getDrawingPos(funcN, commN);
		move_sprite(1, 8 * functionColumn + 120, 8 * functionLines + 96); 
		switch(funcN)
		{
			case 0:
				cond = function1Cond[commN]; 
				comm = function1[commN];
				break;
			case 1:
				cond = function2Cond[commN]; 
				comm = function2[commN];
				break;
			case 2:
				cond = function3Cond[commN];
				comm = function3[commN];
				break;
			default:
				return 0;
		}
		if(levelMap[12 * pos.y + pos.x] == cond || (!cond))
		{
			delay(75);
			switch(comm)
			{
				case FWD:
					if(pos.dir == UP && pos.y == 0 || pos.dir == DOWN && pos.y==10 || pos.dir == LEFT && pos.x==0 || pos.dir == RIGHT && pos.x==11)
						return 1;
					if(pos.dir == UP)
						pos.y--;
					if(pos.dir == DOWN)
						pos.y++;
					if(pos.dir == LEFT)
						pos.x--;
					if(pos.dir == RIGHT)
						pos.x++;
					break;
				case TCW:
					pos.dir = ++pos.dir%4;
					break;
				case CCW:
					pos.dir = (pos.dir?--pos.dir:3);
					break;
				case RF1:
					stackPush(&retStack, IP);
					IP = 0;
					inc = 0;
					commN = 0;
					break;
				case RF2:
					stackPush(&retStack, IP);
					IP = 10;
					inc = 0;
					commN = 0;
					break;
				case RF3:
					stackPush(&retStack, IP);
					IP = 20;
					inc = 0;
					commN = 0;
					break;
				case PAI:
					levelMap[12 * pos.y + pos.x] = paintColor;
					set_bkg_tiles(1+pos.x, 3+pos.y, 1, 1, &tiles[paintColor]);
				default:
					break;
			}
			set_sprite_tile(0, pos.dir + 2);
			move_sprite(0, 8 * pos.x + 16, 8 * pos.y + 40);
			if(levelObjects[12 * pos.y + pos.x] > 1)
			{
				set_sprite_tile(levelObjects[12 * pos.y + pos.x], 0);
				move_sprite(levelObjects[12 * pos.y + pos.x], 0, 0);
				levelObjects[12 * pos.y + pos.x] = 0;
				objectives--;
				if(objectives == 0)
					{delay(500);return 0;}
			}
		}
		if(commN == functionLength[funcN])
		{
			set_bkg_tiles((retStack.stSize>18?18:retStack.stSize), 1, 1, 2, blank);
			IP = stackPop(&retStack);
			if(IP==255)
				return 1;
		}
		if(!levelMap[12 * pos.y + pos.x]) return 1;
		if(inc)
			IP++;
		for(i = 1; i <= (retStack.stSize>18?18:retStack.stSize); i++)
		{
			set_bkg_tiles(i, 1, 1, 1, &tiles[retStack.values[retStack.stSize-i] / 10 + 44]);
			set_bkg_tiles(i, 2, 1, 1, &tiles[retStack.values[retStack.stSize-i] % 10 + 48]);
		}
	}
}

void setCommand(UINT8 function, UINT8 commandNumber)
{
	UINT8 choice = 0;
	UINT8 selection = 0;
	UINT8 cont = 1;
	UINT8 cond = 0;
	UINT8 command = 0;
	set_bkg_tiles(15, 4, 1, 1, &tiles[19]);
	joyState = 0;
	//Calcutlating where to draw
	//MENU DISPLAY
	while(cont)
	{
		while(!joyState)
			joyState = joypad();
		if(joyState&J_A)
		{
			set_bkg_tiles(15 + 2 * selection, choice + 4, 1, 1, &tiles[0]);
			if(!selection)
				command = choice;
			if(selection)
				cond = choice;
			choice = 0;
			selection = !selection;
			cont = selection;
			if(cont)
				set_bkg_tiles(15 + 2 * selection, choice + 4, 1, 1, &tiles[19]);
		}
		else if(joyState&J_DOWN)
		{
			set_bkg_tiles(15 + 2 * selection, choice + 4, 1, 1, &tiles[0]);
			choice = ++choice % (selection?4:instructions);
			set_bkg_tiles(15 + 2 * selection, choice + 4, 1, 1, &tiles[19]);
		}
		else if(joyState&J_UP)
		{
			set_bkg_tiles(15 + 2 * selection, choice + 4, 1, 1, &tiles[0]);
			if(choice == 0)
				choice = (selection?4:instructions);
			choice--;
			set_bkg_tiles(15 + 2 * selection, choice + 4, 1, 1, &tiles[19]);
		} 
		else if(joyState&J_B) //exit
		{
			while(joyState)
				joyState = joypad();
			set_bkg_tiles(15 + 2 * selection, choice + 4, 1, 1, &tiles[0]);
			return;
		}
		while(joyState)
			joyState = joypad();
	}
	
	//If the choosen command is NOT painting
	if(!(command == paint && paint))
	{
		VBK_REG = 1;
		set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[2 * cond]);
		VBK_REG = 0;
		set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, (cond?&tiles[command + 34]:&tiles[command + 41]));
	} else { //If the choosen command is painting
		if(!cond)
		{
			VBK_REG = 1;
			set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[2 * paintColor]);
			VBK_REG = 0;
			set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[10]);
		} else if(cond == paintColor) {
			VBK_REG = 1;
			set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[1]);
			VBK_REG = 0;
			set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[paintColor]);
		} else {
			switch(cond)
			{
				case RED:
					if(paintColor == GRE) i = 2;
					if(paintColor == BLU) i = 3;
					break;
				case GRE:
					if(paintColor == RED) i = 4;
					if(paintColor == BLU) i = 5;
					break;
				case BLU:
					if(paintColor == RED) i = 6;
					if(paintColor == GRE) i = 7;
					break;
			}
			VBK_REG = 1;
			set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[i]);
			VBK_REG = 0;
			set_bkg_tiles(14 + functionColumn, 10 + functionLines, 1, 1, &tiles[40]);
		}
	}
	switch(function)
	{
		case 0:
			function1Cond[commandNumber] = cond;
			function1[commandNumber] = ((command == paint && paint)?PAI:command + 1);
			break;
		case 1:
			function2Cond[commandNumber] = cond;
			function2[commandNumber] = ((command == paint && paint)?PAI:command + 1);
			break;
		case 2:
			function3Cond[commandNumber] = cond;
			function3[commandNumber] = ((command == paint && paint)?PAI:command + 1);
			break;
	}
	move_sprite(1, 0, 0);
}

UINT8 selectCommands()
{
	UINT8 funcNumber = 0;
	UINT8 commNumber = 0;
	while(objectives)
	{
		while(joyState)
			joyState = joypad();
		getDrawingPos(funcNumber, commNumber);
		move_sprite(1, 8 * functionColumn + 120, 8 * functionLines + 96);
		while(!joyState)
			joyState = joypad();
		waitpadup();
		if(joyState&J_A)
			setCommand(funcNumber, commNumber);
		if(joyState&J_START)
			if(runInstructions()) return 1;
		if(joyState&J_UP)
		{
			if(funcNumber == 0 && functionLength[2])
				funcNumber = 2;
			else if(funcNumber == 0 && functionLength[1])
				funcNumber = 1;
			else if(funcNumber == 1)
				funcNumber = 0;
			else if(funcNumber == 2)
				funcNumber = 1;
			commNumber = 0;
		}
		if(joyState&J_DOWN)
		{
			if(functionLength[(funcNumber + 1)%3])
				funcNumber = ++funcNumber%3;
			else
				funcNumber = 0;
			commNumber = 0;
		}
		if(joyState&J_RIGHT)
			commNumber = ++commNumber % functionLength[funcNumber];
		if(joyState&J_LEFT)
		{
			if(commNumber == 0)
				commNumber = functionLength[funcNumber];
			commNumber = --commNumber % functionLength[funcNumber];
		}
		if(joyState&J_B)
		{
			for(i = 0; i<spriteCount; i++)
			{
				set_sprite_tile(i, 0);
				move_sprite(i, 0, 0);
			}
			return 0;
		}
	}
}

#endif
