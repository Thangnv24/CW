# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build

# Include any dependencies generated for this target.
include CMakeFiles/runtimelib.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/runtimelib.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/runtimelib.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/runtimelib.dir/flags.make

CMakeFiles/runtimelib.dir/main.cpp.o: CMakeFiles/runtimelib.dir/flags.make
CMakeFiles/runtimelib.dir/main.cpp.o: ../main.cpp
CMakeFiles/runtimelib.dir/main.cpp.o: CMakeFiles/runtimelib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/runtimelib.dir/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/runtimelib.dir/main.cpp.o -MF CMakeFiles/runtimelib.dir/main.cpp.o.d -o CMakeFiles/runtimelib.dir/main.cpp.o -c /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp

CMakeFiles/runtimelib.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/runtimelib.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp > CMakeFiles/runtimelib.dir/main.cpp.i

CMakeFiles/runtimelib.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/runtimelib.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp -o CMakeFiles/runtimelib.dir/main.cpp.s

# Object files for target runtimelib
runtimelib_OBJECTS = \
"CMakeFiles/runtimelib.dir/main.cpp.o"

# External object files for target runtimelib
runtimelib_EXTERNAL_OBJECTS =

libruntimelib.a: CMakeFiles/runtimelib.dir/main.cpp.o
libruntimelib.a: CMakeFiles/runtimelib.dir/build.make
libruntimelib.a: CMakeFiles/runtimelib.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libruntimelib.a"
	$(CMAKE_COMMAND) -P CMakeFiles/runtimelib.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/runtimelib.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/runtimelib.dir/build: libruntimelib.a
.PHONY : CMakeFiles/runtimelib.dir/build

CMakeFiles/runtimelib.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/runtimelib.dir/cmake_clean.cmake
.PHONY : CMakeFiles/runtimelib.dir/clean

CMakeFiles/runtimelib.dir/depend:
	cd /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build/CMakeFiles/runtimelib.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/runtimelib.dir/depend

