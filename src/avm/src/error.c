/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/core.h>
#include <errno.h>


const char *ec_as_string(int err)
{
    static const char *errors[] = {
        "everything is fine",
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

