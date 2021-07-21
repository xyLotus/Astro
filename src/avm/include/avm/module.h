/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#ifndef AVM_MODULE_H
#define AVM_MODULE_H

/*
 * The module struct and most of its requirements, along with a couple of
 * functions for handling the struct.
 */

#include <avm/object.h>
#include <avm/bc.h>

/*
 * The module struct inherits from the object structure, so it can also be re-
 * -presented using a simple `print` instruction for example. Because it is
 * built with the object struct at the beginning, it can be placed on the
 * custom object heap along with other objects. Internally, a module behaves
 * like a regular object with a couple of special methods along with it.
 *
 * To properly manage a module, it has to be de-allocated using the o_dtor
 * function from the header.
 */

struct module
{
    struct object      _self;
    unsigned int       m_nsyms;     /* amount of symbols */
    struct bc_sym      *m_syms;     /* symbols */
    unsigned int       m_size;      /* size of the code */

    union
    {
        struct bc_hdr  *m_header;   /* bytecode header */
        char           *m_code;     /* bytecode */
    };

    struct object_list m_locals;    /* locals */
};

/* Load a module into memory, from the passed path. The bytecode is mapped into
   memory, using mmap() if possible, which will m_code point to. After loading
   the code into memory, the header is validated and symbols are mapped. The
   opposite of this function is the _self.o_dtor function. */
int module_load(struct module *module, char *path, int flags);


#endif /* AVM_MODULE_H */
