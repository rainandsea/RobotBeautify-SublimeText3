# Robot Beautify

RobotBeautify-SublimeText3 is plugin for Sublime-Text3, which can support .robot files check and foramt based on some rules.
For now, this plugin needs to work with RobotFrameworkAssistant which is also a very useful plugin for .robot file and provide color-markers.

More infos about RobotFrameworkAssistant: https://github.com/andriyko/sublime-robot-framework-assistant/

If just want to use Robot Beautify functions, you just need to install the RobotFrameworkAssistant with no personal settings, and put RobotBeautify directory to your ..\Sublime Text 3\Packages.

1.Remove redundant blank spaces (make sure four blank spaces between keywords, tags...)
2.Suite variable check and format (recommend all upper case in suite variable)
3.Test case name check and format (recommend first char is upper case in words, and joined with underline _)
4.Other variable format (recommend all lower case, joined with underline _)
5.Keywords check and format (recommend first char is upper case in words, and joined with underline _)
6.self-defined kw not used check (recommend if not used then do not write)
7.Special keyword check (recommend not use Comment, Run Keyword And Ignore Error)
8.line code length check (recommend each line not longer than 150, case name not longer than 100)
9.Warning type show ( the yellow dot show a this line have some problem, and can see what the warning detail)
10.Align with some way in Settings and Variables table.
