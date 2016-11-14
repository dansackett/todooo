import os
import argparse
import readline

from colored import fore, style

import config
import errors
import validators
from list import SimpleList
from tab_complete import SimpleCompleter


class REPL(object):
    """REPL Represents the main Todooo prompt REPL"""
    def __init__(self, list_identifier=None):
        self.lists = []
        self.current_list = None
        self.last_line = None

        self._load_lists()

        if list_identifier is not None:
            try:
                self._handle_use(list_identifier)
            except errors.InvalidListError as e:
                print e
                exit()

    def start(self):
        """Start the REPL event loop and catch any errors"""
        self._run_event_loop()

    def stop(self):
        """Stop the event loop in case of exiting or fatal errors"""
        self._stop_event_loop()

    @staticmethod
    def banner():
        print '  ______          __                  '
        print ' /_  __/___  ____/ /___  ____  ____   '
        print '  / / / __ \/ __  / __ \/ __ \/ __ \\ '
        print ' / / / /_/ / /_/ / /_/ / /_/ / /_/ /  '
        print '/_/  \____/\__,_/\____/\____/\____/   '
        print '\n'
        print 'Todooo helps keep lists of things you want to remember or do.'
        print '\n'
                                    

    @property
    def commands_map(self):
        return {
            'new': {
                'description': 'Create a new list',
                'handler': lambda args: self._handle_new(args),
                'args': '<LIST NAME>',
            },
            'rmlist': {
                'description': 'Remove an existing list',
                'handler': lambda args: self._handle_remove_list(args),
                'args': '<LIST NAME>',
            },
            'use': {
                'description': 'Set the current list',
                'handler': lambda args: self._handle_use(args),
                'args': '<LIST NAME>',
            },
            'add': {
                'description': 'Add a new item to the current list',
                'handler': lambda args: self._handle_add(args),
                'args': '<ITEM CONTENT>',
            },
            'replace': {
                'description': 'Replace an item in the current list with another',
                'handler': lambda args: self._handle_replace(args),
                'args': '<ITEM ID> <NEW ITEM CONTENT>',
            },
            'del': {
                'description': 'Delete an item from the current list',
                'handler': lambda args: self._handle_delete(args),
                'args': '<ITEM ID>',
            },
            'move': {
                'description': 'Move an item in the current list',
                'handler': lambda args: self._handle_move(args),
                'args': '<FROM ITEM ID> <TO ITEM ID>',
            },
            'show': {
                'description': 'Show the current list',
                'handler': lambda args: self._handle_show(args),
                'args': None,
            },
            'lists': {
                'description': 'Show all available lists',
                'handler': lambda args: self._handle_lists(args),
                'args': None,
            },
            'exit': {
                'description': 'Exit Todooo',
                'handler': lambda args: self._handle_exit(args),
                'args': None,
            },
            'help': {
                'description': 'Show the help menu',
                'handler': lambda args: self._handle_help(args),
                'args': None,
            },
        }


    def _print(self, text, error=False):
        """Print using the prompt"""
        if error:
            print '%s%s%s%s%s%s' % (style.DIM, config.PROMPT, style.RESET, fore.RED, text, style.RESET)
        else:
            print '%s%s%s%s%s%s' % (style.DIM, config.PROMPT, style.RESET, fore.GREEN, text, style.RESET)

    def _load_lists(self):
        """Load all created lists into memory"""
        if not os.path.exists(config.ROOT_PATH):
            os.mkdir(config.ROOT_PATH)

        full_path = lambda path: os.path.join(config.ROOT_PATH, path)

        files = [full_path(f) for f in os.listdir(config.ROOT_PATH) if os.path.isfile(full_path(f))]

        for file in files:
            self.lists.append(SimpleList(file))

    def _run_event_loop(self):
        """Run the main event loop parsing input from the user and acting on it"""
        while True:
            try:
                command, args = self._capture_input()

                if command == '':
                    continue

                if command not in self.commands_map:
                    raise errors.InvalidCommandError

                self.commands_map[command]['handler'](args)
            except errors.TodoooError as e:
                self._print(e, error=True)
                self._run_event_loop()
            except (KeyboardInterrupt, SystemExit):
                self._stop_event_loop()

    def _stop_event_loop(self):
        """Stop the event loop and save the changes made to lists"""
        dirty = [lst for lst in self.lists if lst.is_dirty()]
        for lst in dirty:
            lst.save()
        exit()

    def _capture_input(self):
        """Capture and parse the user's input into a distinct command and args"""
        user_data = raw_input(style.DIM + config.PROMPT + style.RESET)

        if len(user_data.split(' ')) == 1:
            return user_data, []

        command, args = user_data.split(' ', 1)
        return command.lower(), args.split(' ')

    def _validate_list_is_selected(self):
        """Ensure that a list is selected to operate on"""
        if self.current_list is None:
            raise errors.NoListError

    @validators.validate_num_arguments_eq(1)
    def _handle_new(self, args):
        """Handle creating a new list"""
        new_path = '%s%s%s' % (config.ROOT_PATH, args[0], config.FILE_EXTENSION)
        new_list = SimpleList(new_path, dirty=True)

        self.lists.append(new_list)
        self._handle_use(new_list.name)

    @validators.validate_num_arguments_eq(1)
    def _handle_remove_list(self, args):
        """Handle removing an existing list"""
        new_path = '%s%s%s' % (config.ROOT_PATH, args[0], config.FILE_EXTENSION)
        new_list = SimpleList(new_path, dirty=True)

        list_idx = None
        to_delete = None
        for idx, lst in enumerate(self.lists):
            if lst.name == args[0]:
                list_idx = idx
                to_delete = lst

        if list_idx is None:
            raise errors.InvalidListError

        self.lists.pop(list_idx)
        self.current_list = None
        to_delete.remove()
        self._print('Successfully deleted list')

    def _handle_use(self, args):
        """Handle setitng the current list"""
        if isinstance(args, list) and len(args) == 1:
            l = args[0]
        elif isinstance(args, basestring):
            l = args
        else:
            raise errors.InvalidArgumentError

        self.current_list = None
        for lst in self.lists:
            if lst.name == l:
                self.current_list = lst

        if self.current_list is None:
            raise errors.InvalidListError

        self._print('You are now using the "%s" list' % l)

    def _handle_add(self, args):
        """Handle adding an item to the current list"""
        self._validate_list_is_selected()
        self.current_list.add(args)
        self._print('Successfully added new line')

    def _handle_replace(self, args):
        """Handle replacing an item in a list"""
        self._validate_list_is_selected()
        self.current_list.replace(args)
        self._print('Successfully replaced line')

    def _handle_delete(self, args):
        """Handle deleting an item in a list"""
        self._validate_list_is_selected()
        self.current_list.delete(args)
        self._print('Successfully deleted line')

    def _handle_move(self, args):
        """Handle moving an item to a new position in the list"""
        self._validate_list_is_selected()
        self.current_list.move(args)
        self._print('Successfully moved lines')

    def _handle_lists(self, args):
        """Handle showing all available lists"""
        if len(self.lists) == 0:
            self._print('You currently have no lists created', error=True)
        else:
            for item in self.lists:
                item.print_name()

    def _handle_show(self, args):
        """Handle showing the list"""
        self._validate_list_is_selected()
        if len(self.current_list) == 0:
            self._print('This list is currently empty', error=True)
        else:
            print self.current_list

    def _handle_exit(self, args):
        """Handle exiting the REPL"""
        self._stop_event_loop()

    def _handle_help(self, args):
        """Handle showing the help menu"""
        for key in sorted(self.commands_map.keys()):
            cmd = self.commands_map[key]
            if cmd['args'] is not None:
                print ' %s - %s (%s)' % (key, cmd['description'], cmd['args'])
            else:
                print ' %s - %s' % (key, cmd['description'])

    def get_options(cls):
        """Get the options available for autocomplete"""
        return sorted(cls.commands_map.keys())
