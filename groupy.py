import os.path

import sublime
import sublime_plugin


PROJECT_NAME = 'Groupy'
PROJECT_KEY = 'groupy'


class GroupySettings:
    def get_system_settings(self, key=None, default=None):
        settings = sublime.load_settings(PROJECT_NAME + '.sublime-settings')

        if key is None:
            return settings

        value = self.get_my_settings(key)
        if value is not None:
            return value

        return settings.get(key, default)

    def set_system_settings(self, key, value):
        settings = self.get_system_settings()
        settings.set(key, value)
        sublime.save_settings(PROJECT_NAME + '.sublime-settings')

    def get_my_settings(self, key=None, default=None):
        project_settings = self.get_project_data()
        my_settings = project_settings.get(PROJECT_KEY, {})

        if not isinstance(my_settings, dict):
            my_settings = {}

        if key is None:
            return my_settings

        return my_settings.get(key, default)

    def set_my_settings(self, key, value):
        project_settings = self.get_project_data()
        my_settings = self.get_my_settings()

        if value is None:
            if key in my_settings:
                del my_settings[key]
        else:
            my_settings[key] = value

        project_settings[PROJECT_KEY] = my_settings

        self.window.set_project_data(project_settings)

    def get_project_data(self):
        data = self.window.project_data()
        if not data:
            data = {}
        return data

class GroupyCommand(sublime_plugin.WindowCommand, GroupySettings):
    def run(self, **kwargs):
        group_names = self.get_my_settings('groups', [])
        if not group_names:
            self.window.run_command('groupy_new')
        else:
            options = []
            for name in group_names:
                options.append(('. Open {}'.format(name), (name,), lambda name: self.open(name)))

            file_name = self.window.active_view().file_name()
            if file_name and group_names:
                options.append(('+ Add {} to…'.format(self.view_name()), (group_names,), lambda group_names: self.add_to(group_names, file_name)))
                options.append(('- Remove {} from…'.format(self.view_name()), (group_names,), lambda group_names: self.remove_from(group_names, file_name)))

            options.append(('! New Group', (), lambda: self.window.run_command('groupy_new')))
            options.append(('! Remove Group', (), lambda: self.window.run_command('groupy_remove')))

            self.window.show_quick_panel([opt[0] for opt in options], lambda choice: self.chose(options, choice))

    def chose(self, options, choice):
        if choice != -1:
            chose = options[choice]
            args = chose[1]
            func = chose[2]
            sublime.set_timeout(lambda: func(*args), 1)

    def view_name(self):
        file_name = self.window.active_view().file_name()
        base_name = os.path.basename(file_name)
        view_name = self.window.active_view().name() or base_name
        return view_name or base_name

    def in_group(self, name, file_name):
        files = self.get_my_settings('files', {}).get(name, [])
        return file_name in files

    def open(self, name):
        sublime.status_message(name)
        files = self.get_my_settings('files', {}).get(name, [])
        for file in files:
            self.window.open_file(file)

    def remove_from(self, group_names, file_name):
        options = []
        for name in group_names:
            files = self.get_my_settings('files', {}).get(name, [])
            if file_name in files:
                options.append(([name, 'Remove {} from {}'.format(self.view_name(), name)], (name,), lambda name: self.remove_from_group(name, file_name)))
        if options:
            self.window.show_quick_panel([opt[0] for opt in options], lambda choice: self.chose(options, choice))
        else:
            sublime.status_message('This file is not in any groups')

    def remove_from_group(self, name, file_name):
        sublime.status_message(name)
        all_files = self.get_my_settings('files', {})
        files = all_files.get(name, [])
        if file_name in files:
            files.remove(file_name)
            self.set_my_settings('files', all_files)
            sublime.status_message('Removed {} from {}'.format(self.view_name(), name))

    def add_to(self, group_names, file_name):
        options = []
        for name in group_names:
            files = self.get_my_settings('files', {}).get(name, [])
            if file_name not in files:
                options.append(([name, 'Add {} to {}'.format(self.view_name(), name)], (name,), lambda name: self.add_to_group(name, file_name)))
        self.window.show_quick_panel([opt[0] for opt in options], lambda choice: self.chose(options, choice))

    def add_to_group(self, name, file_name):
        sublime.status_message(name)
        all_files = self.get_my_settings('files', {})
        files = all_files.get(name, [])

        if file_name not in files:
            files.append(file_name)
            all_files[name] = files
            self.set_my_settings('files', all_files)
            sublime.status_message('Added {} to {}'.format(self.view_name(), name))
        else:
            sublime.status_message('Error: this file is already in this group')


class GroupyNewCommand(sublime_plugin.WindowCommand, GroupySettings):
    def run(self, **kwargs):
        self.window.show_input_panel("Group Name:", '', self.new_name, None, None)

    def new_name(self, name):
        group_names = self.get_my_settings('groups', [])
        group_names.append(name)
        self.set_my_settings('groups', group_names)


class GroupyRemoveCommand(sublime_plugin.WindowCommand, GroupySettings):
    def run(self, **kwargs):
        group_names = self.get_my_settings('groups', [])
        options = []
        for name in group_names:
            options.append('Remove {}'.format(name))
        self.window.show_quick_panel(options, lambda choice: self.remove_name(choice))

    def remove_name(self, choice):
        if choice != -1:
            group_names = self.get_my_settings('groups', [])
            name = group_names[choice]
            del group_names[choice]
            self.set_my_settings('groups', group_names)
            sublime.status_message('Removed group {}'.format(name))
