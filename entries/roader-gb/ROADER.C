/* Roader GB (c) 1998 Jay Cook    jaycook1@juno.com     http://members.tripod.com/~ziel 
 -How road is read is sort of messed up, read in reverse(if reading all road tiles at once)
   an easy fix I am sure, but I don't want to mess with it
 -If your speed is greater than 8, the game can't catch up and collision is left a few steps behind. Easy fix tho
 -Need to add some kind of variety to track so it isn't the same back and forth
*/
#include <gb.h>
#include <console.h>
unsigned int scorea,scoreb,scorec,scored,hisa,hisb,hisc,hisd;
unsigned int x,y,mx,my,mxx,myy,score,hiscore;
unsigned int roadinfox [68], roadinfoy [68];
int rx,ry,maxx,rxa,tr,rd,test,rda,jr,rdb,ia;
int sprt,sprta,i,j,speed,starta,c,fone,rdln,cnt,rdc;
int tra,trb,trc,trd,tre,taa,menu,startb,testa;
/* Graphics */
unsigned char jcar[] =
{
  0x00,0x3C,0xDF,0xE3,0xDD,0xFB,0x3C,0x7E,
  0x7E,0x42,0x9D,0xE3,0xDF,0xFB,0xDB,0xFF,
  0x00,0x3C,0xDF,0xE3,0xDF,0xFB,0x3C,0x7E,
  0x7E,0x42,0x9D,0xE3,0xDF,0xFB,0xDF,0xFB
};
unsigned char land[]=
{
  0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,
  0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,
  0x7D,0x00,0xDF,0x00,0xFB,0x00,0xBF,0x00,
  0xEE,0x00,0xFB,0x00,0x7F,0x00,0xF7,0x00,
  0xDD,0x22,0x77,0x88,0xDD,0x22,0xBE,0x41,
  0x57,0xA8,0xEE,0x11,0xD5,0x2A,0xBA,0x45
};

unsigned char roada[] ={ 1 };
unsigned char roadb[] ={ 2 };
unsigned char roadc[] ={ 3 };
/*---------------------------*/
void menua()
{
 gotoxy(6,9);puts(" ");gotoxy(6,10);puts(" ");
 if(menu==1){gotoxy(6,9);puts("*");}
 if(menu==2){gotoxy(6,10);puts("*");}
}
/*---------------------------*/
void title()
{
 cls();
 gotoxy(5,5);puts("Roader GB");
 gotoxy(8,9);puts("Play");
 gotoxy(8,10);puts("Info");
 gotoxy(0,16);printf("Hi Score: %u%u%u%u",hisd,hisc,hisb,hisa);
 gotoxy(5,14);puts("Hit Start");
 menua();
}
/*---------------------------*/
void infoa()
{
 cls();
 gotoxy(5,0);puts("Roader GB");
 gotoxy(0,2);puts(" Jay Cook, 11/20/98");
 gotoxy(5,7);puts("Hit Start!");
 gotoxy(0,9);puts("Homepage:");
 gotoxy(0,10);puts("http://members.tripod.com/~ziel");
 gotoxy(0,14);puts("Email:");
 gotoxy(0,15);puts("Jaycook1@Juno.com");
 startb=0;
 delay(200);
 while(!startb==1){if (joypad()==J_START){startb=1;} }
 title();
}
/*---------------------------*/
mensel()
{
 if(menu==1){starta=1;}
 if(menu==2){infoa();}
}
/*---------------------------*/
void introa()
{
 starta=0;menu=1;title();
 testa=0;speed=5;
 while(!starta==1)
  {
   if (joypad()==J_START){mensel();} 
   if (joypad()==J_UP){menu--;if(menu<1)menu=1;menua();}
   if (joypad()==J_DOWN){menu++;if(menu>2)menu=2;menua();}
   delay(100);
  }
 HIDE_BKG;HIDE_SPRITES;
}
/*---------------------------*/
void raceover()
{/* ''Plows'' your car to a stop */
 j=5;fone =0;
 for(i=0;i<10;i++)
  {
  delay(60);
   if (i==4)j=4;
   if(i==7)j=3;
   if(i==8)j=2;
   if(i==10)j=1;
   y = (y - j); set_sprite_tile(0,sprt);set_sprite_prop(0,0);move_sprite(0,x,y);
  }
 gotoxy(5,trb);puts("You Crashed");printf("Score: %u%u%u%u",scored,scorec,scoreb,scorea);
}

