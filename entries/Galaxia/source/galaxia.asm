;--------------------------------
;            Galaxia
;  Tomasz Slanina - dox@space.pl
;--------------------------------


;limits

MIN_PLAYER_Y equ 24
MAX_PLAYER_Y equ 144

MIN_PLAYER_X equ 16
MAX_PLAYER_X equ 96


;starting position of ship

START_Y  equ 84

;collision rectangles

PLAYER_Y equ 8
PLAYER_Y2 equ 16
PLAYER_X equ 16
PLAYER_X2 equ 16+8

BULLET_Y equ 8
BULLET_Y2 equ 16
BULLET_X equ 8
BULLET_X2 equ 16

;tiles and colors

TILE_BULLET equ 5
TILE_ENEMY equ   6
TILE_ENEMY2 equ  4

COLOR_ENEMY2 equ 1
COLOR_ENEMY equ 1
SHIP_COLOR equ 0

;speed of enemies

START_SPEED equ 5
HARD_SPEED equ 8

;diff increase after MAX_HIT hits

MAX_HIT equ 12

; varaiables in HiRAM (for faster access)

scroll   equ $ff8a
oldb     equ $ff8b
espeed   equ $ff8c
bigl     equ $ff8d
increase equ $ff8e
auto2    equ $ff8f


SECTION "start",HOME[0]

restartzero:   ;label must be set before any local labels
       ld a,32     ;keypad read
       ld hl,$ff00
       ld de,shadow
       ld [hl],a
       ld a,[hl]
       ld a,[hl]
       and $0f
       swap a
       ld b,a
       ld a,16
       ld [hl],a
       ld a,[hl] ;4 times (should be 6 times)
       ld a,[hl]
       ld a,[hl]
       ld a,[hl]
       and $0f
       or b
       cpl
       ld b,a
       bit 6,a  ;Up
       jr z,.down
       ld a,[de] ;y
       cp MIN_PLAYER_Y
       ret c
       sub 4   ;4 = offset
       ld [de],a   ;two sprites (ship)
       ld [shadow+4],a
       ret
.down:
       bit 7,a ;down
       ret z
       ld a,[de];y
       cp MAX_PLAYER_Y
       ret nc
       add 4
       ld [de],a
       ld [shadow+4],a
       ret

vblank:

       inc a
       ld [scroll],a
       jp $ff80 ;jump to HiRAM


SECTION "vblank",HOME[$40]  ;VBL interrupt vector
       push af
       ld a,[scroll] ;Scroll offset
       inc a
       jp vblank ; jump ^^^


SECTION "hblank",HOME[$48]     ;LCDC interrupt vector (hblank mode)
hblank:
       push af
       push bc
       ld a,[scroll] ;pseudo paralax scrolling
       ld b,a
       ld a,[$ff44] ;current scanline
       cp 1
       jr z,.set
       cp 121
       jr z,.set
       srl b
       cp 17
       jr z,.set
       cp 105
       jr z,.set
       srl b
       cp 33
       jr z,.set
       cp 89
       jr z,.set
       srl b
       cp 49
       jr nz,.exit
.set:
       ld a,b
       ld [$ff43],a ; BG scroll X offset

.exit:
       pop bc
       pop af
       reti

; collisions ship - obstacles

collisions:
       ld hl,$c000 ;ship coords
       ld a,[hl+]
       ld b,a   ;y
       ld c,[hl] ;x
       ld d,-16  ; -16 = off
       ld l,2*4+4*4 ;skip bulltes
.kl1:
       ld a,[hl]
       cp d ;-16
       jr z,.notused
       cp 255
       jp z,collisionscd  ;bullets collisions
       push hl
       inc hl
       sub PLAYER_Y  ;calculations of collision rectangles
       cp b
       jr nc,.skip
       add PLAYER_Y2
       cp b
       jr c,.skip
       ld a,[hl]
       sub PLAYER_X
       cp c
       jr nc,.skip
       add PLAYER_X2
       cp c
       jr c,.skip
.wait:    ;game over
       dec hl
       ld a,h
       or l
       jr nz,.wait
       jp $100  ; restart

.skip:
       pop hl
.notused:
       ld a,4 ; next sprite
       add l
       ld l,a
       jr .kl1

;bullets collisions

