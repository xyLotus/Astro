/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#ifndef AVM_H
#define AVM_H

/*
 * The core header provides some global symbols and structs used across the
 * virtual machine, along with some utility functions, like the EC error codes.
 */

#include <stddef.h>
#include <stdlib.h>


/* Utility attributes */

#define _Unused     __attribute__((unused))


/* Version */

#define AVM_VERSION     {0, 0, 4}
#define AVM_COPYRIGHT   "avm 0.0.4 (Astro toolchain)\n" \
    "Copyright (C) 2021 bellrise\n\n" \
    "This project is licenced under the GNU Public Licence v3.0\n" \
    "which can be found at <https://gnu.org/licenses/gpl.html>"


/* Error codes */

#define EC_OK       0       /* everything is fine */
#define EC_TRUE     1       /* a true value */
#define EC_PERM     2       /* operation not permitted */
#define EC_FEXIST   3       /* file/directory doesn't exit */
#define EC_FFILE    4       /* is a file */
#define EC_FDIR     5       /* is a directory */
#define EC_MMAPF    6       /* failed to mmap a file */
#define EC_MMAPM    7       /* failed to mmap memory */
#define EC_HDRSIZE  8       /* invalid header size */

#define AVM_DIE()                                                           \
{                                                                           \
    printf(                                                                 \
        "\nOops :(\n\nSomething went really wrong and the virtual machine " \
        "is not able\nto recover. This error happened in %s on line %d\n",  \
        __FILE__, __LINE__                                                  \
    );                                                                      \
    abort();                                                                \
}


/* Utility macros */

#define AVM_DTOR_STATIC(OBJECT) \
    ((struct object *) &OBJECT)->o_dtor((struct object *) &OBJECT)
#define AVM_DTOR(OBJECT) \
    ((struct object *) OBJECT)->o_dtor((struct object *) OBJECT)
#define AVM_DUMP(OBJECT) \
    ((struct object *) OBJECT)->o_dump((struct object *) OBJECT)


/* Get a string representation of the error for it to be printed. */
const char *avm_strerror(int err);


/* Result from the argument parser (args_parse function). */
struct args
{
    char    *a_filename;
    char    *a_args;
    int     a_debug;
};

/* Global runtime instance */
struct runtime
{
    struct args *args;
};
extern struct runtime _avm_runtime_;

/* Parse the given arguments (without the executable name) and create an args
   struct based on them. This function may exit the program, if some error
   occurs during the parsing. */
struct args avm_argparse(int argc, char **argv);

/* Print a formatted error to standard out. The error function additionally
   runs any possible clean up routines before exiting with exit code 1. */
void avm_error(char *fmt, ...);
void avm_warn(char *fmt, ...);

/* Print n bytes to stdout in hex format, without a newline. */
int avm_hexdump(void *ptr, size_t bytes);


#endif /* AVM_H */
