""" The utils file of Astro grants a variety of
different utilities to make your life easier while
developing Astro. """

__author__ = 'Lotus'
__version__ = 'STASIS'

class IterStr:
    def __init__(self, string):
        self.string = string
        self.left_len = 0
        self.delim: str

    def find(self, delim: str, opt_str = None) -> int:
        if opt_str != None:
            operator_str = opt_str
        else:
            operator_str = self.string

        self.delim = delim
        delim_len = len(delim)
        str_len = len(operator_str)

        i = 0
        while i <= str_len:
            if i + delim_len > str_len:
                break

            if operator_str[i:delim_len+i] == self.delim:
                self.left_len = (str_len - i) - 1
                return i
            i += 1

    def find_next(self):
        if self.delim == None:
            print("Error, no iteration base given.")
            exit(1)

        print('sample str', self.string[:self.left_len])
        return self.find(delim = self.delim, opt_str = self.string[:self.left_len])
        

x = IterStr("Hello ll")


print(x.find('ll'))
print(x.find_next())