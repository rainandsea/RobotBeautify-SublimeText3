# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from .settings import ROBOT_WARNINGS


class RobotErrorsCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('start show robot errors...')
        if self.window.active_view().file_name().endswith('.robot'):
            self.options = [[w[0], 'line: %s' % w[1]]
                            for w in sorted(ROBOT_WARNINGS, key=lambda c: c[1])]
            self.window.show_quick_panel(self.options, self.__jump)

    def __jump(self, item: int) -> None:
        if item == -1:
            return
        lineno = int(self.options[item][1].split(':')[1].strip())
        pt = self.window.active_view().text_point(lineno - 1, 0)
        self.window.active_view().sel().clear()
        self.window.active_view().sel().add(sublime.Region(pt))

        self.window.active_view().show(pt)
