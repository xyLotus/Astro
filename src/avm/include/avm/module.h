/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#ifndef AVM_MODULE_H_
#define AVM_MODULE_H_

/* The module struct and most of it's requirements, along with a couple of
   functions for handling the struct. */

#include <avm/bc.h>


struct module
{
    char              *m_name;      /* name of the module */
    unsigned int      m_nsyms;      /* amount of symbols */
    struct bc_sym     *m_syms;      /* symbols */
    unsigned int      m_flags;      /* module flags */
    unsigned int      m_size;       /* size of the code */
    union {
        struct bc_hdr *m_header;    /* bytecode header */
        char          *m_code;      /* bytecode */
    };
};

/* Load a module into memory, from the passed path. The bytecode is mapped into
   memory, using mmap() if possible, which will m_code point to. After loading
   the code into memory, the header is validated and symbols are mapped. */
int module_load(struct module *module, char *path, int flags);

/* Unload the module from memory, free'ing all it's used resources. */
int module_unload(struct module *module);


#endif /* AVM_module_H_ */

