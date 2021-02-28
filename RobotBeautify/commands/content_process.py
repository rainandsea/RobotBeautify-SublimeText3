# -*- coding: utf-8 -*-
import sublime


class ContentProcess(object):
    def __init__(self, view):
        self.view = view
        self.settings = []
        self.suite_v = []
        self.case_names = []
        self.keywords = []
        self.self_keywords = []
        self.s_contents = []
        self.v_contents = []
        self.t_contents = []
        self.k_contents = []
        self.bs = ' '
        self.s = '*** Settings ***'
        self.v = '*** Variables ***'
        self.t = '*** Test Cases ***'
        self.k = '*** Keywords ***'
        self.up_down = [
            'Suite Setup',
            'Suite Teardown',
            'Test Setup',
            'Test Teardown',
            '[Setup]',
            '[Teardown]'
        ]
        self.too_long_pos = []
        self.suite_v.extend(['${EMPTY}', '${CURDIR}', '${SPACE}'])

    def run(self):
        full_region = sublime.Region(0, self.view.size())

        # Define some variables used later

        L = [self.s.lower(), self.v.lower(), self.t.lower(), self.k.lower()]
        cur_index = 0  # from 0 to 3 mapping to s, v, t, k

        input_line_regions = self.view.lines(full_region)

        for reg in input_line_regions:
            line_text = self.view.substr(reg)
            if len(line_text) >= 150:
                self.too_long_pos.append(reg)

            if line_text.strip().lower() in L:
                cur_index = L.index(line_text.strip().lower())
                continue

            # Settings
            if cur_index == 0:
                text_list = self.__get_text_list(line_text)
                if text_list:
                    self.s_contents.append(text_list)
                    self.settings.append(text_list[0])
                    if text_list[0].title() in self.up_down:
                        self.keywords.extend(self.__get_keywords(text_list[1:]))

            # Variables
            if cur_index == 1:
                text_list = self.__get_text_list(line_text)
                if text_list:
                    self.v_contents.append(text_list)
                    if text_list[0] != '...':
                        self.suite_v.append(text_list[0])

            # Test Cases
            if cur_index == 2:
                if self.__is_case_name(line_text):
                    self.case_names.append(line_text.strip())
                    self.t_contents.append([line_text.strip(), True])
                    continue
                text_list = self.__get_text_list(line_text)
                if text_list:
                    self.t_contents.append(text_list)
                    if text_list[0].title() in self.up_down or text_list[0][0] not in '[.':
                        self.keywords.extend(self.__get_keywords(text_list))
            # Keywords
            if cur_index == 3:
                if len(line_text) > 0 and not line_text.startswith(self.bs) and not line_text.startswith('#'):
                    self.keywords.append(line_text.strip())
                    self.self_keywords.append(line_text.strip())
                    self.k_contents.append([line_text.strip(), True])
                    continue
                text_list = self.__get_text_list(line_text)
                if text_list:
                    self.k_contents.append(text_list)
                    if text_list[0].title() in self.up_down or text_list[0][0] not in '[.':
                        self.keywords.extend(self.__get_keywords(text_list))

    def __get_text_list(self, line_text):
        text_list = line_text.split(self.bs * 2)
        text_list = self.__remove_blank_spaces(text_list)
        return text_list

    def __remove_blank_spaces(self, text_list):
        new_text_list = []
        for item in text_list:
            if item:
                new_text_list.append(item.strip())
        return new_text_list if new_text_list else None

    def __is_case_name(self, line_text):
        if len(line_text) > 0 and not line_text.startswith(self.bs) and not line_text.startswith('#'):
            return True
        return False

    def __is_keyword(self, item):
        if item[0].isdigit():
            return False
        if item in ['_', ';', '.', '\\', '\n', '...']:
            return False
        for char in ['=', '$', '@', '&', ':', '[', ']', '\\', '|', '/', '%', '*', '^']:
            if char in item:
                return False
        return True

    def __get_keywords(self, text_list):
        """
        text_list is not empty
        """
        specialKW = [
            'run keyword',
            'run keyword and continue on failure',
            'run keyword and expect error',
            'run keyword and ignore error',
            'run keyword and return'
            'run keyword and return if',
            'run keyword and return status',
            'run keyword if',
            'run keyword if all critical tests passed',
            'run keyword if all tests passed',
            'run keyword if any critical tests failed',
            'run keyword if any tests failed',
            'run keyword if test failed',
            'run keyword if test passed',
            'run keyword if timeout occurred',
            'run keyword unless',
            'run keywords',
            'wait until keyword succeeds',
            'repeat keyword',
            'else'
        ]
        specialSettings = [
            '[Arguments]',
            '[Documentation]'
        ]
        L = []
        if text_list[0] in specialSettings:
            return L
        for item in text_list:
            if self.__is_keyword(item):
                L.append(item)
                if not item.replace('_', ' ').replace('-', ' ').lower() in specialKW:
                    break
        return L
