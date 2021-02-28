# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from .content_process import ContentProcess
from .settings import ROBOT_WARNINGS, W


class RobotCheckCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        obj = ContentProcess(self.view)
        obj.run()
        settings = obj.settings
        suite_v = obj.suite_v
        case_names = obj.case_names
        keywords = obj.keywords
        self_keywords = obj.self_keywords
        too_long_pos = obj.too_long_pos
        print('keywords count:', len(self_keywords))

        ROBOT_WARNINGS.clear()
        self.warnings = []
        self.__get_warning_pos(settings, 0)
        self.__get_warning_pos(suite_v, 1)
        self.__get_warning_pos(case_names, 2)
        self.__get_warning_pos(keywords, 3)
        self.__is_self_kw_used(self_keywords, case_names)

        self.warnings.extend(too_long_pos)
        for pos in too_long_pos:
            ROBOT_WARNINGS.append([W[8], self.__get_line(pos)])

        self.view.erase_regions('warning')
        self.view.add_regions('warning',
                              self.warnings,
                              'string',
                              'dot',
                              flags=sublime.HIDDEN)
        print('warnings:\n', ROBOT_WARNINGS)

    def __get_warning_pos(self, names, index):
        pos = sublime.Region(0, 0)
        for name in names:
            pos = self.view.find(name, pos.b, flags=sublime.LITERAL)
            if index == 0:
                res, msg = self.__is_set_name_recommend(name)
                if not res:
                    self.warnings.append(pos)
                    line = self.__get_line(pos)
                    ROBOT_WARNINGS.append(
                        [name + ' ' + msg, line])
            if index == 1:
                res, msg = self.__is_var_recommend(name)
                if not res:
                    self.warnings.append(pos)
                    line = self.__get_line(pos)
                    ROBOT_WARNINGS.append(
                        [name + ' ' + msg, line])
            if index == 2:
                res, msg = self.__is_case_name_recommend(name)
                if not res:
                    self.warnings.append(pos)
                    line = self.__get_line(pos)
                    ROBOT_WARNINGS.append(
                        [name + ' ' + msg, line])
            if index == 3:
                res, msg = self.__is_keyword_recommend(name)
                if not res:
                    self.warnings.append(pos)
                    line = self.__get_line(pos)
                    ROBOT_WARNINGS.append(
                        [name + ' ' + msg, line])

    def __is_set_name_recommend(self, name):
        if name == '...':
            return True, None
        if not name.istitle():
            return False, W[3]
        return True, None

    def __is_var_recommend(self, var):
        if '-' in var:
            return False, W[0]
        if ' ' in var:
            return False, W[2]
        if not var.isupper():
            return False, W[4]
        return True, None

    def __is_case_name_recommend(self, case_name):
        if len(case_name) >= 150:
            return False, W[8]
        if ' ' in case_name:
            return False, W[2]
        if '-' in case_name:
            return False, W[0]
        if sum([True for c in '~!@#$%^&*(){}:"<>?|`[];,./+=' if c in case_name]) > 0:
            return False, W[6]
        for word in case_name.split('_'):
            if word[0].islower():
                return False, W[3]
        return True, None

    def __is_keyword_recommend(self, keyword):
        if keyword.isdigit():
            return True, None
        if '.' in keyword and '...' not in keyword:
            keyword = keyword.split('.')[-1]
        if '_' in keyword:
            return False, W[1]
        if '-' in keyword:
            return False, W[0]
        for word in keyword.split():
            if word[0].islower():
                return False, W[3]
        spk = ['comment',
               # 'run keyword and ignore error'
               ]
        if keyword.lower() in spk:
            return False, W[5]
        return True, None

    def __get_line(self, pos):
        cur_line, cur_col = self.view.rowcol(pos.begin())
        return cur_line + 1

    def __get_view_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def __is_self_kw_used(self, self_kw, case_names):
        if not case_names:
            return None
        content = self.__get_view_content()
        pos = sublime.Region(0, 0)
        for kw in self_kw:
            if content.count(kw) == 1:
                pos = self.view.find(kw, pos.b, flags=sublime.LITERAL)
                line = self.__get_line(pos)
                self.warnings.append(pos)
                ROBOT_WARNINGS.append([kw + ' ' + W[7], line])
