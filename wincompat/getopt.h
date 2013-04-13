#ifndef wincompat_getopt_h
#define wincompat_getopt_h

#ifdef __cplusplus
extern "C"
{
#endif

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

int getopt_long(int argc, char * const argv[], const char *optstring,
           const struct option *longopts, int *longindex);

int getopt_long_only(int argc, char * const argv[], const char *optstring,
                  const struct option *longopts, int *longindex);


#ifdef __cplusplus
}
#endif

#endif
