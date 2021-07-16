/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#ifndef AVM_CORE_H_
#define AVM_CORE_H_

/* The core header provides some global symbols and structs used almost
   everywhere in the virtual machine source code. */

#include <stddef.h>


#define AVM_VERSION     {0, 0, 2}
#define AVM_COPYRIGHT   "avm 0.0.2 (Astro toolchain)\n" \
    "Copyright (C) 2021 bellrise\n\n" \
    "This project is licenced under the GNU Public Licence v3.0\n" \
    "which can be found at <https://gnu.org/licenses/gpl.html>"


/* Result from the argument parser (args_parse function). */
struct args
{
    char    *arg_filename;
    char    *arg_args;
};

/* Parse the given arguments (without the executable name) and create an
   args struct based on the arguments. This function may exit the program
   if --help or --version is called for example. */
struct args args_parse(int argc, char **argv);

/* Print a formatted error to standard out. The error function additionally
   runs any possible clean up routines before exiting with exit code 1. */
void vm_error(char *fmt, ...);
void vm_warn(char *fmt, ...);


#endif /* AVM_CORE_H_ */

