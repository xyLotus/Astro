/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 *
 *                                 avm
 *
 * The official Astro Virtual Machine implementation project is built along
 * with the compiler written in Python (possibly a faster implementation might
 * come along one day?) in the same repository. Because these are 2 different
 * langauges and styles, different commit and stylistic rules apply. The goal
 * of writing this in C, and not Rust for example is a fine grain level of
 * control over what is going on and which memory goes where, along with the
 * amazing compilation times and tooling.
 *
 * The project itself is split into the headers found in include/avm and the
 * implementation in src. When building a new implementation of the virtual
 * machine, the headers, which can also be called the API should stay the same,
 * while the underlying code can be a lot different.
 *
 * When writing new code, the style should be consistent and the same as around
 * you. For a quick summary, here are the rules: lines should be less than 80
 * characters long. Function names, structures and variables should be named
 * after what they do in snake_case. Enum types should have a _type or _enum at
 * the end of their name, and all fields should be upper case with the orignal
 * name as the first part. Hash defines, along with global constants should
 * be ALL_UPPER_CASE. The preffered style of comments is standard C block
 * comments, without any C++ "//" comments. An empty trailing newline is also
 * required in each file.
 *
 * Functions should generally have a GNU-style comment above them, but if the
 * parameters are unclear in what they do: first of all, change your code, but
 * if that isn't possible create a Linux kernel-style block comment with @param
 * fields. The project uses C11, for functionality like _Generic macro func-
 * -tions (as a side note, this can be checked if __STDC_VERSION__ >= 201112L).
 *
 * Headers should define header guards in this fashion: AVM_[PATH]_H, and
 * should all have a copyright header, which can be just stolen from here (the
 * copyright header part is the first 7 lines). Includes should form a cool
 * little pyramid, with the longest path as the first, and have 2 newlines
 * below them, before any other code starts.
 *
 * When changing or adding something to a file, remember to add your name to
 * the "Copyright (C) ..." line in the header, and you may also add yourself
 * to the docs/CODEOWNERS file as an important contributor of that given file.
 *
 * tl;dr: Your code should be clean and readable, with meaningful names and
 * expressive comments (which must be kept up to date!). Have fun coding! :-)
 */
#include <avm/object.h>
#include <avm/module.h>
#include <avm/avm.h>
#include <stdio.h>


int main(int argc, char **argv)
{
    struct args args = avm_argparse(--argc, ++argv);

    struct module module = {0};
    int err = module_load(&module, args.arg_filename, 0);
    if (err)
        avm_error("%s", avm_strerror(err));

    module_unload(&module);
}
