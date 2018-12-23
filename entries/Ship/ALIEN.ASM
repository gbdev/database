; Moved Jeff's counter routine to indicate alien collision - M.M.


alien
 ld a,30                ; Y-Pos
 ld ($c00c),a
 ld ($c010),a

 ld a,($c00d)           ; X-Pos
 add a,2
 ld ($c00d),a
 add a,8
 ld ($c011),a

 ld a,4                 ; Frame
 ld ($c00e),a
 ld ($c012),a

 ld a,0                 ; Left sprite normal, Right sprite slipped
 ld ($c00f),a
 ld a,%00100000
 ld ($c013),a

 ld a,($c008)             ; Collision routine!
 ld b,a
 ld a,($c00c)
 sub b
 jr nc,nocol
 add a,8
 jr nc,nocol
 ld a,($c009)
 add a,4                  ; adjust shot offset for ccurate xpos collision
 ld b,a
 ld a,($c00d)
 sub b
 jr nc,nocol
 add a,16
 jr nc,nocol

 ld a,$ff                 ; Collision detected, now reset alien and shot
 ld ($c00d),a
 ld ($c010),a
 ld (fpos),a

 ld de,$1               ;Add 1 to score <----- J.F. 23-OCT-97
 call ScoreShow         ;and display.   <-----

nocol
                                                                  
 ret
