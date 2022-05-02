/*
    ***********************
    *******         *******
    ******* MazezaM *******
    *******         *******
    ***********************

      Copyright (C) 2002
       Malcolm  Tyrrell
      tyrrelmr@cs.tcd.ie

     Amiga Version (C) 2003
      Ventzislav  Tzvetkov
     drHirudo@Amigascne.org

     GameBoy version (C) 2004-2009
       Ventzislav  Tzvetkov
     drHirudo@Amigascne.org
     http://hirudov.com
     Compile with GBDK and
     following command line:

   lcc -Wl-yp0x143=0x80 MazezaM.c -o MazezaM.gb

     This code may be used
     and distributed under
     the terms of the GNU
     General Public Licence.

*/

#include <gb.h>
#include <drawing.h>
#include <string.h>
#include <rand.h>

int w,h,i,j,l,t,r,rx,lx,lives,GameBoyMode,Man;

char *a[20][20],b[20][20];


unsigned char Man_sprite[] = {

	/* Tile 0x00 */
	0x18,0x18,0x00,0x3C,0x00,0x3C,0x00,0x18,0x3C,0x00,0x18,0x42,0x3C,0x00,0x66,0x66,
	0x18,0x18,0x3C,0x3C,0x3C,0x3C,0x00,0x18,0x3C,0x00,0x18,0x42,0x3C,0x00,0x66,0x66,
	0x18,0x18,0x3C,0x3C,0x3C,0x3C,0x00,0x58,0x3C,0x00,0x1A,0x02,0x3E,0x02,0x60,0x60,
	0x18,0x18,0x3C,0x3C,0x3C,0x3C,0x00,0x1A,0x3C,0x00,0x58,0x40,0x7C,0x40,0x06,0x06,

	/* Tile 0x04 */
	0x18,0x18,0x20,0x3C,0x20,0x3C,0x00,0x18,0x1C,0x02,0x38,0x00,0x1C,0x40,0x36,0x36,
	0x18,0x18,0x20,0x3C,0x20,0x3C,0x00,0x18,0x18,0x00,0x18,0x04,0x3C,0x00,0x66,0x66,
	0x18,0x18,0x20,0x3C,0x20,0x3C,0x00,0x18,0x38,0x40,0x1C,0x00,0x38,0x02,0x6C,0x6C,
	0x18,0x18,0x00,0x3C,0x00,0x3C,0x00,0x18,0x3C,0x00,0x18,0x42,0x3E,0x06,0x60,0x60,

	/* Tile 0x08 */
	0x18,0x18,0x00,0x3C,0x00,0x3C,0x00,0x1A,0x3C,0x00,0x18,0x40,0x7C,0x40,0x06,0x06,
	0x18,0x18,0x00,0x3C,0x00,0x3C,0x00,0x58,0x3C,0x00,0x18,0x02,0x3E,0x02,0x60,0x60
};

UWORD background_palette[] = 
{ RGB(0,0,0), RGB(0x0A, 15, 0x06), RGB(0x09, 13, 0x1f), RGB(0x0f, 0x0f, 0x0f)}, black_palette[] = { RGB(0x0, 0x0, 0x0), RGB(0x00, 0x00, 0x00), RGB(0x00, 0x00, 0x00), RGB(0,
0,0)};

UWORD sprites_palette[] = 

{ RGB(0, 0, 0),RGB(0x1F, 12, 0),RGB(0x1F, 0x18, 0x18),RGB(0x1C, 0x1B, 0) };


void fadein(){
if (GameBoyMode==CGB_TYPE) set_bkg_palette(0,1,background_palette);
  else
{BGP_REG = 0x40U;delay(59); BGP_REG = 0x90U;delay(59); BGP_REG = OBP0_REG = 0xE4U;}}

void fadeout() {

if(GameBoyMode==CGB_TYPE) set_bkg_palette( 0, 1, black_palette); else 
{
 BGP_REG = OBP0_REG = OBP1_REG = 0x90U;
 delay(59); BGP_REG = OBP0_REG = OBP1_REG = 0x40U;
 delay(59);BGP_REG = OBP0_REG = OBP1_REG = 0x00U;}}

void Wait(){wait_vbl_done();wait_vbl_done();}

