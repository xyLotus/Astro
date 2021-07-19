/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/avm.h>
#include <avm/object.h>
#include <malloc.h>
#include <string.h>

/* Object implementation */

struct object *object_new(char *name)
{
    AVM_DIE();
}

/* The default constructor should be called after each custom constructor,
   because this free's the default fields of the object, apart from the o_vptr
   which points to a custom struct. When building a custom constructor, any
   free'd pointer must be zeroed, or else the default destructor will throw
   a fatal error about a dangling pointer. */
int _o_default_dtor(struct object *self)
{
    /*
     * We do not want danling pointers to unfreed memory on the standard heap,
     * so we throw a fatal error if that happens to be the case.
     */
    if (self->o_vptr)
        avm_error("vptr of %p has not been free'd before removing the"
                  "object", self);

    free(self->o_name);
    memset(self, 0, sizeof(struct object));

    return EC_OK;
}
