This is a windows port of The Silver Searcher, maintained by
Krzysztof Kowalczyk (http://blog.kowalczyk.info/).

Binaries: http://blog.kowalczyk.info/software/the-silver-searcher-for-windows.html

To compile you need Premake (http://industriousone.com/premake, I use 4.3)
and Visual Studio.

Compilation steps:
 * run: premake4 vs2010
 * open vs-premake/ag.sln in Visual Studio 2010 or later, proceed as usual

How this port was made.
-----------------------

The philosophy was to make minimal changes from the official repo.

The libraries that ag depends (zlib, pcre, pthread-win32) are included in
wincompat directory.

I wrote a premake meta-build script (premake4.lua) which is used to generate
Visual Studio project files.

As much as possible, I wrote Windows versions of unix functions/headers
used by ag (in wincompat directory).

I also wrote testing framework (scripts/runtests.py and tests), although it's
light on tests currently.

And that's pretty much it.
