==========================

Bleep

--------------------------

Game Boy Dev Compo Version

(prerelease / alpha)

--------------------------

by Andrew G. Crowell

==========================


A music maker for the Game Boy.


Introduction
------------

Bleep is a music creation program with piano roll interface.

It lets you jam out chip music really quickly, and it writes directly into save
memory, so your work is saved automatically. This is not the final version, but
I was reminded the Game Boy dev compo was going on, so I'd.

This is just a prerelease, the final will include source code, and add many
missing features to the editor.


Controls
--------

Up/Down/Left/Right (tap) = move cursor once
Up/Down/Left/Right (hold) = move cursor quickly
A (on empty cell) = draw new note. hold A and drag to make longer/shorter notes.
A (on current note) = truncate/remove note, draws new note if dragged.
Start = play from beginning
Select + Left/Right = select channel
Select + Start = play from current measure


HUD
---

+---+-----------+---+
|   |           | c |
|   |           +---+
| a |     b         |
|   |           +---+
|   |           | d |
+---+-----------+---+

a = Piano
b = Music Sheet
c = Channel Selector
d = Measure Counter

-- Piano --

Visually represents the pitch of the notes in music sheet


-- Music Sheet --

This space represents the music score itself.

The grid is horizontally divided into 4 notes per beat, 4 beats per measure,
for a total of 2048 notes (or 128 measures). The grid also divided vertically,
one row per note, separated into octaves. Sharp notes are shaded differently to
help you out.

You can place notes here to make music. Channels are monophonic, so each column
of the music sheet can contain a single note.

- Press the directions to move around the music sheet.
- Press A to place notes or delete notes on the music sheet.
  You can hold A and move around to make longer/shorter notes.


-- Channel Selector --

There are four channels.

P1 = Pulse 1
P2 = Pulse 2
W = Wave
N = Noise

There are currently preset instruments for each of the channels, that can't be
changed. In the final release this will be customizable.

- Pulse 1 is "flute"-like.
- Pulse 2 is "piano" or "harp" like.
- Wave is initialized to a 4-bit square wave:

  00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF

- Noise is sort of "snare"-like. It also doesn't have a conventional pitch.
  Currently you can affect what "divisor" is used by the noise channel
  which uses the note number modulo 8, but that's all at the moment.

  I plan to make noise use a customizable drumkit
  (where each note is a different drum), but it's not there yet.

- Hold Select and press Left/Right to switch the channel shown in the editor.


-- Measure Counter --

Shows the current measure number being viewed in the song.
There are 16 notes, or 4 beats per measure.

- Hold Select and press Start to play starting from the current measure


Known Issues
------------

- If you drag a note that crosses a 256-byte boundary, it will currently
  stop redrawing the note preview until you let go of the note.
- Note placement acts funky at column 2047, the final column of the song.


Planned Features
----------------

- Quick navigation
- Vertical camera panning during playback
- Playback step forward
- Note effects
- Copy/paste
- Instrument editor
- Speed/tempo editor, including tempo modes, like swing timing, etc.
- and more!