bcol:
       ld a,[hl]
       cp d      ; d = -16
       ret z
       push hl
       inc hl
       ld b,a     ;y
       ld c,[hl]  ;x
       ld l,2*4+4*4 ; enemies
.kl1xx:
       ld a,[hl]
       cp d
       jr z,.nieuzywanyxx
       cp 255
       jr z,.kokoxx
       push hl
       inc hl
       sub BULLET_Y
       cp b
       jr nc,.skipxx
       add BULLET_Y2
       cp b
       jr c,.skipxx
       ld a,[hl]
       sub BULLET_X
       cp c
       jr nc,.skipxx
       add BULLET_X2
       cp c
       jr c,.skipxx
       pop hl
       inc hl ;x
       inc hl ;tile
       ld a,[hl-]
       cp TILE_ENEMY
       jr nz,.nieENEMY
       dec hl
       ld [hl],d ;remove destroyed enemy

       ld a,[bigl]
       inc a
       cp MAX_HIT
       jr c,.spo
       ld a,$ff
       ld [increase],a
       cpl
.spo:
       ld [bigl],a
.nieENEMY:
       pop hl
       ld [hl],d ;usuwamy pocisk
       ret
.kokoxx:
       pop hl
       ret
.skipxx:
       pop hl
.nieuzywanyxx:
       ld a,4
       add l
       ld l,a
       jr .kl1xx


SECTION "boot",HOME[$100]
       nop
       jp main

SECTION "header",HOME[$134]

       db "GALAXIA        ",$c0
       db 0,0,0,0,0,0,0,0,0,0,0,0
main:
       di
       xor a
       ld [$ff40],a ;LCD off
       ld sp,$cfff
       ld [$ff4f],a  ;vram bank 0
       ld h,$80
       ld l,a
       ld de,tiles

       ld c,16
.loop7:
       cpl
       ld [hl+],a
       dec c
       jr nz,.loop7

       ld c,16*6
.loop6:
       ld a,[de]
       inc de
       ld [hl+],a
       dec c
       jr nz,.loop6

       ld h,$98
       ld l,c ;c=0
       push hl
       ld e,32
       ld b,4
.lbig:
       ld c,e
       xor a
.l2:
       ld [hl+],a ; solid color
       dec c
       jr nz,.l2
       ld c,e
       ld a,1
.l3:
       ld [hl+],a
       dec c
       jr nz,.l3
       dec b
       jr nz,.lbig
       ld c,32*2 ;middle of the screen
       xor a
.xxx:
       ld [hl+],a
       dec c
       jr nz,.xxx

       ld b,4 ; down part of bg screen
.lbigx:
       ld c,e
       ld a,1
.l3x:
       ld [hl+],a
       dec c
       jr nz,.l3x

       ld c,e
       xor a
.l2x:
       ld [hl+],a ; solid color
       dec c
       jr nz,.l2x
       dec b
       jr nz,.lbigx
       pop hl
       ld a,1
       ld [$ff4f],a
       ld d,b   ;0
       ld b,4
.lbig2:
       ld c,e
       ld a,d
.lx1:
       ld [hl+],a ;solid
       dec c
       jr nz,.lx1
       inc d
       ld c,16 ;only 16 !
.lx2:
       ld a,d
       ld [hl+],a
       set 5,a    ;flip h on
       ld [hl+],a
       dec c
       jr nz,.lx2
       dec b
       jr nz,.lbig2

       ld c,32*2
       ld a,4
.xxx2:
       ld [hl+],a
       dec c
       jr nz,.xxx2
       ld b,4
.lbig2x:
       ld c,16
       ld a,d
       set 6,a  ; flip v always on
.lx2x:
       ld [hl+],a
       set 5,a    ;flip h on
       ld [hl+],a
       res 5,a    ;flip h off
       dec c
       jr nz,.lx2x
       dec d
       ld c,e
       ld a,d
.lx1x:
       ld [hl+],a ;linia solid = paleta
       dec c
       jr nz,.lx1x
       dec b
       jr nz,.lbig2x

       ld hl,$ff68 ; BG palette
       ld a,128
       ld [hl+],a
       ld c,8
       ld d,h
       xor a