/*---------------------------*/
void checkcol()
{
 mx=roadinfox[trb];mxx=roadinfox[trc];// my= roadinfoy[trb];myy= roadinfoy[trc];
 my=128;myy=128;
 if (x+8 > mx){ if (x < mx+8) { if (y+8 > my) { if (y<my+8)speed=0;}}}
 if (x+8 > mxx){ if (x < mxx+8) { if (y+8 > myy) { if (y<myy+8)speed=0;}}}
 // old colsion code, reads Y value in reverse     
 //  for(ia=0;ia<63;ia++){  
 //  roadinfoy[ia]=roadinfoy[ia]+speed;
 //  test=roadinfoy[ia]; if(test>256)test=0; roadinfoy[ia]=test;
 //  if (x+8 > roadinfox[ia]){ if (x < roadinfox[ia]+8) { if(y+8 > roadinfoy[ia]) {if (y<roadinfoy[ia]+8)speed=0;}}}
 //  }
}
/*---------------------------*/
void makeroadb()
{ /* Draws the road */
 set_bkg_data(1,3,land);
  j--;if (j<0)j=31;
 /* Makes the road sway back and forth */ 
 if(tra==1){ taa++;if (taa==3){taa=0;
 if(tr==1){rd++;if (rd >3)tr=3;}
 if(tr==2){rd--; if (rd <-3)tr=1;}
 if (tr==3)tr=2;}}
 /* Draws grass */
   for (rx=0;rx<20;rx++){ set_bkg_tiles(rx,j,1,1,roadb); }
 /* Draws left border of road and puts it into memory*/
 rxa=4+rdln+rd+rdc; roadinfox[j]=(rxa*8+8);set_bkg_tiles(rxa,j,1,1,roadc);
 /* Draws road */
 for(rx=0;rx<rdb;rx++){set_bkg_tiles(5+rdln+rd+rx+rdc, j,1,1,roada);}
 /* Draws right border of road and puts it into memory*/ 
 rxa=15+(-rdln)+rd+rdc;roadinfox[j+32]=(rxa*8+8);set_bkg_tiles(rxa,j,1,1,roadc);
 /* Puts rest of road info into memory */
 roadinfoy[j]=(j*8+16); roadinfoy[j+32]=(j*8+16);
}
/*---------------------------*/
void makeroada()
{ rd=0;tra=0;makeroadb();tra=1; }
/*---------------------------*/
void traa() /* sets up collision on left and right side of road */
{trb--;if (trb==-1)trb=31;trc--;if (trc==31)trc=63;}
void trab() /* sets up collision on left and right side of road */
{trb++;if (trb==32)trb=0;trc++;if (trc==64)trc=32;}
/*---------------------------*/
cscore()
{
scorea++;if (scorea==10){scorea=0;scoreb++;if(scoreb==10){scoreb=0;scorec++;if(scorec==10){scorec=0;scored++;if(scored==10){scorea=0;scoreb=0;scorec=0;scored=0;}}}}
}
/*---------------------------*/
void speedup()
{ speed++;if(speed > 8)speed=8; }
/*---------------------------*/
void checkroad()
{
/* If the screen has scrolled enough, then draw a new set of tiles */
rda=rda+speed;if (rda >= 8) { rda=rda-8; cscore();trd++;if(trd=33)trd=0;
 if (rdln<3) cnt++;if (cnt==36) {rdln++;speedup();cnt=0;rd=rd-1;rdb=rdb-2;rdc++;}
 traa();makeroadb();}
}
/*---------------------------*/
void controls()
{
   if(joypad()==J_RIGHT)        
    {
     x=x+speed; if(x>158)x=158; 
     set_sprite_tile(0,sprt);
     set_sprite_prop(0,0);     
     move_sprite(0,x,y);
    }
   
   if(joypad()==J_LEFT)        
    {
     x=x-speed; if(x<10)x=10;
     set_sprite_tile(0,sprt);
     set_sprite_prop(0,0);     
     move_sprite(0,x,y);
    }    
   if(testa==1){if(joypad()==J_UP) { speed++;if (speed >8)speed=8;} } 
   if(testa==1){if(joypad()==J_DOWN) { speed--;if (speed <1)speed=1;} }
   if(joypad()==J_START) 
   {waitpadup();{starta=0;while(!starta==1)if(joypad()==J_START){starta=1; } waitpadup();}}
}
/*---------------------------*/
void main()
{
startabc:
introa();
SPRITES_8x8;
/* sets up info */
score=0;scorea=0;scoreb=0;scorec=0;scored=0;
sprt=0;sprta=0;rdln=0;rdc=0;
x=75;y=130;maxx=35;rx=0;
j=0;tr=1;rd=-1;rdb=10; rda=0;
trb=14;trc=46;tra=1;trd=0;tre=0;
set_sprite_data(0, 1, jcar);
set_sprite_tile(0,sprt);
move_sprite(0,75, 130);
//draws road
 for(i=14;i>1;i--){ makeroadb(); }for(i=34;i>14;i--){ makeroada();} 
SHOW_BKG;SHOW_SPRITES;
mx=8;my=8+8;
while(!speed==0)
  {
    controls();
    checkroad();
    scroll_bkg(0,-speed); tre=tre+speed;
    if(tre>=255) tre=tre-255;
    checkcol();
 if(speed>0)  delay(130);
        }  
raceover();
{waitpadup();{starta=0;while(!starta==1)if(joypad()==J_START){starta=1; } waitpadup();}}
set_sprite_tile(0,sprt);set_sprite_prop(0,0); move_sprite(0,x,0);
scroll_bkg(0,tre);
//if (score > hiscore)hiscore=score;
if (hisd <= scored){if(hisc <= scorec){if(hisb <= scoreb){if(hisa<=scorea) {hisa=scorea;hisb=scoreb;hisc=scorec;hisd=scored;}}}}
goto startabc;
} 

/* thats all */
