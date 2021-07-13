""" The main file is the entrypoint for execution of astro,
the where all the dev intended execution order takes places. """

from astro_file import AstroFile
from tokenizer import Tokenizer

__author__ = 'xyLotus'
__version__ = '0.0.5'
__status__ = 'Work In Progess'

# seperator
print()

file_handle = AstroFile(
    file_name = "astro_code.txt", 
    cleanup = False
)

tokenizer = Tokenizer(
    h_file = file_handle
)
tokenizer.tokenize()

# seperator
print()
