""" The main file is the entrypoint for execution of astro,
the where all the dev intended execution order takes places. """

# Local
from astro_types import TokenType
from astro_file import AstroFile
from tokenizer import Tokenizer

import argparse_config


__author__ = 'xyLotus'
__version__ = '0.0.5'
__status__ = 'Work In Progess'

# Command-line Argument Vector Handling
argparse_config.init_parse()
argv = argparse_config.get_argv()

# NOTE Any argument handles (argv.arg_name)
#      will be written below this comment


# Main functionality post-argument parsing
# seperator
print()

file_handle = AstroFile(
    file_name="astro_code.txt", 
    cleanup=False
)

tokenizer = Tokenizer(
    h_file=file_handle
)
tokenizer.tokenize()
tokenizer.compress(token_id = TokenType.SYM)

# seperator
print()