void Level(int mazenumber){int k;
char *n[20],*c[20];HIDE_SPRITES;move_sprite(0x00,0,0);
gotogxy(0,0);
switch (mazenumber)
   {
	case 1: n[0]="Humble Origins";c[0]="©Malcolm Tyrrell";w=7;h=2;
	lx=1;rx=1;a[1][0]=" Ä  Ä  ";a[2][0]=" Ä  ÅÉ ";
	break;


	case 2: n[0]="Easy Does It";c[0]="©Malcolm Tyrrell";w=8;h=3;
	lx=3;rx=2;a[1][0]="  Ä  ÅÇÉ";a[2][0]="  Ä Ä Ä ";
	a[3][0]=" Ä Ä Ä  ";break;

	case 3: n[0]="Up, Up and Away";c[0]="©Malcolm Tyrrell";w=5;h=11;
	lx=11;rx=1;a[1][0]="  Ä  ";a[2][0]=" Ä ÅÉ";a[3][0]=" ÅÉ  ";
	a[4][0]="Ä Ä  ";a[5][0]=" Ä Ä ";a[6][0]=" ÅÇÉ ";a[7][0]="Ä Ä  ";
	a[8][0]=" Ä Ä ";a[9][0]=" Ä Ä ";a[10][0]="Ä ÅÉ ";a[11][0]=" Ä   ";break;

	case 4: n[0]="To and Fro";c[0]="©Malcolm Tyrrell";w=13;h=6;lx=1;rx=1;
	a[1][0]="   ÅÇÇÇÉ     ";a[2][0]="Ä ÅÇÇÇÉ  ÅÇÉ ";a[3][0]=" Ä ÅÇÉ ÅÇÇÉ  ";
	a[4][0]="Ä Ä  ÅÇÇÇÇÇÉ ";a[5][0]=" ÅÇÉ Ä   ÅÉ  ";a[6][0]="Ä Ä Ä ÅÉ  Ä  ";
	break;

	case 5: n[0]="Loop-de-Loop";c[0]="©Malcolm Tyrrell";w=14;h=4;lx=2;rx=4;
	a[1][0]=" ÅÇÇÇÉ ÅÉ ÅÉ  ";a[2][0]="   ÅÉ  ÅÉ  ÅÉ ";
	a[3][0]="ÅÉ  Ä ÅÉ ÅÇÉ  ";a[4][0]="   ÅÇÇÇÇÇÇÉ  Ä";break;


	case 6:
		n[0]="Little  Harder";w=5;h=4;lx=2;rx=1;
		a[1][0]=" Ä Ä ";
		a[2][0]="  Ä Ä";
		a[3][0]=" Ä   ";
		a[4][0]=" ÅÉ Ä";
		break;

	case 7:
		n[0]="Somehow Easy";w=5;h=rx=3;lx=1;
		a[1][0]="  ÅÉ ";
		a[2][0]=" Ä   ";
		a[3][0]=" Ä ÅÉ";
		break;

	case 8: n[0]="Be Prepared";c[0]="©Malcolm Tyrrell";w=7;h=6;lx=5;rx=3;
	a[1][0]="   Ä   ";a[2][0]=" ÅÇÇÉ  ";a[3][0]=" ÅÇÉ ÅÉ";
	a[4][0]=" Ä Ä Ä ";a[5][0]=" Ä ÅÉ  ";a[6][0]="Ä ÅÉ   ";
	break;

	case 9: n[0]="Two Front Doors";c[0]="©Malcolm Tyrrell";
	w=16;h=7;lx=1;rx=7;a[1][0]="       ÅÇÇÇÇÇÉ  ";
	a[2][0]="  ÅÇÇÉ ÅÇÇÉ Ä Ä ";a[3][0]="ÅÉ ÅÉ ÅÇÇÇÇÉ Ä Ä";
	a[4][0]="ÅÉ     Ä Ä      ";a[5][0]="  ÅÇÇÇÇÇÇÇÇÇÇÇÉ ";
	a[6][0]=" Ä ÅÉ    Ä ÅÇÉ  ";a[7][0]="  Ä   ÅÇÉ     ÅÉ";
	break;

	case 10: n[0]="Through, through";
	c[0]="©Malcolm Tyrrell";w=15;h=4;lx=3;rx=1;
	a[1][0]=" ÅÇÇÉ  ÅÇÇÉ  ÅÉ";a[2][0]=" Ä ÅÉ ÅÉ Ä ÅÉ  ";
	a[3][0]=" Ä ÅÉ ÅÇÇÉ ÅÉ  ";a[4][0]=" Ä ÅÉ  ÅÇÇÉ  Ä ";
	break;

	case 11: n[0]="Double Cross";c[0]="©Malcolm Tyrrell";w=9;h=7;lx=7;rx=3;
	a[1][0]=" Ä  ÅÇÇÉ ";a[2][0]=" Ä  Ä ÅÉ ";a[3][0]=" Ä ÅÇÇÉ Ä";
	a[4][0]="Ä ÅÉ  Ä  ";a[5][0]="  Ä   ÅÇÉ";a[6][0]=" ÅÇÇÇÇÉ  ";
	a[7][0]="  Ä      ";
	break;

	case 12: n[0]="Inside Out";c[0]="©Malcolm Tyrrell";w=14;h=10;lx=8;rx=1;
	a[1][0]="            Ä ";a[2][0]=" ÅÇÇÇÇÇÇÇÇÉ  Ä";
	a[3][0]=" ÅÇÉ       ÅÉ ";a[4][0]=" Ä ÅÇÇÇÇÇÇÉ Ä ";
	a[5][0]=" ÅÇÉ ÅÇÉ  ÅÇÉ ";a[6][0]=" ÅÇÉ   Ä  ÅÇÉ ";
	a[7][0]=" Ä ÅÇÇÇÇÇÉ ÅÉ ";a[8][0]=" Ä Ä Ä    ÅÇÉ ";
	a[9][0]=" ÅÇÇÇÇÇÇÇÇÇÇÉ ";a[10][0]="              ";
	break;

	case 13: n[0]="Hidden  corridor";w=12;h=10;lx=4;rx=1;
	a[1][0]= " ÅÉ Ä Ä ÅÇÉ ";
	a[2][0]= " Ä   ÅÉ   Ä ";
	a[3][0]= "  ÅÉ  Ä  ÅÉ ";
	a[4][0]= " ÅÇÇÇÇÇÇÉ   ";
	a[5][0]= " Ä    Ä ÅÉ  ";
	a[6][0]= "Ä ÅÉ Ä Ä Ä  ";
	a[7][0]= " ÅÇÇÇÇÇÉ Ä Ä";
	a[8][0]= "  ÅÇÇÇÇÉ Ä  ";
	a[9][0]= " Ä Ä Ä Ä ÅÉ ";
	a[10][0]="Ä Ä Ä Ä Ä   ";
	break;




   default: {fadeout();color(BLACK,WHITE,SOLID);gprint("  ÑÑ                ÑÑÑÑ                ÑÑÑÑ");
   color(LTGREY,WHITE,SOLID);gprint("      You have  ");color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ");
   color(LTGREY,WHITE,SOLID);gprint("      Escaped.  ");color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ     ");
   color(DKGREY,BLACK,SOLID);gprint("WELL DONE!");color(BLACK,WHITE,SOLID);
   gprint(" ÑÑÑÑ                ÑÑÑÑ                ÑÑÑÑ                ÑÑÑÑ                ____                ÑÑÑÑ");
   color(DKGREY,WHITE,SOLID);gprint("ÅÇÉ");color(BLACK,LTGREY,SOLID);
   gprint("ááááááááááááá");color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ   ");
   color(BLACK,LTGREY,SOLID);gprint("ááááááááááááá");
   for (i=0;i<6;i++)
  {color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ");color(DKGREY,WHITE,SOLID);gprint("ÜÜÜ");
   color(BLACK,LTGREY,SOLID);gprint("ááááááááááááá");}
   fadein();
color(BLACK,DKGREY,SOLID);
set_sprite_prop(0,S_PRIORITY);Man=5;t=88;SHOW_SPRITES;
   for (k=0;k!=21;k++) {
for (l=0;l!=8;l++) {
if (++Man==7) Man=4;set_sprite_tile(0,Man);
move_sprite(0x00,k*8+l,t);Wait();

   if (k >= 14 && k <= 15) t--;
   if (k == 16) t+=2;
   if (k == 15) {gotogxy(12,5);gprint("Hurray!");}
   if (k == 17) {color(WHITE,WHITE,SOLID);gotogxy(12,5);gprint("       ");t=88;}
  }}
  delay(8200);fadeout();reset();}
 }
for (i=1;i<h+1;i++) strcpy(&b[i][0],a[i][0]);
l=((20-w)/2);t=((20-h)/2);r=20-l-w;color(BLACK,WHITE,SOLID);
gprint("ÑÑ");color(DKGREY,WHITE,SOLID);
gprint("Level ");if (mazenumber<10) gprintf("0%d",mazenumber);
                   else gprintf("%d",mazenumber);
color(BLACK,WHITE,SOLID); gprint("Ñ");color(LTGREY,WHITE,SOLID);
gprint("Lives ");gprintf("%d",lives);
color(BLACK,WHITE,SOLID);gprint("ÑÑ");

for (i=1;i<t+1;i++) gprint("ÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑ");

for (i=1;i<h+1;i++){
if (i==lx) for (k=0;k<l;k++) gprint("_");
if (i!=lx) for (k=0;k<l;k++) gprint("Ñ");
color(i%2+1,WHITE,SOLID);gprint(a[i][0]);
color(BLACK,WHITE,SOLID);
if (i==rx) for (k=0;k<r;k++) gprint("_");
if (i!=rx) for (k=0;k<r;k++) gprint("Ñ");
}

for (i=t+h+1;i<17;i++) gprint("ÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑ");

j=strlen(n[0]);
if (!j) gprint("ÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑ"); else 
   {for (k=0;k<((18-j)/2);k++) gprint("Ñ");
   gprint(" ");color(LTGREY,WHITE,SOLID);gprint(n[0]);gprint(" ");color(BLACK,WHITE,SOLID);for (k=0;k<((18-j)/2);k++) gprint("Ñ");}

set_sprite_prop(0,S_PRIORITY);
Man=4;
SHOW_SPRITES;
for (i=0;i!=(l+1)*8+1;i++){if (++Man==7) Man=4;
set_sprite_tile(0,Man);
move_sprite(0x00,i,(((t+lx))*8)+16);
Wait();}
gotogxy((i/8)-2,t+lx);gprint("Ö");
set_sprite_tile(0,0);
i=lx;j=1;

}

