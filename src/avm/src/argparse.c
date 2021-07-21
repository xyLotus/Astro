/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/avm.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


struct option
{
    const char *name;
    void (*action) (void);
};

/* Functions */

static void parse_short();
static void parse_long();
static void action_usage();
static void action_version();
static void action_args();
static void action_debug();

/* Globals, used for parsing */

static int         *glob_pos;
static int         glob_argc;
static char        **glob_argv;
static struct args *glob_args;

/* Main args_parse function */

struct args avm_argparse(int argc, char **argv)
{
    struct args args = {0};

    for (int i = 0; i < argc; i++) {

        glob_pos = &i;
        glob_argc = argc;
        glob_argv = argv;
        glob_args = &args;

        if (argv[i][0] == '-') {
            if (argv[i][1] == '-')
                parse_long();
            else
                parse_short();

            continue;
        }
        else
            args.a_filename = argv[i];
    }

    if (!args.a_filename)
        avm_error("no input file");

    return args;
}

static void parse_short()
{
    if (strlen(glob_argv[*glob_pos]) < 2)
        avm_error("empty argument '%s'", glob_argv[*glob_pos]);

    static const struct option actions[] = {
        {"h", action_usage},
        {"v", action_version},
        {"a", action_args},
        {"d", action_debug},
    };

    static const size_t actions_s = sizeof(actions) / sizeof(struct option);

    for (size_t i = 0; i < actions_s; i++) {
        if (actions[i].name[0] == glob_argv[*glob_pos][1]) {
            actions[i].action();
            return;
        }
    }

    avm_warn("unknown option '%s'", glob_argv[*glob_pos]);
}

static void parse_long()
{
    if (strlen(glob_argv[*glob_pos]) < 3)
        avm_error("empty argument '%s'", glob_argv[*glob_pos]);

    static const struct option actions[] = {
        {"help", action_usage},
        {"version", action_version},
        {"args", action_args},
        {"debug", action_debug},
    };

    static const size_t actions_s = sizeof(actions) / sizeof(struct option);

    for (size_t i = 0; i < actions_s; i++) {
        if (strcmp(actions[i].name, glob_argv[*glob_pos] + 2) == 0) {
            actions[i].action();
            return;
        }
    }

    avm_warn("unknown argument '%s'", glob_argv[*glob_pos]);
}

static void action_usage()
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

static void action_version()
{
    printf("%s\n", AVM_COPYRIGHT);
    exit(0);
}

static void action_args()
{
    if (*glob_pos + 1 == glob_argc)
        avm_error("no arguments passed to --args");

    glob_args->a_args = (char *) glob_argv[*glob_pos + 1];
    (*glob_pos)++;
}

static void action_debug()
{
    glob_args->a_debug = 1;
}
