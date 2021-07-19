/**
 * Astro Virtual Machine
 *
 * Copyright (C) 2021 bellrise
 *
 * This file is licenced under the GNU Public Licence v3.0 which can be found
 * at the root of this project found at <https://github.com/xyLotus/Astro>.
 */
#ifndef AVM_OBJECT_H
#define AVM_OBJECT_H

/* Object struct and its interface */

#define OBJECT_USED     1
#define OBJECT_FREED    2

/*
 * Objects are structures allocated on a custom heap managed just for them, to
 * provide more control over garbage collecting and reference counting. An
 * object should never be allocated on the stack, because they must outlive
 * a C function call.
 *
 * Once allocated, an object stays in memory so it doesn't get copied around
 * decreasing speed. Only the pointer to the object moves. Most objects have
 * values attached to them, which are usually allocated structures on the stan-
 * -dard heap provided by malloc(), because that doesn't need to ref-counted
 * and is removed when calling the deconstructor for the object.
 */

struct object
{
    char            *o_name;
    void            *o_vptr;
    unsigned int    o_ref;
    unsigned int    o_flags;
    unsigned int    o_type;

    /* Object destructor. This should be called before removing it from the
       object arena, to free any heap-allocated memory. Different object will
       have different destructors, but none of them free the object from the
       heap, it needs to be done by hand. */
    int (*o_dtor) (struct object *self);

    /* Method for printing the object to standard out. This should print the
       raw form of the object, without a newline. If the object cannot be nice-
       -ly formatted, print the object ID (memory addr), name and possibly the
       type. */
    int (*o_print) (struct object *self);

    /* Return 0 or 1 depending on the "boolean" value of the object. This is
       used in if statements. */
    int (*o_bool) (struct object *self);
};

struct object_list
{
    unsigned int  ol_size;
    struct object **ol_objects;
};

struct object_map /* FAR FROM IMPLEMENTATION, DO NOT USE */
{
    unsigned int om_size;
    unsigned int om_space;
    struct object **ol_objects;
};

/* Functions */

/* Create a new object on the heap. */
struct object *object_new(char *name);


#endif /* AVM_OBJECT_H */
