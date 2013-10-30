-- to generate Visual Studio files in vs-premake directory, run:
-- premake4 vs2010 or premake4 vs2008

-- common settings for solutions
function solution_common()
  configurations { "Debug", "Release", "ReleaseKjk" }
  location "vs-premake" -- this is where generated solution/project files go

  -- Symbols - generate .pdb files
  -- StaticRuntime - statically link crt
  -- ExtraWarnings - set max compiler warnings level
  -- FatalWarnings - compiler warnigs are errors'
  -- NoMinimalRebuild - disable /Gm because it clashes with /MP
  flags {
   "Symbols", "StaticRuntime",
   "NoRTTI", "Unicode", "NoExceptions", "NoMinimalRebuild"
  }

  configuration "Debug"
    targetdir "dbg" -- this is where the .exe/.lib etc. files wil end up
    defines { "_DEBUG", "DEBUG" }

  configuration "Release"
     targetdir "rel"
     flags { "Optimize" }
     defines { "NDEBUG" }

  configuration "ReleaseKjk"
     targetdir "rel"
     flags { "Optimize" }
     defines { "NDEBUG", "KJK_BUILD" }

  configuration {"vs*"}
    -- defines { "_WIN32", "WIN32", "WINDOWS", "_CRT_SECURE_NO_WARNINGS" }
    defines { "_WIN32", "WIN32", "WINDOWS", "_CRT_SECURE_NO_WARNINGS" }
    -- 4800 - int -> bool coversion
    -- 4127 - conditional expression is constant
    -- 4100 - unreferenced formal parameter
    -- 4244 - possible loss of data due to conversion
    -- /MP  - use multi-cores for compilation
    buildoptions {
        "/wd4800", "/wd4127", "/wd4100", "/wd4244"
    }
end

solution "ag"
  solution_common()

  project "ag"
    kind "ConsoleApp"
    language "C++"
    files {
      "src/*.h",
      "src/*.c",
      "wincompat/dirent.*",
      "wincompat/getopt.*",
      "wincompat/unistd.*",
      "wincompat/kjk_crash_handler.*",
    }

    configuration {"vs*"}
      -- /TP  - compile as c++
      buildoptions { "/TP" }

    defines { "PCRE_STATIC" }
    includedirs { "src", "wincompat", "wincompat/zlib", "wincompat/pcre-8.32",
    "wincompat/pthread-win32" }
    linkoptions {"/NODEFAULTLIB:\"msvcrt.lib\""}
    links { "Shlwapi", "zlib", "pthread-win32", "pcre" }

  project "pcre"
    kind "StaticLib"
    language "C"
    defines { "HAVE_CONFIG_H" }
    files {
      "wincompat/pcre-8.32/pcre_byte_order.c",
      "wincompat/pcre-8.32/pcre_chartables.c",
      "wincompat/pcre-8.32/pcre_compile.c",
      "wincompat/pcre-8.32/pcre_config.c",
      "wincompat/pcre-8.32/pcre_dfa_exec.c",
      "wincompat/pcre-8.32/pcre_exec.c",
      "wincompat/pcre-8.32/pcre_fullinfo.c",
      "wincompat/pcre-8.32/pcre_get.c",
      "wincompat/pcre-8.32/pcre_globals.c",
      "wincompat/pcre-8.32/pcre_jit_compile.c",
      "wincompat/pcre-8.32/pcre_maketables.c",
      "wincompat/pcre-8.32/pcre_newline.c",
      "wincompat/pcre-8.32/pcre_ord2utf8.c",
      "wincompat/pcre-8.32/pcre_refcount.c",
      "wincompat/pcre-8.32/pcre_string_utils.c",
      "wincompat/pcre-8.32/pcre_study.c",
      "wincompat/pcre-8.32/pcre_tables.c",
      "wincompat/pcre-8.32/pcre_ucd.c",
      "wincompat/pcre-8.32/pcre_valid_utf8.c",
      "wincompat/pcre-8.32/pcre_version.c",
      "wincompat/pcre-8.32/pcre_xclass.c",
    }
    includedirs { "wincompat/pcre-8.32" }

  project "zlib"
     kind "StaticLib"
     language "C"
     files { "wincompat/zlib/*.c", "wincompat/zlib/*.h" }
     excludes { "wincompat/zlib/gzclose.c", "wincompat/zlib/gzread.c", "wincompat/zlib/gzwrite.c", "wincompat/zlib/gzlib.c"}
     includedirs { "wincompat/zlib" }

  project "pthread-win32"
     kind "StaticLib"
     language "C"
     files {
        "wincompat/pthread-win32/*.h",
        "wincompat/pthread-win32/pthread.c"
     }
     includedirs { "wincompat/pthread-win32" }
