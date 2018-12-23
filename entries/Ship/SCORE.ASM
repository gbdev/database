
; Score keeping routines, J.F., 23-Oct-97

LOBYTEVAR(digit1)
LOBYTEVAR(digit2)

ScoreX = 16                            ;X position of score
ScoreY = 15                            ;Y position of score
ScreenScore = $9800+ScoreX+(32*ScoreY) ;Scrn address of score
ChrDigits = $8c                        ;start of digits char set

; Reset score to 0000
ScoreReset
        ld      hl,digit1
        xor     a               ; A = 0
        ldi     (hl),a
        ldi     (hl),a
        ret

; Add DE to running score from digit1 to digit2
; DE must be in Binary Coded Decimal (BCD) format.
; (i.e. to add 100 to score set DE=$100)

ScoreAdd:
        ld      hl,digit2
        ld      a,e
        add     a,(hl)
        daa
        ldd     (hl),a
        ld      a,d
        adc     a,(hl)
        daa
        jr      c,ScoreOver      ; score has overflowed 9999
        ld      (hl),a
        ret

;Force score to never go over 9999
ScoreOver:
        ld      a,$99
        ldi     (hl),a
        ldi     (hl),a
        ret

; Add DE to running score & put on screen
; DE must be in Binary Coded Decimal (BCD) format.
; (i.e. to add 100 to score set DE=$100)
ScoreShow
        call    ScoreAdd
        ld      bc,ScreenScore
        ld      hl,digit1

        ld      a,(hl)
        ld      e,a
        srl     a
        srl     a
        srl     a
        srl     a
        add     a,ChrDigits
        push    af

ScoreS1                     ;Wait until screen memory available
        ldh     a,(41h)
        and     2
        jr      nz,ScoreS1

        pop     af
        ld      (bc),a

        inc     bc
        ld      a,e
        and     0fh
        add     a,ChrDigits
        push    af

ScoreS2                     ;Wait until screen memory available
        ldh     a,(41h)
        and     2
        jr      nz,ScoreS2

        pop     af
        ld      (bc),a

        inc     bc
        inc     hl

        ld      a,(hl)
        ld      e,a
        srl     a
        srl     a
        srl     a
        srl     a
        add     a,ChrDigits
        push    af

ScoreS3                     ;Wait until screen memory available
        ldh     a,(41h)
        and     2
        jr      nz,ScoreS3

        pop     af
        ld      (bc),a
        inc     bc
        ld      a,e
        and     0fh
        add     a,ChrDigits
        push    af

ScoreS4                     ;Wait until screen memory available
        ldh     a,(41h)
        and     2
        jr      nz,ScoreS4

        pop     af
        ld      (bc),a
        ret
;
