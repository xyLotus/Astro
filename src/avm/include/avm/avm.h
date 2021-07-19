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

/* Version */

#define AVM_VERSION     {0, 0, 2}
#define AVM_COPYRIGHT   "avm 0.0.2 (Astro toolchain)\n" \
    "Copyright (C) 2021 bellrise\n\n" \
    "This project is licenced under the GNU Public Licence v3.0\n" \
    "which can be found at <https://gnu.org/licenses/gpl.html>"

/* Error codes */

#define EC_OK       0       /* everything is fine */
#define EC_PERM     1       /* operation not permitted */
#define EC_FEXIST   2       /* file/directory doesn't exit */
#define EC_FFILE    3       /* is a file */
#define EC_FDIR     4       /* is a directory */
#define EC_MMAPF    5       /* failed to mmap a file */
#define EC_MMAPM    6       /* failed to mmap memory */

/* Get a string representation of the error for it to be printed. */
const char *avm_strerror(int err);

/* Result from the argument parser (args_parse function). */
struct args
{
    char    *arg_filename;
    char    *arg_args;
};

/* Parse the given arguments (without the executable name) and create an args
   struct based on them. This function may exit the program, if some error
   occurs during the parsing. */
struct args avm_argparse(int argc, char **argv);

/* Print a formatted error to standard out. The error function additionally
   runs any possible clean up routines before exiting with exit code 1. */
void avm_error(char *fmt, ...);
void avm_warn(char *fmt, ...);


#endif /* AVM_H */
