# `avm`

This is the official implementation of an Astro virtual machine, written in C
and C++. In practice, the virtual machine is a part of the `astro` script which
also calls the Astro compiler, so the end-user never actually sees this being
executed. The simplest way of executing this program is passing the path to a
file with compiled bytecode as the first argument.

You can run these 2 commands (if you have both `astroc` and `avm` in your path).
```shell
$ astroc code.asx -o /tmp/code.abc
$ avm /tmp/code.abc
```
