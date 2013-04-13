#ifndef wincompat_unistd_h
#define wincompat_unistd_h

#ifdef __cplusplus
extern "C"
{
#endif

int getpagesize();

/* implemented in getopt.c */
int getopt(int argc, char * const argv[], const char *optstring);

extern char *optarg;
extern int optind, opterr, optopt;

#ifdef __cplusplus
}
#endif

#endif
