@echo off
setlocal enabledelayedexpansion

for %%i in (*.c) do (
	echo Compiling %%i...
	..\bin\lcc -Wa-l -c -o %%i.o %%i
	set str=!str! %%i.o
)

for %%i in (levels/*.s) do (
	echo Compiling %%i...
	..\bin\lcc -Wa-l -c -o %%i.o levels/%%i
	set str=!str! %%i.o
)

..\bin\lcc -Wl-m -Wl-yp0x143=0xC0 -o turtle.gb %str%
del *.lst *.o *.map *.sym
pause
