/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/core.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>


void vm_error(char *fmt, ...)
{
    va_list args;
    va_start(args, fmt);

    fprintf(stderr, "avm: \033[91merror:\033[0m ");
    vfprintf(stderr, fmt, args);
    fprintf(stderr, "\n");

    va_end(args);
    exit(1);
}

void vm_warn(char *fmt, ...)
{
    va_list args;
    va_start(args, fmt);

    fprintf(stderr, "avm: \033[91merror:\033[0m ");
    vfprintf(stderr, fmt, args);
    fprintf(stderr, "\n");

    va_end(args);
}
