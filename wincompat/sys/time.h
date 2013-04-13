#ifndef wincompat_sys_time_h
#define wincompat_sys_time_h

#include <windows.h>

int gettimeofday(struct timeval * tp, struct timezone * tzp);

#endif