.pall:
       ld [hl],a   ;palette generator
       ld [hl],d
       add 5
       ld [hl],a
       ld [hl],d
       ld [hl],d
       ld [hl],d
       ld [hl],d
       ld [hl],d
       dec c
       jr nz,.pall
       inc hl  ;ff6a
       ld a,128+2
       ld [hl+],a
       ld de,spritep
       ld c,64
.copy:
       ld a,[de]
       ld [hl],a
       inc de
       dec c
       jr nz,.copy
       ld a,8   ;LCDC interrupt = hblank
       ld [$ff41],a   ;LCDC set

       ld hl,oamdma ;OAM DMA code MUST be executed from HiRAM
       ld de,$ff80
       ld c,a
       inc c
.copy1:
       ld a,[hl+]
       ld [de],a
       inc de
       dec c
       jr nz,.copy1

       ld hl,shadow ; shadow OAM clear
       ld a,-16
       ld c,a
.xloop:
       ld [hl+],a
       dec c
       jr nz,.xloop

       xor a    ; varaibles set
       ld [oldb],a
       ld [bigl],a
       ld [increase],a
       ld [auto2],a
       ld l,a
       cpl
       ld [s_end],a
       ld a,START_SPEED
       ld [espeed],a
       ld a,START_Y ;ship sprites
       ld h,$c0
       ld [hl+],a
       ld a,10
       ld [hl+],a
       ld a,2     ;tile
       ld [hl+],a
       ld a,SHIP_COLOR
       ld [hl+],a
       ld a,START_Y
       ld [hl+],a
       ld a,10+8
       ld [hl+],a
       ld a,2+1     ;tile
       ld [hl+],a
       ld a,SHIP_COLOR
       ld [hl],a

       ld a,128+16+2 ;on , chr 8000 , bg 9800 , 8x16 , obj on
       ld [$ff40],a

       xor a
       ld [$ff0f],a  ;clear interrupts flag
       ld a,3
       ld [$ffff],a  ;set interrupts = VBL+LCDC
       ei

mainloop:
       ld hl,scroll
       ld a,[hl]

.waitframe:
       cp [hl]
       jr z,.waitframe ;wait for next frame

       ld a,[increase] ;diff. increase ?
       or a
       jr z,.noinc
       ld a,[espeed] ; speed of enemies
       cp START_SPEED
       jr nz,.diff2
       ld a,HARD_SPEED
       ld [espeed],a
       jr .noinc
.diff2:
       ld [auto2],a
.noinc:
       xor a
       ld [increase],a
       bit 1,[hl]
       jp z,collisionsloop
       rst 0  ; keypad read and test up/down
       bit 5,b
       jr z,.left
       ld a,[shadow+1];x
       cp MIN_PLAYER_X
       jr c,.skipmove
       sub 4
       ld [shadow+1],a
       add 8
       ld [shadow+5],a
       jr .skipmove

.left:
       bit 4,b
       jr z,.skipmove
       ld  a,[shadow+1];x
       cp  MAX_PLAYER_X
       jr nc,.skipmove
       add 4
       ld [shadow+1],a
       add 8
       ld [shadow+5],a
.skipmove:
       ld a,[oldb] ; old buttons status
       xor b
       and b
       ld c,a
       ld a,b
       ld [oldb],a
       ld a,c
       and 3
       jr z,.noshot

;shot

       ld hl,shadow+4*2
       ld c,4
.loz:
       ld a,[hl]
       cp -16
       jr nz,.nextbullet

       ld a,[shadow] ;free slot was found
       ld [hl+],a
       ld a,[shadow+1]
       add 9
       ld [hl+],a
       ld a,TILE_BULLET
       ld [hl+],a
       ld a,1
       ld [hl],a
       jr .noshot

.nextbullet:
       ld a,4
       add a,l
       ld l,a
       dec c
       jr nz,.loz

.noshot:

;new enemies

       ld a,[scroll] ; pseudo "timer"
       and $c
       jr nz,.endenemyadd

       ld hl,shadow+4*2+4*4 ; skiping ship/bullets
.l1:
       ld a,[hl]
       cp -16  ; is active ?
       jr z,.insert
       cp 255   ; end of sprites
       jr z,.endenemyadd
       inc hl
       inc hl
       inc hl
       inc hl
       jr .l1

