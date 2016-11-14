import os

import config
import errors
import validators


class SimpleList(object):
    """A SimpleList handles the logic for operating and saving a list"""

    def __init__(self, path, dirty=False):
        self.path = path
        self.name = path
        self.items = []
        self.clean = not dirty

        self.load_items()

    def __len__(self):
        """Get the length of the list's items"""
        return len(self.items)

    def __str__(self):
        """Print the list's contents"""
        output = ''
        for idx, item in enumerate(self.items, 1):
            output += ' %s. %s\n' % (idx, item)
        return output

    def load_items(self):
        """Load the items from the file into memory"""
        if not os.path.exists(self.path):
            f = open(self.path, 'w')
            f.close()

        with open(self.path) as f:
            lines = []
            for line in f.readlines():
                lines.append(line[len(config.LINE_PREFIX):-len(config.LINE_SUFFIX)])

            self.items = lines
            self.name = self.path[len(config.ROOT_PATH):-len(config.FILE_EXTENSION)]

    def save(self):
        """Write the list items to its file"""
        with open(self.path, 'w+') as f:
            for line in self.items:
                f.write('%s%s%s' % (config.LINE_PREFIX, line, config.LINE_SUFFIX))

    def remove(self):
        """Write the list items to its file"""
        os.remove(self.path)

    def print_name(self):
        """Print the name of the list"""
        print ' %s%s' % (config.LINE_PREFIX, self.name)

    def mark_dirty(self):
        """Set the list to dirty"""
        self.clean = False

    def is_dirty(self):
        """Check if the list is dirty"""
        return not self.clean

    def add(self, args):
        """Add a new item to the list"""
        text = ' '.join(args)

        if text == '':
            raise errors.InvalidArgumentError

        self.items.append(text)
        self.mark_dirty()

    @validators.validate_num_arguments_gt(2)
    def replace(self, args):
        """Replace an item in the list"""
        text = args[1:]

        idx = validators.parse_index(self, args[0])

        self.items[idx] = ' '.join(text)
        self.mark_dirty()

    @validators.validate_num_arguments_eq(1)
    def delete(self, args):
        """Delete an item from the list"""
        idx = validators.parse_index(self, args[0])

        self.items.pop(idx)
        self.mark_dirty()

    @validators.validate_num_arguments_eq(2)
    def move(self, args):
        """Move an item in the list to another space"""
        from_idx = validators.parse_index(self, args[0])
        to_idx = validators.parse_index(self, args[1])

        if from_idx == to_idx:
            raise errors.SameItemError

        self.items[from_idx], self.items[to_idx] = self.items[to_idx], self.items[from_idx]
        self.mark_dirty()
