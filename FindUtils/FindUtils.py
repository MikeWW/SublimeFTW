# FindUtils
# https://github.com/MikeWW/SublimeFTW

import sublime, sublime_plugin
import re

# Cache some useful RegExps...
RegExpString_Path = ""
if sublime.platform() == "windows":
	#So, this should really be much more complex to take into account UNC paths etc...
	RegExpString_Path = "([a-zA-Z]\:[^:]*):$"
else:
	RegExpString_Path = "(\/[^:]*):$"
RegExp_Path = re.compile(RegExpString_Path)
RegExp_ML_Path = re.compile(RegExpString_Path, re.MULTILINE)

# TODO: Localization?
RegExp_ML_FindResultsHeader = re.compile("Searching [0-9]+ files for \".*\"", re.MULTILINE)
RegExp_FindResultsHeader = re.compile("Searching [0-9]+ files for \".*\"")

RegExp_ML_FindResultsFooter = re.compile("1 match in 1 file|[0-9]+ matches in 1 file|[0-9]+ matches across [0-9]+ files", re.MULTILINE)

# Used when we defer making changes to a view because it's file is loading.
lPendingViewChanges = {}

def extractLastFindResults(_Input):
	"""
		Extracts the last block of find results from a string.

		Returns None if it cannot find a find result block.
	"""
	Match = None
	for Match in RegExp_ML_FindResultsHeader.finditer(_Input):
		pass
	if Match == None:
		print("NoMatch")
		return None;
	
	StartPos = Match.start(0)

	Match = RegExp_ML_FindResultsFooter.search(_Input, StartPos);

	if Match == None:
		return None;

	EndPos = Match.end(0)

	return _Input[StartPos:EndPos]	


def extractFindResultsContainingCursor(_Input, _iCursor):
	"""
		Given a string and a cursor position within that string (in chars),
		extracts the find result block that the cursor resides within.
	"""
	Match = None
	StartPos = -1;

	for Match in RegExp_ML_FindResultsHeader.finditer(_Input):
		if Match.start(0) < _iCursor:
			StartPos = Match.start(0)
			pass
		else:			
			break

	if StartPos == -1:
		return None;

	_iCursor = _iCursor - StartPos
		
	Match = None
	for Match in RegExp_ML_FindResultsFooter.finditer(_Input, StartPos):
		pass
	if Match == None:
		return None;

	EndPos = Match.end(0)

	return _Input[StartPos:EndPos], _iCursor

def getCursorEncodedFile(_Input, _iCursor):
	"""
		Given a string containing one or more find results block,
		finds the filename and line number that corresponds to the 
		line the cursor is on.

		Returns None if it could not find the required info.
		Returns a row-encoded filename string "<filename>:<row>" otherwise.
	"""
	Match = None
	StartPos = -1;

	Filename = ""

	for Match in RegExp_ML_Path.finditer(_Input):
		if Match.start(0) < _iCursor:
			StartPos = Match.start(0)
			Filename = Match.group(1)
			pass
		else:			
			break

	if StartPos == -1:
		return None;

	_iCursor = _iCursor - StartPos

	_Input = _Input[StartPos:len(_Input)]

	iCurCharCount = 0;

	for CurLine in _Input.splitlines():
		iCurCharCount = iCurCharCount + len(CurLine)
		if iCurCharCount >= _iCursor:
			Match = re.match( " *([0-9]+)(?:(?:\: )|(?:  ))", CurLine);
			if Match != None:
				return Filename + ":" + Match.group(1)
			else:
				return None

def parseFindChanges(_Input):
	"""
		Given a string containing one find result blocks it returns:
			{
				"<Filename": 
					{
						"<line#>": "<NewLineText>",
						. . .
					},
				. . .
			}

		Line numbers are strings to aid passing through to another command.
	"""
	lFindResults = _Input.splitlines();

	if len(lFindResults) < 2:
		return {}

	Match = re.match("^Searching [0-9]+ files for \".*\"$", lFindResults[0])

	if Match == None:		
		return {};
			
	Mode_LookingForFile = 0;
	Mode_ParsingChanges = 1;

	Mode = Mode_LookingForFile;

	lFilesToChange = {}

	CurFileName = "";
	lCurFileChanges = {};

	for CurLine in lFindResults:
		if Mode == Mode_LookingForFile:
			Match = re.match(RegExp_Path, CurLine);
			if Match != None:
				CurFileName = Match.group(1);
				lCurFileChanges = {};
				Mode = Mode_ParsingChanges;
		elif Mode == Mode_ParsingChanges:
			if CurLine == "":
				lFilesToChange[CurFileName] = lCurFileChanges;
				Mode = Mode_LookingForFile;
			else:
				Match = re.match(" *([0-9]+)(?:(?:\: )|(?:  ))(.*)$", CurLine);
				if Match != None:
					lCurFileChanges[str(int(Match.group(1)) - 1)] = Match.group(2);
	# Finish the last files changes.
	if Mode == Mode_ParsingChanges:
		lFilesToChange[CurFileName] = lCurFileChanges;

	return lFilesToChange;


