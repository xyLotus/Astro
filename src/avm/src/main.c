/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/core.h>
#include <stdio.h>


int main(int argc, char **argv)
{
    struct args args = args_parse(--argc, ++argv);
}
