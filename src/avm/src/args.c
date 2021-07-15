/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/core.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


struct option
{
    const char *name;
    void (*action) (int *pos, const int argc, const char **argv);
};

static void parse_short(int *pos, const int argc, const char **argv);
static void parse_long(int *pos, const int argc, const char **argv);

static void action_usage(int *, const int, const char **);
static void action_version(int *, const int, const char **);


struct args args_parse(int argc, char **argv)
{
    struct args args = {0};

    for (int i = 0; i < argc; i++) {

        if (argv[i][0] == '-') {
            if (argv[i][1] == '-')
                parse_long(&i, (const int) argc, (const char **) argv);
            else
                parse_short(&i, (const int) argc, (const char **) argv);

            continue;
        }
        else
            args.filename = argv[i];
    }

    if (!args.filename)
        vm_error("no input file");

    return args;
}

static void parse_short(int *pos, const int argc, const char **argv)
{
    if (strlen(argv[*pos]) < 2)
        vm_error("empty argument '%s'", argv[*pos]);

    static const struct option actions[] = {
        {"h", action_usage},
        {"v", action_version},
    };

    static const size_t actions_s = sizeof(actions) / sizeof(struct option);

    for (size_t i = 0; i < actions_s; i++) {
        if (actions[i].name[0] == argv[*pos][1]) {
            actions[i].action(pos, argc, argv);
            return;
        }
    }

    vm_warn("unknown option '%s'", argv[*pos]);
}

static void parse_long(int *pos, const int argc, const char **argv)
{
    if (strlen(argv[*pos]) < 3)
        vm_error("empty argument '%s'", argv[*pos]);

    static const struct option actions[] = {
        {"help", action_usage},
        {"version", action_version},
    };

    static const size_t actions_s = sizeof(actions) / sizeof(struct option);

    for (size_t i = 0; i < actions_s; i++) {
        if (strcmp(actions[i].name, argv[*pos] + 2) == 0) {
            actions[i].action(pos, argc, argv);
            return;
        }
    }

    vm_warn("unknown argument '%s'", argv[*pos]);
}

static void action_usage(int *pos, const int argc, const char **argv)
{
    printf(
        "usage: avm file [option]...\n"
        "Execute compiled Astro bytecode.\n\n"
        "  -h, --help       show this page and exit\n"
        "  -v, --version    show the current version and exit\n"
    );
    exit(0);
}

static void action_version(int *pos, const int argc, const char **argv)
{
    printf("%s\n", AVM_COPYRIGHT);
    exit(0);
}
