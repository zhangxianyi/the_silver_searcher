#include "encoding.h"
#include "util.h"

#include <strsafe.h>
#include <windows.h>

/*
 http://stackoverflow.com/questions/3082620/convert-utf-16-to-utf-8
*/
char * convert_utf16_to_utf8(const char *buf, int *utf8_len) {
    // Get WCHAR's count corresponding to total input string length
    const size_t UTF16_LEN_MAX = INT_MAX - 1;
    size_t utf16_len;

    HRESULT hr = StringCchLengthW((STRSAFE_PCNZWCH)buf, UTF16_LEN_MAX, &utf16_len);
    if (FAILED(hr))
    {
        DWORD dwError = GetLastError();
        die("convert_utf16_to_utf8: StringCchLengthW failed - hr = 0x%X - LastError == 0x%X.", hr, dwError);
    }

    // Count the terminating \0
    ++utf16_len;

    // Get the size of destination UTF-8 buffer, in CHAR's (= bytes)
    *utf8_len = ::WideCharToMultiByte(
        CP_UTF8,                // convert to UTF-8
        0,                        // specify conversion behavior
        (LPCWCH)buf,            // source UTF-16 string
        (int)utf16_len,   // total source string length, in WCHAR's,
        // including end-of-string \0
        NULL,                   // unused - no conversion required in this step
        0,                      // request buffer size
        NULL,              // unsued
        NULL              // unused
        );

    if ((*utf8_len) == 0)
    {
        DWORD dwError = GetLastError();
        die("convert_utf16_to_utf8: WideCharToMultiByte (calculating size) failed - LastError == 0x%X.", dwError);
    }

    // Allocate the destination buffer for UTF-8 string
    char *_buf = (char *)malloc(*utf8_len);

    // Convert from UTF-16 to UTF-8
    int result = ::WideCharToMultiByte(
        CP_UTF8,                // convert to UTF-8
        0,                        // specify conversion behavior
        (LPCWCH)buf,            // source UTF-16 string
        (int)utf16_len,   // total source string length, in WCHAR's,
        // including end-of-string \0
        _buf,                    // destination buffer
        *utf8_len,                 // destination buffer size, in bytes
        NULL, NULL              // unused
        );

    if (result == 0)
    {
        DWORD dwError = GetLastError();
        die("convert_utf16_to_utf8: WideCharToMultiByte (conversion) failed - LastError == 0x%X.", dwError);
    }

    return _buf;
}
