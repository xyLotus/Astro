"""
File wrapper for the tokenizer.
"""
import re

__author__  = 'xyLotus, bellrise'
__version__ = '0.0.5'


class AstroFile:
    """ Class that represents a astro file
    it __repr__'s the given file's @member file_name
    content and will probably be able to do various file operations. """

    def __init__(self, file_name: str, cleanup: bool = True):
        """Prepare the file for use.
        :param file_name: path to the file
        :param cleanup: remove comments from the file
        """
        self.file_name = str(file_name)
        self.content = ""

        with open(file_name, 'r') as f:
            self.content = f.read()

        if cleanup:
            self._cleanup()

    def __repr__(self):
        return self.content

    def _cleanup(self) -> None:
        """Removes comments from the source file. """

        content: str = self.content.replace('\r', '')

        result = re.finditer(r'(;;[\n\w\s]*;;)+', content)
        for match in result:
            # The reason I'm not using .replace on a string here is because
            # I would be cutting out every single instance which might come
            # up in a later match.
            spaces = ' ' * (match.span()[1] - match.span()[0])
            content = content[:match.span()[0]] + spaces \
                + content[match.span()[1]:]

        lines = content.split('\n')
        for index, line in enumerate(lines):
            match = re.match(r'^[^;]*(?P<comment>;.*)$', line)
            if match:
                lines[index] = line.replace(match.group('comment'), '')

        self.content = '\n'.join([s.rstrip() for s in lines])
