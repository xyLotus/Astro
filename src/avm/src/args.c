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
    void (*action) (int *, const int, const char **, struct args *);
};

static void parse_short(int *pos, const int argc, const char **argv,
        struct args *args);
static void parse_long(int *pos, const int argc, const char **argv,
        struct args *args);

static void action_usage(int *, const int, const char **, struct args *);
static void action_version(int *, const int, const char **, struct args *);
static void action_args(int *, const int, const char **, struct args *);


struct args args_parse(int argc, char **argv)
{
    struct args args = {0};

    for (int i = 0; i < argc; i++) {

        if (argv[i][0] == '-') {
            if (argv[i][1] == '-')
                parse_long(&i, (const int) argc, (const char **) argv, &args);
            else
                parse_short(&i, (const int) argc, (const char **) argv, &args);

            continue;
        }
        else
            args.arg_filename = argv[i];
    }

    if (!args.arg_filename)
        vm_error("no input file");

    return args;
}

static void parse_short(int *pos, const int argc, const char **argv,
        struct args *args)
{
    if (strlen(argv[*pos]) < 2)
        vm_error("empty argument '%s'", argv[*pos]);

    static const struct option actions[] = {
        {"h", action_usage},
        {"v", action_version},
        {"a", action_args}
    };

    static const size_t actions_s = sizeof(actions) / sizeof(struct option);

    for (size_t i = 0; i < actions_s; i++) {
        if (actions[i].name[0] == argv[*pos][1]) {
            actions[i].action(pos, argc, argv, args);
            return;
        }
    }

    vm_warn("unknown option '%s'", argv[*pos]);
}

static void parse_long(int *pos, const int argc, const char **argv,
        struct args *args)
{
    if (strlen(argv[*pos]) < 3)
        vm_error("empty argument '%s'", argv[*pos]);

    static const struct option actions[] = {
        {"help", action_usage},
        {"version", action_version},
        {"args", action_args}
    };

    static const size_t actions_s = sizeof(actions) / sizeof(struct option);

    for (size_t i = 0; i < actions_s; i++) {
        if (strcmp(actions[i].name, argv[*pos] + 2) == 0) {
            actions[i].action(pos, argc, argv, args);
            return;
        }
    }

    vm_warn("unknown argument '%s'", argv[*pos]);
}

static void action_usage(int *pos, const int argc, const char **argv,
        struct args *args)
{
    printf(
        "usage: avm [option] ... file\n"
        "Execute compiled Astro bytecode.\n\n"
        "  file                 name of the file\n"
        "  -a, --args [args]    program arguments\n"
        "  -h, --help           show this page and exit\n"
        "  -v, --version        show the current version and exit\n\n"
        "Only the last filename will be taken into consideration, any other "
        "path will \nbe skipped. The [args] option is a single string that is "
        "then internally \nsplit and passed to the Astro code as the global "
        "__args__ variable.\n"
    );
    exit(0);
}

static void action_version(int *pos, const int argc, const char **argv,
        struct args *args)
{
    printf("%s\n", AVM_COPYRIGHT);
    exit(0);
}

static void action_args(int *pos, const int argc, const char **argv,
        struct args *args)
{
    if (*pos + 1 == argc)
        vm_error("no arguments passed to --args");

    args->arg_args = (char *) argv[*pos + 1];
    (*pos)++;
}

