/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#include <avm/object.h>
#include <avm/module.h>
#include <avm/avm.h>
#include <avm/bc.h>
#include <string.h>
#include <stdio.h>

#if __linux__
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#elif _WIN32
#include <malloc.h>
#endif


#define PTR_ADD(BASE, OFFSET) (void *) ((size_t) (BASE) + (size_t) (OFFSET))

static int module_dtor(struct object *self);
static int module_dump(struct object *self);

int module_load(struct module *module, char *path, int flags)
{
#if __linux__
    /* The Linux implementation uses mmap() for better performance. */

    int fd;
    struct stat file_stat;

    fd = open(path, O_RDONLY);
    if (fd == -1)
        return EC_FEXIST;

    if (fstat(fd, &file_stat) == -1)
        return EC_PERM;

    module->m_size = file_stat.st_size;

    if (module->m_size < sizeof(struct bc_hdr))
        return EC_HDRSIZE;

    module->m_code = mmap(
            NULL, file_stat.st_size, PROT_READ, MAP_PRIVATE, fd, 0
    );
    if (!module->m_code)
        return EC_MMAPF;

#elif _WIN32
    /* The WinAPI also has a mmap()-like function, this can be done but now I'm
       just loading the file byte by byte into memory. */

    FILE *fp = fopen(path, "rb");
    if (!fp)
        return EC_FEXIST;

    fseek(fp, 0, SEEK_END);
    size_t file_size = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    module->m_size = file_size;
    module->m_code = malloc(file_size);

    for (size_t i = 0; i < file_size; i++)
        module->m_code[i] = fgetc(fp);

    fclose(fp);
#endif

    module->_self.o_name = PTR_ADD(module, module->m_header->hdr_off_mname);
    module->m_nsyms = 0;
    module->m_syms = NULL;
    /* todo: Map symbols */
    module->_self.o_flags |= AO_LOADED;
    module->m_size = module->m_header->hdr_size;

    /* Setup object */
    module->_self.o_dtor = module_dtor;
    module->_self.o_dump = module_dump;

    return 0;
}

static int module_dtor(struct object *self)
{
    struct module *module = (struct module *) self;

#if __linux__
    /* munmap() the file. */
    munmap(module->m_code, module->m_size);

#elif _WIN32
    /* Free the allocated memory. */
    free(module->m_code);

#endif
    /* Any other memory clean up goes here! Also, we want to zero the data for
       good measure. */
    memset(module, 0, sizeof(struct module));

    /* Call the original dtor for the object */
    _obj_default_dtor(self);

    return EC_OK;
}

static int module_dump(struct object *self)
{
    if (!_avm_runtime_.args->a_debug)
        return EC_OK;

    printf("[Module '%s' %p]\n", self->o_name, self);

    return EC_OK;
}
