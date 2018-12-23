;               DEDICATED TO GUMPIE YOKOI 1941-1997
;
;            Megamania Clone (Megamania TM Activision)
;                          Version 1.1a
;
;      Source, Routines, Music and Data (C) 1997 Michael Mika
;      and Genetic Fantasia.  Any use of said copyright for
;      commercial distribution is STRICTLY prohibited.  This
;      document is provided for internal use only.
;      Any violation of said copyright is punishable BY LAW.
;
;      A simple demonstration of sprites and tiles.  Just
;      a ship that can be moved left and right with limits
;      and the capability to fire.  Feel free to try and add
;      bad guys and collisions.
;
;      Mike (mmika@geneticfantasia.com)

; V1.1  - Added fire count, Jeff F., 23-Oct-97
; V1.1a - Added alien ship, Mike M., 24-Oct-97

hirambase       =       0ff80h
lorambase       =       0c0a0h
gfxtiles        =       $8800
sprtiles        =       $8000
gameon          =       %10100111  ;turn game screen on
#DEFINE LOBYTEVAR(X)  X = lorambase \lorambase  .set (lorambase + 1)
#DEFINE HIBYTEVAR(X)  X = hirambase \hirambase  .set (hirambase + 1)
#DEFINE LOWORDVAR(X)  X = lorambase \lorambase  .set (lorambase + 2)
#DEFINE HIWORDVAR(X)  X = hirambase \hirambase  .set (hirambase + 2)
; Create variables in low-ram

LOBYTEVAR(xpos)                 ; player X-Position
LOBYTEVAR(fpos)                 ; shot Y-Position

.org $0000              ; Needed to fool tasm..

.org $0040              ; VBlank IRQ
 reti                   ; Do nothing
.org $0048              ; LCDC Status IRQ
 reti                   ; Do nothing
.org $0050              ; Timer Owerflow
 reti                   ; Do nothing
.org $0058              ; Serial Transfear Completion
 reti                   ; Do nothing
.org $0060              ; Hmm, this is a wierd on
                        ; Im not sure how this one works
                        ; Transition from high to low
                        ; of pin p10-p13
                        ; I think Its a hardware thing
 reti                   ; Do nothing :)
; Irqs done..

.org $0100

; GameBoy Header with correct checksum
.db $00,$C3,$50,$01,$CE,$ED,$66,$66,$CC,$0D,$00,$0B,$03,$73,$00,$83
.db $00,$0C,$00,$0D,$00,$08,$11,$1F,$88,$89,$00,$0E,$DC,$CC,$6E,$E6
.db $DD,$DD,$D9,$99,$BB,$BB,$67,$63,$6E,$0E,$EC,$CC,$DD,$DC,$99,$9F
.db $BB,$B9,$33,$3E     ; Standard Nintendo DO NOT CHANGE...

.db "MEGAMANIA       "  ; Cart name   16bytes
.db $00,$00,$00         ; Not used
.db $00                 ; Cart type   ROM Only
.db $00                 ; ROM Size    32k
.db $00                 ; RAM Size     0k
.db $fe,$ba             ; Maker ID    $bafe=Genetic Fantasia
.db $01                 ; Version     =1
.db $ce                 ; Complement check (Important)
.db $37,$69             ; Cheksum, fix this if you are going to
                        ; run this in VGB

start                   ; This is addr $0150
 ld a,0
 ldh ($40),a
 ld     sp,$fff4        ; Put the stack where the GB wants it
 ld a,0
 ld ($ff0f),a
 ld     a,%00000000     ; VBLANK IRQs ON
 ldh    ($ff),a
 ei

 call initdma
reset
 ld a,0
 sub    a               ; Misc standard init things..
 ldh    ($41),a         ; LCDC Status
 ldh    ($42),a         ; Screen scroll Y=0
 ldh    ($43),a         ; Screen scroll X=0
 call   clean
 ld     a,%00000111     ; LCD Controller = Off (No picture on screen)
                        ; WindowBank = $9800 (Not used)
                        ; Window = OFF
                        ; BG Chr = $8000
                        ; BG Bank= $9800
                        ; OBJ    = 8x8
                        ; OBJ    = Off
                        ; BG     = On
 ldh    ($40),a


 call   nor_col         ; Normal palette

 call   waitvbl         ; Must be in VBL before turning the screen On.
 ld     a,gameon     ; LCD Controller = On
 ldh    ($40),a
 call   maincopy