void Title(){
int i;
HIDE_SPRITES;
DISPLAY_ON;
mode (M_TEXT_OUT);
gotogxy(0,0);
color(BLACK,WHITE,SOLID);
gprint("ÑÑ       ÑÑ       ÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑ    ");
color(LTGREY,WHITE,SOLID);gprint("MazezaM");color(BLACK,WHITE,SOLID);
gprint("     ÑÑÑÑ                ÑÑÑÑ");color(DKGREY,WHITE,SOLID);gprint("Puzzle game-push");
color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ block to reach ÑÑÑÑ");color(DKGREY,WHITE,SOLID);gprint(" exit  of level ");
color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ                ÑÑÑÑ                ÑÑÑÑ");color(LTGREY,WHITE,SOLID);
gprint("GamebΩy  2004-09");
color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ                ÑÑÑÑ");color(LTGREY,WHITE,SOLID);gprint("   by drHirudo  ");
color(BLACK,WHITE,SOLID);gprint("ÑÑÑÑ                ÑÑÑÑ");
gprint("ÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑ                    Press START to play");fadein();for (;;) { if (joypad() & J_START) break;
i++;
}
initrand(i);
}

void sound2(long freq1,long freq2)
{
NR52_REG = 128; /* make sure sound is enabled */
NR51_REG = 255; /* send sound to left and rignt */

NR10_REG = 127;

NR11_REG = NR21_REG = 0;
NR12_REG = 242;
NR13_REG = freq1 & 0x00FF;
NR14_REG = freq1 >>8;

NR22_REG = 34;
NR23_REG = freq2 & 0x00FF;
NR24_REG = freq2 >>8;
}

