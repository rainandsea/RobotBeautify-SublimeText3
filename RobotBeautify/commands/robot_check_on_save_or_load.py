import sublime
import sublime_plugin


class RobotCheckOnSaveOrLoad(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        if view.file_name().endswith('.robot'):
            view.run_command('robot_check')

    def on_load(self, view):
        if view.file_name().endswith('.robot'):
            view.run_command('robot_check')
