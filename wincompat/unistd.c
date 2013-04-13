#include <windows.h>
#include "unistd.h"

#ifdef __cplusplus
extern "C"
{
#endif

int getpagesize (void)
{
  SYSTEM_INFO system_info;
  GetSystemInfo (&system_info);
  return system_info.dwPageSize;
}

#ifdef __cplusplus
}
#endif