void main() {
int mazeno,ModeID,direction,count;

char Txt[20];move_bkg(0,0);

BGP_REG = OBP0_REG = OBP1_REG = GameBoyMode = 0x00U;

if(_cpu==CGB_TYPE) {    // Color gameboy detected
  /* Transfer color palette */
  set_bkg_palette( 0, 1, background_palette );
  set_sprite_palette( 0, 1, sprites_palette );GameBoyMode=CGB_TYPE;}
SPRITES_8x8;SHOW_BKG;DISPLAY_ON;HIDE_WIN;HIDE_SPRITES;
disable_interrupts();
						   http://hirudov.com
gotogxy(0,6);color (DKGREY,LTGREY,SOLID);gprint (" http://hirudov.com ");
SHOW_BKG;fadein();
sound2(1930,1949);
delay(3200);fadeout();


set_sprite_data(0x00, 10, Man_sprite);
set_sprite_tile (0x00, Man=0x00);

mazeno=1;lives=3;

BGP_REG = OBP0_REG = OBP1_REG = 0x00U;
SHOW_BKG;
Title();Level(mazeno);

for(;;){

direction=joypad();

if (direction==J_SELECT) {lives--;set_sprite_prop(0,S_FLIPY|S_PRIORITY);if (lives>0){
       color(BLACK,DKGREY,SOLID);gotogxy(l+j-3,t+i-1);gprint("ARGH!");delay(1500);
          Level(mazeno);} else
{Wait();color(LTGREY,WHITE,SOLID);gotogxy(17,0);
gprint("0");gotogxy(5,8);color(BLACK,LTGREY,SOLID);gprint("GAME OVER!");Delay(4200);fadeout();reset();}
}

if (direction == (J_START|J_SELECT|J_A)) Level(++mazeno); /* {BGP_REG = 0x00U;reset();} */

if ((direction & J_RIGHT) && (i==rx && j==w)) {
set_sprite_prop(0,S_PRIORITY);Man=5;
for (ModeID=l+w;ModeID<20;ModeID++)
for (count=0;count!=8;count++) {
if (++Man==7) Man=4;set_sprite_tile(0,Man);
move_sprite(0x00,ModeID*8+count,((t+i)*8)+16);Wait();}
color(LTGREY,WHITE,SOLID);t--;
switch (rand()%6)
{
case 0: {gotogxy(13,t+rx);gprint("Hurray!");break;}

case 1: {gotogxy(13,t+rx);gprint("Hurrah!");break;}

case 2: {gotogxy(16,t+rx);gprint("Yes!");break;}

case 3: {gotogxy(14,t+rx);gprint("Great!");break;}

case 4: {gotogxy(12,t+rx);gprint("Yee-hah!");break;}

default:{gotogxy(16,t+rx);gprint("Yay!");}
   }
Delay(799);t++;
for (count=0;count!=8;count++) {
if (++Man==7) Man=4;set_sprite_tile(0,Man);
move_sprite(0x00,ModeID*8+count,((t+i)*8)+16);Wait();}
lives+=(lives<9);Level(++mazeno);
 direction=0;}

if ((direction & J_RIGHT) && j<w) if (b[i][j]==' '){set_sprite_prop(0,S_PRIORITY);
Man=5;
for (count=0;count!=8;count++) {
if (++Man==7) Man=4;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);Wait();}
set_sprite_tile(0,0);move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);
j++;} else

