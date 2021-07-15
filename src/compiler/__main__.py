"""
The entrypoint. Calls functions to compile the program.
"""
import argparse

import ac_parser
from astro_file import AstroFile
from tokenizer import Tokenizer

__author__  = 'xyLotus, bellrise'


def main():
    """Collect command line arguments and call the functions. """

    parser = argparse.ArgumentParser(description='Compile Astro source code '
                                     'into bytecode.')  
    parser.add_argument('src', help='Path to source code')
    parser.add_argument('--noerr', action='store_true', help='Catches all errors'
                        'at compilation runtime')

    args = parser.parse_args()

    file_obj = AstroFile(args.src)
    tokenizer = Tokenizer(file_obj)
    tokenizer.tokenize()
    print(tokenizer.tokens)

    from pprint import pp
    parsed = ac_parser.Parser(args.src, tokenizer.get_context())
    pp(parsed.parse())


if __name__ == '__main__':
    main()
