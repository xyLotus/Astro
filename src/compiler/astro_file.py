""" The file where the AstroFile class gets stored,
which gets used as a file handle for basic operations
in context to the Astro compilation progress.  """

__author__ = 'xyLotus'
__version__ = '0.0.5'


class AstroFile:
    """ Class that represents a astro file
    it __repr__'s the given file's @member file_name
    content and will probably be able to do various file operations. """

    def __init__(self, file_name: str, cleanup: bool):
        self.file_name = str(file_name)
        self.cleanup = cleanup # wether to cleanup file in __repr__ or not
        self.content = ""

        with open(file_name, 'r') as f:
            self.content = f.read()

    def __repr__(self):
        if self.cleanup:
            self._cleanup()
        return self.content

    def _cleanup(self) -> None:
        """ removes unessecary characters with RegEx from source file
        for tokenization (ready-up), overwrites @member content """
        pass # TODO => Complete function with RegEx (remove comments)
