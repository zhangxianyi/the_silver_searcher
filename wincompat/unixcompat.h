#ifndef wincompat_unix_compat_h
#define wincompat_unic_compat_h

/* Define things that are provided by unix headers but not by Visual Studio */

/* <sys/types.h> on unix */
typedef int ssize_t;

#define PATH_MAX 512

#endif
