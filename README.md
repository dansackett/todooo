# Todooo

Todooo is a super simple list management REPL which allows you to create and
manage lists of data easily. Everyone has their own style of working with lists
and this is my preferred style of doing so.

Currently, all lists will exist in the `~/.todooo/` directory and will be
stored as `.txt` files meaning they can be edited outside of the application if
you want.

## Installation

Installation can be done via PyPI and it's suggested to install globally.

```
pip install todooo
```

## Usage

Todooo works simply by typing `todooo` from the terminal. However you can
preload an existing list into the shell by using the `--use` flag with the
command like so:

```
todooo --use <LIST NAME>
```

Once inside the application, you have the following options:

| Command   | Description                                       | Arguments                     |
|-----------|---------------------------------------------------|-------------------------------|
| `add`     | Add a new item to the current list                | <ITEM CONTENT>                |
| `del`     | Delete an item from the current list              | <ITEM ID>                     |
| `exit`    | Exit the application                              | -                             |
| `help`    | Show the command menu                             | -                             |
| `lists`   | Show all available lists                          | -                             |
| `move`    | Move an item in the current list                  | <FROM ITEM ID> <TO ITEM ID>   |
| `new`     | Create a new list                                 | <LIST NAME>                   |
| `replace` | Replace an item in the current list with another  | <ITEM ID> <NEW ITEM CONTENT>  |
| `rmlist`  | Remove an existing list                           | <LIST NAME>                   |
| `show`    | Show the current list items                       | -                             |
| `use`     | Set the current list                              | <LIST NAME>                   |
