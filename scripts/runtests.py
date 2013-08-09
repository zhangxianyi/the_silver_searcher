#!/usr/bin/env python

"""
Build ag and run tests.

Run as: ./scripts/runtests.py (because I'm lazy and it's easier to
hard-code such things).

It'll use a temporary directory ../ag_tests during tests.

To make it easy and compact to write additional tests:
- test descriptions are in files in tests directory
- a single file describes multiple tests
- for each test, it says:
  - what files exist and their content
  - command to run (presumably ag with apropriate flags)
  - expected result of the command
- tests stop when the output is different that the expected result. When that
  happens, ../ag_tests directory contains the data for the test so that a developer
  can investigate the problem
"""

import sys, os, shutil
from util import run_cmd, run_cmd_throw, memoize

# only when testing, speeds up test cycle
DISABLE_BUILD = True

def error_exit(msg):
	print(msg); sys.exit(1)

@memoize
def top_level_dir():
	# auto-detect either being in top-level or inside scripts
	if os.path.exists("runtests.py"):
		dir = ".."
	else:
		dir = "."
	path = os.path.realpath(dir)
	os.chdir(path)
	return path

@memoize
def ag_tests_dir():
	return os.path.realpath(os.path.join(top_level_dir(), "..", "ag_tests"))

def delete_ag_tests_dir():
	path = ag_tests_dir()
	if os.path.exists(path):
		shutil.rmtree(path, True)

def recreate_ag_tests_dir():
	delete_ag_tests_dir()
	path = ag_tests_dir()
	os.mkdir(path)

def is_win():
	return False # TODO:add proper test

@memoize
def ag_exe_path():
	ag_cmd = "ag"
	if is_win(): ag_cmd = "ag.exe"
	return os.path.realpath(os.path.join(top_level_dir(), ag_cmd))

def verify_started_in_right_directory():
	path = os.path.join(top_level_dir(), "scripts", "runtests.py")
	if not os.path.exists(path):
		error_exit("Must be in top level of source directory and run as ./scripts/runtests.py.\npath=%s" % path)

# just to be safe, if ../ag_tests directory exists we won't run tests and
# ask the user to delete it manually. This is either a conflict with a directory
# that a user created or left-over from previous failed run.
def verify_ag_tests_dir_doesnt_exist():
	if not os.path.exists(ag_tests_dir()): return
	print("ag_tests directory ('%s') directory from previous run exist" % ag_tests_dir())
	error_exit("Please delete it manually.")

def print_error(out, err, errcode):
	print("Failed with error code %d" % errcode)
	if len(out) > 0: print("Stdout:\n%s" % out)
	if len(err) > 0: print("Stderr:\n%s" % err)

def build_mac():
	(out, err, errcode) = run_cmd("./build.sh")
	if errcode != 0:
		print_error(out, err, errcode)
		# trying to be helpful and tell user how to resolve specific problems
		# TODO: also detect lack of pcre
		if "No package 'liblzma' found" in err:
			error_exit("\nIf you're using homebrew, you need to install xz package to get liblzma\nRun: brew install xz")
		sys.exit(1)

def build_win():
	error_exit("Building on Windows not supported yet")

def build():
	if DISABLE_BUILD and os.path.exists(ag_exe_path()):
		return
	if sys.platform == "darwin":
		build_mac()
	elif sys.platform.startswith("win"):
		build_win()
	else:
		error_exit("Don't know how to build on this platform. sys.platform=%s, os.name=%s" % (sys.platform, os.name))

def path_unix_to_native(path):
	parts = path.split("/")
	return os.path.join(parts)

def create_dir_for_file(path):
	dir = os.path.dirname()
	if not os.path.exists(dir):
		os.makedirs(dir)

# here path is always in unix format
def write_to_file(path, content):
	path = path_unix_to_native(path)
	create_dir_for_file(path)
	with open(path, "wb") as fo:
		fo.write(content)

class TestFileInfoSimple(object):
	def __init__(self, name, content):
		self.name = name
		self.content = content
	def write(self):
		write_to_file(self.name, self.content)

class TestInfo(object):
	def __init__(self):
		self.files = []
		self.test_name = "" # optional
		self.cmd = ""
		self.expected = ""

# context for parsing functions
class Tests(object):
	def __init__(self, test_file):
		self.test_file = test_file # for debugging
		self.lines = []
		with open(test_file, "rb") as fo:
			self.lines = fo.readlines()
		self.lines = [line.rstrip() for line in self.lines]
		self.curr_line = 0
		self.curr_test_info = None
		self.test_infos = []

	def start_new_test(self):
		if self.curr_test_info != None:
			self.test_infos.append(self.curr_test_info)
		self.curr_test_info = TestInfo()

	def unget_line(self):
		self.curr_line -= 1
		return self.lines[self.curr_line]

	def next_line(self):
		if self.curr_line >= len(self.lines):
			return None
		l = self.lines[self.curr_line]
		self.curr_line += 1
		return l

	def raise_error(self):
		print("Invalid format of tests file '%s'" % self.test_file)
		curr_line = self.unget_line()
		print("Curr line no %d:\n'%s'" % (self.curr_line, curr_line))
		raise "Error"

TEST_START = "test:"
CMD_START = "cmd:"
FILE_START = "file:"
NEW_TEST_START = "--"

# helper function that
def select_parsing_function(tests, *valid):
	curr_line = tests.unget_line()
	# TODO: write me
	return None

def parse_test_start(tests):
	tests.start_new_test()
	# TODO: write me
	return None

def parse_at_file_start(tests):
	while True:
		line = tests.next_line()
		if None == line:
			return None
		# skip comments at the top of the file
		if line.startswith("#"):
			continue
		if line == NEW_TEST_START:
			return parse_test_start(tests)
		tests.raise_error()

# returns an array of TestInfo objects
def parse_test_file(test_file):
	tests = Tests(test_file)
	parse_func = parse_at_file_start
	while parse_func != None:
		parse_func = parse_func(tests)
	return tests

def run_one_test_info(test_info):
	recreate_ag_tests_dir()

def run_tests_in_file(test_file):
	print(test_file)
	tests = parse_test_file(test_file)
	for test_info in tests.test_infos:
		run_one_test(test_info)

def run_tests():
	ag_cmd = ag_exe_path()
	if not os.path.exists(ag_cmd):
		error_exit("Didn't find ag executable. Expected: '%s'" % ag_cmd)
	test_files = [os.path.join("tests", f) for f in os.listdir("tests")]
	for f in test_files:
		run_tests_in_file(f)
	# if everything went ok, delete the temporary tests directory
	delete_ag_tests_dir()

def main():
	#print("top_level_dir = %s\nag_tests_dir =  %s\n" % (top_level_dir(), ag_tests_dir()))
 	verify_started_in_right_directory()
	verify_ag_tests_dir_doesnt_exist()
	build()
	run_tests()

if __name__ == "__main__":
	main()