;############ setup
 ld a,115           ; Y position of ship
 ld ($c000),a
 ld (xpos),a        ; Set ship near center
 ld ($c004),a       ; Y position of 2nd ship sprite
 ld a,0             ; Set frame and other goodies in sprite pseudo base
 ld ($c00b),a       ; DMA copies $c000 to $c0a0 to sprite oam
 ld ($c002),a
 ld ($c003),a
 ld ($c006),a
 ld a,%00100000
 ld ($c007),a
 ld a,$ff
 ld (fpos),a        ; Fire position at $ff (Offscreen)
 ld a,2
 ld ($c00a),a

 call ScoreReset    ; Set score to 0000      <----- J.F. 23-Oct-97
 ld de,$0           ;                        <-----
 call ScoreShow     ; Display Score on screen<-----

mainloop
 call getkeys           ; Check for Start Key
 bit $1,a
 call nz,left
 bit $0,a
 call nz,right
 bit $4,a
 call nz,fire
 call waitvbl
; Draw ship!
 ld a,(xpos)
 ld ($c001),a
 add a,4
 ld ($c009),a
 add a,4
 ld ($c005),a
 ld a,(fpos)  ; if FPOS <> $ff then subtract 3 positions until it does equal
 cp $ff       ; $ff!
 jr z,main2
 dec a
 dec a
 dec a
 ld (fpos),a
main2
 ld ($c008),a

 call alien         ; Call Alien routine     <----- M.M. 24-Oct-97
 call $ff80      ; call sprite DMA routine to copy $c000-$c0a0 to $fe00
 jp mainloop

right:
 push af
 ld a,(xpos)
 sub 8*20-12
 jr nc,right2
 add a,8*20-12
 inc a
 inc a
 ld (xpos),a
right2
 pop af
 ret

left:
 push af
 ld a,(xpos)
 sub 12
 jr c,left2
 add a,12
 dec a
 dec a
 ld (xpos),a
left2
 pop af
 ret

fire:
 push af
 ld a,(fpos)
 cp $ff
 jr nz,fire2
 ld a,116
 ld (fpos),a
fire2
 pop af
 ret

maincopy
 ld hl,mainspr
 ld de,sprtiles
 ld bc,2048
 call move
 ld hl,tiles
 ld de,gfxtiles
 ld bc,2048
 call move
 ld hl,screen
 ld de,$9800
 ld bc,1024
 call move
 ret

move
 ldh     a,(41h)
 and     2
 jr      nz,move
 ld     a,(hli)
 ld     (de),a
 inc    de
 dec    bc
 ld     a,b             ; Are we done (is bc=0000??)
 or     c
 jr     nz, move
 ret

move_char
 ld     hl,$8000
 ld     d,$00           ; move 256 bytes
 ld     e,$12           ; x2=512
 jp     mchar_loop
 ret

mchar_loop
 ldh     a,(41h)
 and     2
 jr     nz,mchar_loop
 ld     a,(bc)
 ld     (hli),a
 inc    bc
 dec    d
 jp     nz,mchar_loop
 dec    e
 jp     nz,mchar_loop
 ret

move_text
 ld     hl,$d800
 ld     d,$00
 ld     e,$04           ; 256*4=1024=32x32=One whole GB Screen
 jp     mtext_loop

mtext_loop
 ld     a,(bc)
 ;and    $3f             ; Lowest 6 bits only *removed* NOT TEXT
 ld     (hli),a
 inc    bc
 dec    d
 jp     nz,mtext_loop
 dec    e
 jp     nz,mtext_loop
 ret


