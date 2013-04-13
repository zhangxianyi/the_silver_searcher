#ifndef wincompat_getopt_h
#define wincompat_getopt_h

#define null_argument       0
#define no_argument         0
#define required_argument   1
#define optional_argument   2

struct option {
    const char* name;
    int         has_arg;
    int *       flag;
    char        val;
};

#endif
