#include "getopt.h"

#ifdef __cplusplus
extern "C"
{
#endif

char *optarg;
int optind, opterr, optopt;

int getopt(int argc, char * const argv[], const char *optstring)
{
    return 0;
}

int getopt_long(int argc, char * const argv[], const char *optstring,
           const struct option *longopts, int *longindex)
{
    return 0;
}

int getopt_long_only(int argc, char * const argv[], const char *optstring,
                  const struct option *longopts, int *longindex)
{
    return 0;
}

#ifdef __cplusplus
}
#endif
