"""
The entrypoint. Calls functions to compile the program.
"""
import argparse

from astro_file import AstroFile
from tokenizer import Tokenizer

__author__  = 'xyLotus, bellrise'


def main():
    """Collect command line arguments and call the functions. """

    parser = argparse.ArgumentParser(description='Compile Astro source code '
                                     'into bytecode.')
    parser.add_argument('src', help='Path to source code')
    parser.add_argument('--no-err', action='store_true', help='Do not exit '
                        'after errors')

    args = parser.parse_args()

    file = AstroFile(args.src)
    tokenizer = Tokenizer(file)
    tokenizer.tokenize()

    import pprint
    pprint.pp(tokenizer.get_context())


if __name__ == '__main__':
    main()
