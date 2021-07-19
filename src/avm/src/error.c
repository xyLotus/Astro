/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/avm.h>


const char *avm_strerror(int err)
{
    static const char *errors[] = {
        "?",
        "?",
        "action is not permitted",
        "file/directory does not exist",
        "is a file",
        "is a directory",
        "failed to map a file into memory",
        "failed to map new memory"
    };

    static const int size = sizeof(errors) / sizeof(char *);

    if (err < 0 || err >= size)
        return "Unknown error";

    return errors[err];
}