if (b[i][w-1]==' ') {set_sprite_prop(0,S_PRIORITY);
for (ModeID=w-1;ModeID>0;ModeID--) b[i][ModeID]=b[i][ModeID-1];
b[i][0]=' ';b[i][w]=0;

Man=5;
for (count=0;count!=4;count++) {
if (++Man==7) Man=4;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);Wait();}

gotogxy(l,t+i); color ((i%2)+1,WHITE,SOLID);gprint(&b[i][0]);

for (count=4;count!=8;count++) {
if (++Man==7) Man=4;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);Wait();}

set_sprite_tile(0,0);move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);j++;

}

if ((direction & J_LEFT) && j>1) if (b[i][j-2]==' '){
set_sprite_prop(0,S_FLIPX|S_PRIORITY);Man=5;
for (count=8;count!=0;count--) {
if (++Man==7) Man=4;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j-1)*8+count,((t+i)*8)+16);Wait();}
set_sprite_tile(0,0);move_sprite(0x00,(l+j-1)*8+count,((t+i)*8)+16);
j--;} else

if (b[i][0]==' ') {j--;set_sprite_prop(0,S_FLIPX|S_PRIORITY);
for (ModeID=1;ModeID<w;ModeID++) b[i][ModeID-1]=b[i][ModeID];
b[i][w-1]=' ';
for (count=0;count<w+1;count++) Txt[count]=b[i][count];

Man=5;

for (count=8;count!=4;count--) {if (++Man==7) Man=4;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);Wait();}

gotogxy(l,t+i); color ((i%2)+1,WHITE,SOLID);gprint(&b[i][0]);

for (count=4;count!=0;count--) {if (++Man==7) Man=4;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);Wait();}

set_sprite_tile(0,0);move_sprite(0x00,(l+j)*8+count,((t+i)*8)+16);

}

if ((direction & J_DOWN) && i<h) if (b[i+1][j-1]==' '){
Man=7;
for (count=0;count!=8;count++) {
if (++Man==10) Man=7;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j)*8,((t+i)*8)+16+count);Wait();}
set_sprite_tile(0,0);move_sprite(0x00,(l+j)*8,((t+i)*8)+16+count);
i++;}

if ((direction & J_UP) && i>1) if (b[i-1][j-1]==' '){
Man=2;
for (count=8;count!=0;count--) {
if (++Man==4) Man=1;
set_sprite_tile(0,Man);
move_sprite(0x00,(l+j)*8,((t+i)*8)+8+count);Wait();}
set_sprite_tile(0,0);move_sprite(0x00,(l+j)*8,((t+i)*8)+8+count);
i--;}

direction=0;
}

}
