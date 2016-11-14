import argparse
import readline

from tab_complete import SimpleCompleter
from repl import REPL

__version__ = '1.0.5'


def main():
    parser = argparse.ArgumentParser(description='Todoo Description...')
    parser.add_argument('--use', help='Choose a list to use')

    # Parse the arguments for initial load
    args = parser.parse_args()

    # Print the banner
    REPL.banner()

    # Establish the main REPL object
    repl = REPL(args.use)

    # Register our completer function
    readline.set_completer(SimpleCompleter(repl.get_options()).complete)

    # Use the tab key for completion
    readline.parse_and_bind('tab: complete')

    # Start the event loop
    repl.start()


if __name__ == '__main__':
    main()
