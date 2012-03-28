## SublimeFTW - Misc Sublime Text 2 Packages
https://github.com/MikeWW/SublimeFTW

Sublime is quickly becoming a key part of my programming workflow so I'm putting my packages and tweaks up here for easy access. Everything here is pretty much written about 30 minutes after I think of it. You have been warned!

Comments/requests/suggestions welcome!

I am used to a very different naming convention than the Sublime Test standard (never mind C++ rather than Python) so excuse the schizophrenic naming. Maybe one day I'll tidy it up :-) 

-MikeW, 2012
mike-at-mikesspace.net


### Current Contents:

#### FindUtils:
!! Currently only properly tested on OSX

##### apply_find_changes <Mode>
OSX: super+shift+r
Linux/Win: ctrl+shift+r

Where <Mode> is one of the following strings:
 * "LastFindResults" (the default)
 * "CursorFindResult"

This command moves changes you have made in the Find Results pane into the corresponding files. Super useful when refactoring large codebases :-)

Edited source files are left open in Sublime with changed
lines marked for review before you save them.

You should call this when you have the Find Results panel visible and active.

If _Mode == "LastFindResult":
	The last find result block in the results panel is used.
If _Mode == "CursorFindResult"
	The find results block containing the cursor is used.

##### go_to_found_line
OSX: ctrl+super+l
Linux/Win: ctrl+alt+l

Call this when you have the caret over a line in the Find Results pane and it will take you to that line in the source file.
