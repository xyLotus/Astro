/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include "fastargs.h"
#include <fastargs.h>
#include <avm/avm.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/* Globals */

static struct args *glob_args;

/* Functions */

static int action_usage(void *arg),
           action_version(void *arg),
           action_set_file(void *arg),
           action_set_args(void *arg),
           action_set_debug(void *arg);

struct args avm_argparse(int argc, char **argv)
{
    struct fa_parser *parser;
    struct args args;

    glob_args = &args;

    /* Initialize parser. */
    parser = fa_init('-', NULL, NULL, FA_REQUIREPOS);

    /* Set arguments. */
    fa_val(parser, "file", NULL, FA_STRING, action_set_file);
    fa_add(parser, "a", "args", NULL, FA_VALUE | FA_STRING, action_set_args);
    fa_add(parser, "h", "help", NULL, FA_FLAG | FA_HELP, action_usage);
    fa_add(parser, "v", "version", NULL, FA_FLAG, action_version);
    fa_add(parser, "d", "debug", NULL, FA_FLAG, action_set_debug);

    fa_parse(parser, argc, argv);
    fa_destroy(parser);
    return args;
}

static int action_usage(void *_Unused arg)
{
    printf(
        "usage: avm [option] ... file\n"
        "Execute compiled Astro bytecode.\n\n"
        "  file                 name of the file\n"
        "  -a, --args [args]    program arguments\n"
        "  -h, --help           show this page and exit\n"
        "  -v, --version        show the current version and exit\n"
        "  -d, --debug          enable vm debug features\n\n"
        "Only the last filename will be taken into consideration, any other "
        "path will \nbe skipped. The [args] option is a single string that is "
        "then internally \nsplit and passed to the Astro code as the global "
        "__args__ variable.\n"
    );
    exit(0);
}

static int action_set_file(void *arg)
{
    glob_args->a_filename = (char *) arg;
    return 0;
}

static int action_set_args(void *arg)
{
    glob_args->a_args = (char *) arg;
    return 0;
}

static int action_set_debug(void *_Unused arg)
{
    glob_args->a_debug = 1;
    return 0;
}

static int action_version(void *_Unused arg)
{
    printf("%s\n", AVM_COPYRIGHT);
    exit(0);
}