; **** Main Sprite Animation Frames ****
screen
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h,087h
.byte 088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h
.byte 088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h,088h
.byte 086h,080h,081h,082h,083h,084h,085h,086h,086h,086h,086h,086h,086h,086h,086h,086h
.byte 086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h
.byte 086h,086h,086h,086h,086h,086h,086h,08Ah,08Bh,08Ah,08Bh,08Ah,08Bh,086h,086h,086h
.byte 086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h
.byte 086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h
.byte 086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h,086h
mainspr
.byte 001h,001h,007h,007h,01Fh,01Fh,01Fh,01Fh,007h,007h,007h,007h,001h,001h,001h,001h
.byte 031h,031h,033h,033h,037h,037h,03Fh,03Fh,039h,039h,031h,031h,030h,030h,030h,030h
.byte 018h,018h,018h,018h,018h,018h,018h,018h,018h,018h,018h,018h,018h,018h,018h,018h
.byte 000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h
.byte 000h,000h,000h,000h,00Fh,00Fh,07Fh,07Fh,07Fh,07Fh,000h,000h,06Eh,06Eh,06Eh,06Eh
.byte 000h,000h,07Fh,07Fh,07Fh,07Fh,00Fh,00Fh,000h,000h,000h,000h,000h,000h,000h,000h
.byte 000h,000h,000h,000h,0F0h,0F0h,0FEh,0FEh,0FEh,0FEh,000h,000h,0EEh,0EEh,0EEh,0EEh
.byte 000h,000h,0FEh,0FEh,0FEh,0FEh,0F0h,0F0h,000h,000h,000h,000h,000h,000h,000h,000h
tiles
.byte 000h,0FFh,07Ch,0FFh,060h,0FFh,078h,0FFh,060h,0FFh,07Ch,0FFh,000h,0FFh,000h,0FFh
.byte 000h,0FFh,0C3h,0FFh,0F3h,0FFh,0FFh,0FFh,0CFh,0FFh,0C3h,0FFh,000h,0FFh,000h,0FFh
.byte 000h,0FFh,03Eh,0FFh,030h,0FFh,03Ch,0FFh,030h,0FFh,03Eh,0FFh,000h,0FFh,000h,0FFh
.byte 000h,0FFh,078h,0FFh,066h,0FFh,066h,0FFh,078h,0FFh,066h,0FFh,000h,0FFh,000h,0FFh
.byte 000h,0FFh,078h,0FFh,060h,0FFh,066h,0FFh,066h,0FFh,07Eh,0FFh,000h,0FFh,000h,0FFh
.byte 000h,0FFh,0CCh,0FFh,0FCh,0FFh,030h,0FFh,030h,0FFh,030h,0FFh,000h,0FFh,000h,0FFh
.byte 000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh
.byte 000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h
.byte 000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,000h,0FFh,000h,0FFh,000h,0FFh
.byte 000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh,000h,0FFh
.byte 07Fh,0FFh,006h,0FFh,007h,0FFh,00Fh,0FFh,00Fh,0FFh,007h,0FFh,006h,0FFh,07Fh,0FFh
.byte 000h,0FFh,018h,0FFh,03Ch,0FFh,0FEh,0FFh,0FEh,0FFh,03Ch,0FFh,018h,0FFh,000h,0FFh

digits                          ;<----- J.F. 23-Oct-97
 .include "digits.asm"          ;<-----

; **** Libraries ****
; Get Keypad Button Status
; From Pan's technical document.
; The following bits are set if pressed.
;    $80 - Start   $8 - Down
;    $40 - Select  $4 - Up
;    $20 - B       $2 - Left
;    $10 - A       $1 - Right

getkeys
 ld     a,$20
 ldh    ($00),a         ;turn on P15
 ldh    a,($00)         ;delay
 ldh    a,($00)

 cpl
 and    $0f
 swap   a
 ld     b,a

 ld     a,$10
 ldh    ($00),a         ;turn on P14
 ldh    a,($00)         ;delay
 ldh    a,($00)
 ldh    a,($00)
 ldh    a,($00)
 ldh    a,($00)
 ldh    a,($00)

 cpl
 and    $0f
 or     b
 swap   a
 ret

nor_col                 ; Sets the colors to normal palette
 ld     a,%10010011     ; grey 3=11 (Black)
                        ; grey 2=10 (Dark grey)
                        ; grey 1=01 (Ligth grey)
                        ; grey 0=00 (Transparent)
 ldh    ($47),a
 ld     a,%01001011     ; grey 3=11 (Black)

 ldh    ($48),a         ; 48,49 are sprite palettes set same as background
 ld     a,$00000000
 ldh    ($49),a
 ret

initdma                 ; Transfer DMA routine to RAM
 ld     de,$ff80
 ld     hl,dmacode
 ld     bc,dmaend-dmacode
 call   move
 ret

dmacode                 ; Transfer sprite data from reg A pos. using DMA
 di
 push af
 ld     a,$c0
 ldh    ($46),a         ; Start DMA
 ld     a,$28           ; Wait for 160ns
dma_wait
 dec    a
 jr     nz,dma_wait
 pop af

 ei
 ret
dmaend

waitvbl                 ; Wait for Vertical blank
 push af
 push bc
 push de
 push hl
 ldh    a,($40)         ; LCD screen on??
 add    a,a
 jr     nc,wvb
notyet
 ldh    a,($44)         ; $ff44=LCDC Y-Pos
 cp     $98             ; $98 and bigger = in VBL
 jr     nz,notyet
wvb
 pop hl
 pop de
 pop bc
 pop af
 ret

spr_cls                 ; Clear Sprites
 ld l,0
 ld h,$c0
spclear
 ld a,$ff
 ld (hl),a
 inc l
 ld a,l
 cp $a0
 jp nz,spclear
 ret


clean
 ld     a,%00000000     ; VBLANK IRQs ON
 ldh    ($ff),a
 call spr_cls
 ld     a,%00000011     ; LCD Controller = Off (No picture on screen)
 ldh    ($40),a
 ld a,0
 ldh ($43),a
 ldh ($42),a
 call $ff80
 call waitvbl
 ret

; Include score library
 .include "score.asm"     ;<----- J.F. 23-Oct-97
; Include alien library
 .include "alien.asm"     ;<----- M.M. 24-Oct-97

.block $008000-$          ; pad rest of rom with zeros
.end

