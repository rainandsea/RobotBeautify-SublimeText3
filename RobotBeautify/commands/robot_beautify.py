# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re
from .content_process import ContentProcess


class RobotBeautifyCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file_name = self.view.file_name()
        full_region = sublime.Region(0, self.view.size())

        if not file_name.endswith('.robot'):
            sublime.status_message("ctrl + alt + l only works for .robot file")
            return None

        obj = ContentProcess(self.view)
        obj.run()
        settings = obj.settings
        suite_v = obj.suite_v
        case_names = obj.case_names
        keywords = obj.keywords
        s_contents = obj.s_contents
        v_contents = obj.v_contents
        t_contents = obj.t_contents
        k_contents = obj.k_contents
        s = obj.s
        v = obj.v
        t = obj.t
        k = obj.k
        s_max_length = max([len(s) for s in settings]) if settings else 0
        v_max_length = max([len(v) for v in suite_v]) if suite_v else 0
        self.bs = ' '

        # format blank space and alignment
        content_s = self.__format_s_or_v(s_contents, s_max_length)
        content_v = self.__format_s_or_v(v_contents, v_max_length)
        content_t = self.__format_t_or_k(t_contents)
        content_k = self.__format_t_or_k(k_contents)

        content_all = ''
        if content_s:
            content_s = s + '\n' + content_s + '\n'
            content_all += content_s
        if content_v:
            content_v = v + '\n' + content_v + '\n'
            content_all += content_v
        if content_t:
            content_t = t + '\n' + content_t + '\n'
            content_t = self.__format_other_var(suite_v, content_t)
            content_all += content_t
        if content_k:
            content_k = k + '\n' + content_k + '\n'
            content_k = self.__format_other_var(suite_v, content_k)
            content_all += content_k

        content_all = self.__format_suite_var(suite_v, content_all)
        # content_all = self.__format_other_var(var_upper, content_all)
        content_all = self.__format_case_name(case_names, content_all)
        content_all = self.__format_keywords(keywords, content_all)

        self.view.replace(edit, full_region, content_all)
        self.view.erase_regions('warning')

    def __format_s_or_v(self, content_list, max_length):
        if not content_list:
            return None
        content = ''
        for line in content_list:
            for index, item in enumerate(line):
                if index == 0:
                    content += item
                elif index == 1:
                    content = content + self.bs * \
                        (max_length + 4 - len(line[0])) + item
                else:
                    content = content + self.bs * 4 + item
            content += '\n'
        return content

    def __format_t_or_k(self, content_list):
        if not content_list:
            return None
        content = ''
        name_num = 0
        for line in content_list:
            if line[-1] is True:  # case name or keyword name
                name_num += 1
                # if name_num is big than 1, insert a '\n' before this line
                if name_num > 1:
                    content += '\n' + line[0]
                else:
                    content += line[0]
            else:
                for item in line:
                    content = content + self.bs * 4 + item
            content += '\n'
        return content

    def __format_suite_var(self, suite_v, content):
        for v in suite_v:
            content = content.replace(
                v[1:], v[1:].upper().replace(' ', '_').replace('-', '_'))
        return content

    def __format_other_var(self, suite_v, content):
        all_var = re.findall(r'[\$@&]\{[a-zA-Z0-9_-]*\}', content)
        suite_v = [v[1:] for v in suite_v]  # &{val} and @{val} maybe used like ${val}
        for var in all_var:
            if var[1:] not in suite_v:
                content = content.replace(var, var.replace('-', '_').lower())
        return content

    def __format_case_name(self, names, content):
        for name in names:
            s = name.replace('-', '_').replace(' ', '_')
            s = '_'.join([w[0].upper() + w[1:] for w in s.split('_')])
            content = content.replace(name, s)
        return content

    def __format_keywords(self, keywords, content):
        for kw in keywords:
            if '.' in kw:
                kw = kw.split('.')[-1]
            words = kw.replace('_', ' ').replace('-', ' ').split()
            res = ' '.join([w[0].upper() + w[1:] for w in words])
            content = content.replace(kw, res)
        return content
