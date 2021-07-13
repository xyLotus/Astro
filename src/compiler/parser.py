"""
The parser.
"""
from astro_types import TokenType
from typing import List
import avm

__author__  = 'bellrise'
__version__ = '0.1'


class Parser:
    """The parser takes a list of tokens that are the result from the
    tokenizer class, and returns a syntax tree that can then be turned into
    bytecode. In between parsing, different parts of the code are checked
    for invalid or useless code. This class can print an error telling you
    where the invalid code is located, and exit the program if the code
    cannot compile properly. """

    # List of all possible checks the parser can run on the code
    possible_checks = []

    def __init__(self, filename: str, tokens: List[dict], trust_me=False):
        """Setup the parser instance. This takes a token list. To actually
        start the parsing process, call parse() on the created object.
        :param filename: path to the file currently being compiled
        :param tokens:   list of context groups
        :param trust_me: True if the parser should trust the developer with
                         the data format
        """
        self.filename = filename
        self.tokens = tokens
        self.checks = []

        if not trust_me:
            if not isinstance(tokens[0], dict):
                raise TypeError('token context should be a dict')

            required_fields = 'line', 'source', 'tokens'
            for token in tokens:
                if not all(key in token for key in required_fields):
                    raise KeyError('missing keys in token context')

    def parse(self, checks=...) -> list:
        """Start parsing the provided token list, turning it into a syntax
        tree that can then be synthesized into bytecode.
        :param checks: a list of checks the parser should run, by default
                       all checks are enabled
        """
        if checks is ...:
            self.checks = self.possible_checks

        return []


if __name__ == '__main__':
    # This is a small piece of code for testing the general functionality
    # of the parser, real unit tests will be written.
    __parser = Parser('test.asx', [
        {'line': 1, 'source': '! function(param, param2):', 'tokens': [
            TokenType.EXCL, TokenType.NAME, TokenType.LPAREN, TokenType.NAME,
            TokenType.COMMA, TokenType.NAME, TokenType.RPAREN, TokenType.COLON
        ]},
        {'line': 2, 'source': '    out param', 'tokens': [
            TokenType.TAB, TokenType.NAME, TokenType.NAME
        ]}
    ])

    if __parser.parse() != [
        {
            'type': avm.BCO_FUNCTION,
            'name': 'function',
            'params': ['param', 'param2'],
            'code': [
                {'type': avm.BCO_BASECALL, 'call': 'out', 'params': [
                    {'type': 'var', 'name': 'param'}
                ]}
            ]
        }
    ]:
        print('failed to parse')
