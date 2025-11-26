# TextReader.GB
Plays plain text files directly
from the SD card!

This is a simple TXT File Reader for:
* the Game Boy with an **EZ-Flash Junior** SD cart; *(Tested)*
* the Game Boy with an **Everdrive X3/X5/X7** SD cart; *(untested)*
	* *maybe the everdrive version could work on some recent clones, needs confirmation. I tested 2 old clones and they did not work at all.*

Partially supported Charsets:
* UTF-8
	* should be enough for most latin characters

Supported Charsets:
* CP1252 (aka Windows 1252)
* ISO-8859-1 (a subset of CP1252)

## Instructions

### Controls
#### File Browser
* UP/DOWN: Navigate files;
* LEFT/RIGHT: skip a "page";
* A: Open file;
* B: Back to first file;
* SELECT: Show All Files/Show TXT (and a few others) files only;
* START: Show info.

#### Text Reader
* UP/DOWN: Navigate lines;
* LEFT/RIGHT: skip a "page" (about 14 lines);
* A: Expand line;
* B: Back to file browser;
* SELECT: Change Charset Encoding;
* START: Change Font.

## Future plans/Wishlist
* Automatic line break option
* Better UTF8 implementation
* Make it faster, better caching
* Auto-detect encoding
* Compatibility with more flash cards
* Simple Markdown support
* Suggestions?

## More info

License: MIT

This project used VGM player as a base and wont be possible without this.
https://github.com/untoxa/VGM_player


	Thanks to untoxa for making this VGM Player, not only because this application is based on his work, but also because I didnt realize this project was possible until seeing this thing work on my EZ-Flash Jr.

	Also a thanks to all GBDK-2020 mantainers and authors, GBCompo25 organizers, partners and sponsors. You rock!

You need the latest version of GBDK-2020, GNU Make, Python + Pillow package to compile this project.
On windows you also need the linux subsystem, say, MSys2.

Charset References:
* https://www.charset.org/utf-8
* https://www.charset.org/charsets/iso-8859-1
* https://www.charset.org/charsets/windows-1252

## About me
I make games and pixel art, I have developed for PC and old video games like Nintendo Game Boy and Sega Master System.

You can find some of my games here:
* https://rodrigocard.itch.io/

Social media links:
* https://x.com/RodrigoRodrigoR
* https://bsky.app/profile/rodrigorodrigor.bsky.social


You can also find me on #gbdev, #gbdk2020 and #gbstudio discord.