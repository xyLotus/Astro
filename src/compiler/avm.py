"""
Copyright (C) 2021 bellrise

This file is licenced under the GNU Public Licence v3.0 which can be found
at the root of this project found at <https://github.com/xyLotus/Astro>.

Collection of values defined by the Astro virtual machine headers. Note
that not all definitions are set here, because they are C-specific or just
useless here. This can also be called the AVM interface. You may use this
file in any implementation of the compiler or interpreter, because the
basic set of values will always be here along with some implementation
specific fields.
"""
from _ctypes import sizeof as _sizeof
from ctypes import c_uint16 as _ushort, c_char as _char, c_uint as _uint, \
        c_char_p as _char_ptr
from abc import ABC, abstractmethod
_ptr_size = _sizeof(_char_ptr)

BC_VERSION  = 1
BC_MAGIC    = b'\x5aABC'
__version__ = BC_VERSION


class _bc_struct(ABC):
    """Private handler for the struct classes. """

    def __init__(self):
        """The class constructor adds all defined symbols from the class. """
        fields = self.__class__.__dict__['__annotations__']
        for key, typ in fields.items():
            self.__dict__[key] = typ()

    @abstractmethod
    def size(self) -> int:
        """Return the size of the object. """
        pass


class bc_hdr(_bc_struct):
    """Bytecode header. This is located at the beginning of every compiled
    bytecode file containing useful meta information about the file. The
    strings with names are located after the header, in the exact order the
    lengths are provided in the header. """

    hdr_magic: bytes        # magic bytes
    hdr_version: int        # version
    hdr_size: _uint         # sizeof bc_hdr + sizeof hdr_data
    hdr_flags: int          # header flags
    hdr_sys: _char          # system
    hdr_endian: _char       # file endianness
    hdr_org_name: _ushort   # original file name
    hdr_mod_name: _ushort   # module name
    hdr_main_func: _ushort  # main function name
    hdr_data: bytes         # data

    def size(self) -> int:
        """Return the size of the struct. """
        return 24 + len(self.hdr_data)


class bc_ins(_bc_struct):
    """Single instruction"""

    ins_type: _ushort       # type of instruction
    ins_len: _ushort        # payload length
    ins_payload: bytes      # payload

    def size(self) -> int:
        """Return the size of the struct. """
        return 4 + len(self.ins_payload)


class bc_sym(_bc_struct):
    """Symbol, also known as a function. sym_ptr points to the start of the
    BCO_FUNCTION instruction. """

    sym_pos: _uint          # location of symbol in file
    sym_len: _ushort        # symbol length
    sym_flags: _ushort      # flags
    sym_ptr: _char_ptr      # pointer to start of symbol

    def size(self) -> int:
        """Return the size of the struct. """
        return 8 + _ptr_size


# Universal values

BC_FALSE            = 0x00
BC_TRUE             = 0x01

# hdr_sys

BC_SYS_UNKNOWN      = 0x00
BC_SYS_LINUX        = 0x01
BC_SYS_WIN          = 0x02

# hdr_endian

BC_ENDIAN_SMALL     = 0x00
BC_ENDIAN_BIG       = 0x01

# hdr_flags

BCF_HDR_BUILTIN     = 0x00000001    # builtin module
BCF_HDR_STANDALONE  = 0x00000002    # no dependencies

# sym_flags

BCF_SYM_PUBLIC      = 0x0001    # public function
BCF_SYM_PRIVATE     = 0x0002    # private function
BCF_SYM_METHOD      = 0x0004    # method
BCF_SYM_CALLED      = 0x0008    # function was called

# ins_type

BCO_NOP             = 0x0000    # no operation
                                # implementation specific
BCO_FUNCTION        = 0x0010    # function definition
BCO_ENDFUNC         = 0x0011    # end of function definition
BCO_BASECALL        = 0x0012    # basic instruction call
BCO_CALL            = 0x0013    # function call
BCO_IMPORT          = 0x0014    # module import
BCO_CREATE          = 0x0015    # create variable
BCO_ASSIGN          = 0x0016    # assign to variable
BCO_RETURN          = 0x0017    # return
BCO_IF              = 0x0018    # if
BCO_ELIF            = 0x0019    # elif
BCO_ELSE            = 0x001a    # else
BCO_ENDIF           = 0x001b    # end of if statement
