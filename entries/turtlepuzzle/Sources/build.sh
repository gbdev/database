export GBDKDIR=/home/xubuntu/gbdk/

for C in $(ls levels/*.z80); do
	echo Converting $C...
	./replace $C
	rm -rf $C
done

for C in $(ls *.c); do
  echo Compiling $C...
  ../bin/lcc -Wa-l -c -o $C.o $C
  str="$str $C.o"
done

for C in $(ls *.s); do
  echo Compiling $C...
  ../bin/lcc -Wa-l -c -o $C.o $C
  str="$str $C.o"
done

rm -rf levels/*.inc

for C in $(ls levels/*.s); do
  echo Compiling $C...
  ../bin/lcc -Wa-l -c -o $C.o $C
  str="$str $C.o"
done

../bin/lcc -Wl-m -Wl-yp0x143=0xC0 -o turtle.gb $str
rm -f *.lst *.o *.sym
cd levels
rm -f *.lst *.o *.map *.sym
read
wine $GBDKDIR/bgb.exe $GBDKDIR/Sources/turtle.gb
clear
