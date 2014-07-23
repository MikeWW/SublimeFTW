## Better Sublime

### Manual (in English)

Forked From MikeWW/SublimeFTW, and fix some bugs.

Now it only have one function: 

1. Apply the modify of the find result to the original files.

Usage for the plugin:

After you installed it properly, you can edit your seach result, then you can press the command below to apply the changes to the original files.

OSX: super+shift+r  
Linux/Win: ctrl+shift+r  

### 中文版说明

目前只有一个功能：

把你在sublime搜索结果中的修改应用到原始文件中。

在你正确安装完该插件，你可以编辑你的搜索结果，然后按下对应快捷键就可以把搜索结果中的修改应用到原始的文件中。

对应快捷建如下：

OSX: super+shift+r  
Linux/Win: ctrl+shift+r  

----------------------------------Oringinal README below this line--------------------------------

## SublimeFTW - Misc Sublime Text 2 Packages
https://github.com/MikeWW/SublimeFTW

Sublime is quickly becoming a key part of my programming workflow so I'm putting my packages and tweaks up here for easy access. Everything here is pretty much written about 30 minutes after I think of it. You have been warned!

Comments/requests/suggestions welcome!

I am used to a very different naming convention than the Sublime Test standard (never mind C++ rather than Python) so excuse the schizophrenic naming. Maybe one day I'll tidy it up :-) 

Downloads (see below for info):  
> FindUtils : https://github.com/downloads/MikeWW/SublimeFTW/FindUtils.sublime-package

-MikeW, 2012  
mike-at-mikesspace.net


### Current Contents:

#### FindUtils:
!! Currently only properly tested on OSX

##### apply_find_changes \<Mode\>
OSX: super+shift+r  
Linux/Win: ctrl+shift+r  

Where \<Mode\> is one of the following strings:  
* "LastFindResults" (the default)  
* "CursorFindResult"  

This command moves changes you have made in the Find Results pane into the corresponding files. Super useful when refactoring large codebases :-)

Edited source files are left open in Sublime with changed
lines marked for review before you save them.

You should call this when you have the Find Results panel visible and active.

If _Mode == "LastFindResult": The last find result block in the results panel is used.  
If _Mode == "CursorFindResult": The find results block containing the cursor is used.  

##### go_to_found_line
OSX: ctrl+super+l  
Linux/Win: ctrl+alt+l  

Call this when you have the caret over a line in the Find Results pane and it will take you to that line in the source file.