.insert:  ;free slot

       ld a,[$ff04] ;random number generator
       ld b,a
       ld a,[scroll]
       cpl
       rla
       rla
       xor b
       swap a
       and 127 ;limit
       add 24

       ld [hl+],a  ; y
       ld a,170 ; x
       ld [hl+],a

       ld a,[$ff04]
       bit 0,a      ;red or green ?
       ld a,TILE_ENEMY
       ld b,COLOR_ENEMY
       jr z,.llx
       ld a,TILE_ENEMY2
       ld b,COLOR_ENEMY2
.llx:
       ld [hl+],a
       ld [hl],b

.endenemyadd:

;sprite autorun

       ld hl,shadow+4*2 ;starting form "bullets"
       ld c,-16
.loopauto:

       ld a,[espeed]
       ld e,a
       ld a,[hl+] ;x
       cp c  ;on/off ?
       jr z,.skipme
       cp 255
       jr z,.end
       inc hl ;tile
       ld a,[hl]
       cp TILE_BULLET
       jr z,.bullet_auto

       cp TILE_ENEMY
       jr z,.enemy_auto

       ld a,[auto2]
       srl e
       or a
       jr z,.enemy_auto  ;skip in easy mode

       dec hl
       ld a,[hl];x
       and 15
       sub 7
       ld b,a
       dec hl
       ld a,[hl]
       add b
       ld [hl+],a
       ld a,[hl]
       sub START_SPEED/2
       jr .cont

.enemy_auto:

       dec hl ;x
       ld a,[hl]
       sub e
.cont:
       ld [hl],a ;x
       cp 8
       jr nc,.skipme
       dec hl   ;y
       ld a,c
       ld [hl+],a

.skipme:
       inc hl ;tile
       inc hl ;atrib
       inc hl ;next
       jr .loopauto

.bullet_auto:
       dec hl
       ld a,[hl]
       add 5
       ld [hl],a
       cp 160
       jr c,.skipme
       dec hl
       ld a,c
       ld [hl+],a
       jr .skipme
.end:
       jr shortcut  ; 2 bytes instead 3 for "jp mainloop"

collisionsloop:
       call collisions

shortcut:
       jp mainloop

collisionscd:
       ld l,8
       call bcol
       ld l,12
       call bcol
       ld l,16
       call bcol
       ld l,20
       jp bcol

oamdma:
       ld a,$c0    ; DMA Shadow OAM -> OAM
       ld [$ff46],a
.wait:
       dec a
       jr nz,.wait
       pop af
       reti

spritep:

db %00000001,%01111101
db %00000000,%00000000
db %00000000,%01000100
db %00010000,%00000010
db %00000000,%00000000
db %00011111,%00001101
db %11100000,%00000011

tiles:

db %00000000,%10000000
db %10000000,%01000000
db %11000000,%00100000
db %11100000,%00010000
db %11110000,%00001100
db %11111100,%00000011
db %11111111,%00000000
db %11111111,%00000000

db %00000000,%00011110
db %00000000,%00001111
db %00000111,%00000111
db %00000000,%00011111
db %00000000,%00011111
db %00000111,%00000111
db %00000000,%00001111
db %00000000,%00011110

db %00000000,%00000000
db %00000000,%10000000
db %11111110,%11111110
db %01111111,%10000001
db %01111111,%10000001
db %11111110,%11111110
db %00000000,%10000000
db %00000000,%00000000

db %11111111,%00000000
db %10000001,%01111110
db %10000001,%01111110
db %10000001,%01111110
db %10000001,%01111110
db %10000001,%01111110
db %10000001,%01111110
db %11111111,%00000000

db %00000000,%00000000
db %00000000,%00000000
db %00000000,%00000000
db %00111100,%00000000
db %00111100,%00000000
db %00000000,%00000000
db %00000000,%00000000
db %00000000,%00000000

db %00011000,%00000000
db %00111100,%00011000
db %01111110,%00111100
db %11111111,%01111110
db %11111111,%01111110
db %01111110,%00111100
db %00111100,%00011000
db %00011000,%00000000


db " dox@space.pl"  ;placeholder :)


SECTION "RAM",BSS

shadow:                 ds 40*4  ;Shadow OAM
s_end:                  ds 1     ;0xff = end of sprite table
