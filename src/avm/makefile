# Copyright (C) 2021 bellrise

# This is a universal makefile that uses the generated target.mk file by
# the configure script for all the information about the compiler used, source
# files and so on.

include out/target.mk


# First, run the setup target to generate any required directories or files,
# and then compile all the sources.

all: $(OBJECTS) link


clean:
	find out -name '*.o' | xargs rm -rf


link:
	$(CC) $(CFLAGS) -o $(RESULT) $(OBJECTS)


install:
	sudo cp -f out/$(RESULT) /usr/bin/$(RESULT)


uninstall:
	sudo rm -f /usr/bin/$(RESULT)


$(OBJECTS): $(SOURCES)
	$(CC) $(CFLAGS) -c -o $@ $(shell echo $@ | sed 's/out/src/' \
		| sed 's/\.o/\.c/')
