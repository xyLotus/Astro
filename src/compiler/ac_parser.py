"""
The parser.
"""
import re
import sys
from typing import List, Callable, Optional

import avm
from astro_types import TokenType, Token

__author__  = 'bellrise'
__version__ = '0.1'

if sys.version_info.minor < 5:
    raise RuntimeError('requires Python >= 3.5')


class Parser:
    """The parser takes a list of tokens that are the result from the
    tokenizer class, and returns a syntax tree that can then be turned into
    bytecode. In between parsing, different parts of the code are checked
    for invalid or useless code. This class can print an error telling you
    where the invalid code is located, and exit the program if the code
    cannot compile properly. """

    possible_checks = []

    signatures = (
        # ! name ( ... ) :
        (avm.BCO_FUNCTION, (
            TokenType.EXCL, TokenType.NAME, TokenType.LPAREN, ...,
            TokenType.RPAREN, TokenType.COLON)),
        # name ( ... )
        (avm.BCO_CALL, (
            TokenType.NAME, TokenType.LPAREN, ...,
            TokenType.RPAREN)),
        # name = ...
        (avm.BCO_ASSIGN, (TokenType.NAME, TokenType.ASSIGN, ...)),
        # name ...
        (avm.BCO_BASECALL, (TokenType.NAME, ...)),
    )

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

        # This is set in trap_errors
        self.error_callback = None

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

        self.calculate_indents()

        for token_ctx in self.tokens:
            tokens = token_ctx['tokens']
            result = self.match(tokens)
            if result is None:
                self.error(token_ctx, 'invalid syntax')

            for k, v in avm.__dict__.items():
                if k.startswith('BCO_') and v == result:
                    print(k)
                    break

        return []

    def match(self, tokens: List[Token]) -> Optional[int]:
        """Match a token list to a statement type, and then return that tuple
        of the type and function to call to parse it. We first fetch only the
        token IDs and that are not spaces. Then iterate through the signatures
        using similar to regex rules: if a ellipsis (...) is found in the
        middle, it skips n tokens until it finds the next type in the signature.
        If the ellipsis is at the end, it matches anything.
        :param tokens: list of token types
        :return: token ID or None if not matched
        """
        tokens = [tok.id for tok in tokens if tok.id is not TokenType.SPACE]
        if not tokens:
            return avm.BCO_NOP

        for _sig in self.signatures:
            # Check each signature for a matching one
            id_, sig = _sig
            tok_index = 0

            if _sig[1][0] is ...:
                raise SyntaxError('invalid signature: cannot start with any')

            for sig_index, element in enumerate(sig):
                # If the element in the signature is an ellipsis, skip until it
                # finds the next element in the token list or to the end if no
                # element is found after the ellipsis.
                if element is ...:
                    if sig_index - 1 == len(sig):
                        return id_
                    if sig_index + 1 >= len(sig):
                        return id_
                    if sig[sig_index+1] is ...:
                        raise SyntaxError('invalid signature: 2 any fields')

                    pos = tokens[tok_index:].index(sig[sig_index+1])
                    if pos == -1:
                        # If the next token hasn't been found, skip to another
                        # signature.
                        break

                    # We have to take in account that we're taking a slice of
                    # the tokens list
                    tok_index += pos
                    continue

                if not element == tokens[tok_index]:
                    break

                tok_index += 1

            # We found a match!
            if tok_index == len(tokens):
                return id_

        return None

    def calculate_indents(self):
        """Count the indents for every token array in self.tokens, and add
        a brand new field named 'indent' with the amount of indentations. The
        chosen amount of indents is the first found amount. If real tabs (\t)
        are used, they are counted as 4 spaces which is interchangeable with
        4 actual spaces.
        """
        width = 0

        # Replace tabs with 4 spaces
        for index, tok in enumerate(self.tokens):
            self.tokens[index]['tokens'] = [
                Token(TokenType.SPACE, ' ') * 4 if t.id == TokenType.TAB
                else t
                for t in tok['tokens']
            ]

        for index, context in enumerate(self.tokens):
            context['indent'] = 0
            # We need to skip the first line because of index stuff down below
            if not context['tokens'] or index == 0:
                continue

            if context['tokens'][0].id == TokenType.SPACE:
                if not width:
                    # If the tab size wasn't defined yet, count it
                    width = self._count_continuous(context['source'], ' ')

                # If the tab size isn't the same as the defined width, throw
                # a nice little indentation error width complex math trying to
                # guess your tab size.
                tab = self._count_continuous(context['source'], ' ')
                if tab % width != 0 or (tab - width > width):
                    should_be = width
                    if tab > width:
                        previous = self.tokens[index-1].get('indent', 0)
                        should_be = previous * width + width

                    self.error(
                        context, f'invalid indent of {tab}, should be {should_be}',
                        size=tab, tab=False
                    )

                context['indent'] = tab // width

    @staticmethod
    def _count_continuous(string, char) -> int:
        """Count the amount of continuous chars from the start of the string.
        :param string: string to count on
        :param char: single character to compare
        """
        counter = 0
        for c in string:
            if c is not char:
                break
            counter += 1
        return counter

    def trap_errors(self, callback: Callable[[str, dict], None]):
        """Catch any errors that could close the parser, passing the error
        message and the token context to the function.
        :param callback: a function that will be called when an error occurs.
        """
        self.error_callback = callback

    def error(self, ctx: dict, *msg, at=0, size=0, tab=True, sep=' '):
        """Print a compilation error and exit.
        :param ctx: line context - index, filename and source
        :param msg: any amount of data to print after that
        :param at: index at where the error happened
        :param size: length of the squiggly
        :param tab: start the squiggly from the start of code (skip whitespace)
        :param sep: separator, default is space
        """
        if self.error_callback:
            self.error_callback(msg, ctx)
            return
        self._print_problem('Compilation error', ctx, *msg, at=at,
                            size=size, tab=tab, sep=sep)
        exit(1)

    def warn(self, ctx: dict, *msg, at=0, size=0, tab=True, sep=' '):
        """Print a warning.
        :param ctx: line context - index, filename and source
        :param msg: any amount of data to print after that
        :param at: index at where the error happened
        :param size: length of the squiggly
        :param tab: start the squiggly from the start of code (skip whitespace)
        :param sep: separator, default is space
        """
        self._print_problem('Compilation warning', ctx, *msg, at=at,
                            size=size, tab=tab, sep=sep)

    def _print_problem(self, title, ctx, *msg, at, size, tab, sep):
        msg = sep.join([str(x) for x in msg])
        if not size:
            size = len(ctx['source'])
        if self.error_callback:
            self.error_callback(msg, ctx)
            return

        # We want to skip whitespace for the squiggly but only if tab is True
        match = re.match(r'^\s*', ctx['source'])
        if tab and match:
            offset = match.span()[1]
            size -= offset
            at += offset

        print(
            f'{title} in {self.filename}:\n',
            f'{ctx["line"]:4} | {ctx["source"]}\n',
            ' ' * 7, ' ' * at, '^' + '~' * (size - 1), '\n',
            msg, sep='', file=sys.stderr
        )
