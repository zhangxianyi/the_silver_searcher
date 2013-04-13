#ifndef wincompat_unix_compat_h
#define wincompat_unic_compat_h

#include <io.h>
#include <stdio.h>

/* Define things that are provided by unix headers but not by Visual Studio */

/* <sys/types.h> on unix */
typedef int ssize_t;

#define PATH_MAX 512

/* those redefinitions silence warnings from newer version of Visual Studio */
#define isatty _isatty
#define fileno _fileno
#define strdup _strdup
#define close _close
#define open _open
#define fdopen _fdopen
#define popen _popen
#define pclose _pclose
#define pipe _pipe

#define S_IFIFO _S_IFIFO

#define S_ISDIR(mode)  (((mode) & S_IFMT) == S_IFDIR)
#define S_ISREG(mode)  (((mode) & S_IFMT) == S_IFREG)

#define va_copy(dest, src) (dest = src)

#endif
