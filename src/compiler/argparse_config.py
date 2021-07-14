"""Stores the configuration of the current
Astro argparser (powered by @lib argparse). """

__author__ = 'Lotus'
__version__ = 'STASIS'


import argparse


argparser = argparse.ArgumentParser(
    description="Processes the Astro compiler's arguments."
)

def init_parse():
    """Initializes argparser => set-up of config. """
    argparser.add_argument(
        'target_file',
        help='File to be compiled'
    )

    argparser.add_argument(
        '--noerr',
        action="store_true",
        help='Catches all errors at compilation run-time'
    )

    # NOTE Add any other arguments to-be-parsed
    #      below this comment


def get_argv() -> list:
    """Returns the parsed arguments (reflective)"""
    args = argparser.parse_args()
    return args