class ApplyFindChangesListener(sublime_plugin.EventListener):
	"""
		Used to apply changes that were deferred due to files being loaded.
	"""
	def on_load(self, view):
		FileName = view.file_name();
		if FileName != None:
			if FileName in lPendingViewChanges:
				lChanges = lPendingViewChanges[FileName]
				if lChanges != None:
					lPendingViewChanges[FileName] = None;
					view.run_command("apply_find_changes_in_file", { "_lChanges": lChanges, "_bCloseIfUntouched": True });


class ApplyFindChangesCommand(sublime_plugin.WindowCommand):
	"""
		apply_find_changes <Mode>
			
		Where <Mode> is one of: "LastFindResults", "CursorFindResult" (a string)

		This command moves changes you have made in the Find Results pane into the corresponding files. Super useful when refactoring large codebases :-)

		Edited source files are left open in Sublime with changed
		lines marked for review before you save them.

		You should call this when you have the Find Results panel visible and active.

		If _Mode == "LastFindResult":
			The last find result block in the results panel is used.
		If _Mode == "CursorFindResult"
			The find results block containing the cursor is used.
	"""
	def run(self, _Mode = "LastFindResult"):
		view = self.window.active_view();
		if view == None:
			return

		InputText = view.substr(sublime.Region(0, view.size()));
		FindResultBlock = None

		#if _Mode == "LastFindResult":
		FindResultBlock = extractLastFindResults(InputText);
		#elif _Mode == "CursorFindResult":
		#	FindResultBlock = extractFindResultsContainingCursor(InputText, view.sel()[0].begin());

		if FindResultBlock == None:
			return

		lFilesToChange = parseFindChanges(FindResultBlock);
		if lFilesToChange != None:
			lOriginalViews = self.window.views();
			self.lOriginalViewIDs = set()
			for CurView in lOriginalViews:
				self.lOriginalViewIDs.add(CurView.id())

			self.applyChanges(lFilesToChange, self.window)

		self.lOriginalViewIDs = set();

	def applyChanges(self, _lFilesToChange, _Window,):
		for CurFilename, lChanges in _lFilesToChange.iteritems():
			lPendingViewChanges[CurFilename] = lChanges;
			CurFileView = _Window.open_file(CurFilename);
			if CurFileView.id() in self.lOriginalViewIDs:
				CurFileView.run_command("apply_find_changes_in_file", { "_lChanges": lChanges, "_bCloseIfUntouched": False });
				lPendingViewChanges[CurFilename] = None;


class ApplyFindChangesInFileCommand(sublime_plugin.TextCommand):
	"""
		Used internally by ApplyFindChangesCommand
	"""
	def run(self, edit, _lChanges, _bCloseIfUntouched):
		lLineRegions = []
		for ChangeLine, ChangeText in _lChanges.iteritems():
			LineRegion = self.replaceLineIfDifferent(edit, self.view, int(ChangeLine), ChangeText);
			if LineRegion != None:
				lLineRegions.append(LineRegion)
		if lLineRegions != []:
			self.view.add_regions("ApplyFindChanges", lLineRegions, "mark", "bookmark", sublime.HIDDEN);
		elif _bCloseIfUntouched == True:
			if self.view.window != None:
		#		self.view.window().focus_view(self.view)
				self.view.window().run_command("close_file")

	def replaceLineIfDifferent(self, _Edit, _View, _iLine, _Text):
		LineStart = _View.text_point(_iLine, 0)
		LineRegion = _View.line(LineStart)
		
		if _View.substr(LineRegion) != _Text:
			_View.replace(_Edit, LineRegion, _Text)
			return LineRegion
		else:
			return None

class GoToFoundLineCommand(sublime_plugin.TextCommand):
	"""
		Call this when you have the caret over a line in the Find Results pane and it will take you to that line in the source file.
	"""
	def run(self, edit):
		InputText = self.view.substr(sublime.Region(0, self.view.size()));
		EncodedFilename = getCursorEncodedFile(InputText, self.view.sel()[0].begin())
		if EncodedFilename != None:
			self.view.window().open_file(EncodedFilename, sublime.ENCODED_POSITION)

