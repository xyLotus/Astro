# Copyright (C) 2021 bellrise

# The Makefile used for building the virtual machine.

# The compiler of choice. This can also be gcc or some Windows version of gcc.
CC := clang

# Compiler flags and debug version flags.
CFLAGS := -Wall -Wextra -Wno-unused-parameter
DFLAGS := -fsanitize=address
IFLAGS := -Iinclude

# Binary result
RESULT := avm

# Files
SOURCES := $(shell find src -type f -printf '%p ' | sed 's/src\///g')
OBJECTS := $(foreach var,$(SOURCES),build/objects/$(var).o)

# Default target, build and link everything from the ground up.
all: setup build

# Setup directories
setup:
	mkdir -p build/objects

# Build instruction
build: $(SOURCES)
	@ $(CC) $(CFLAGS) $(DFLAGS) $(IFLAGS) -o build/$(RESULT) $(OBJECTS)

# Print the help page
help:
	@printf "targets:\n \
	  (default)   - build the whole project\n \
	  install     - install the binary to /usr/bin\n \
	  uninstall   - remove the installed binary\n \
	  clean       - remove the build directory\n"

# Install the produced binary to /usr/bin
install:
	@ sudo cp -f build/$(RESULT) /usr/bin/$(RESULT)

# Remove the produced binary from /usr/bin
uninstall:
	@ sudo rm -f /usr/bin/$(RESULT)

# Clean the build directory
clean:
	rm -r build

$(SOURCES):
	@ echo "Compiling $@"
	@ $(CC) $(CFLAGS) $(DFLAGS) $(IFLAGS) -c -o build/objects/$@.o src/$@

