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
include CMakeFiles/llvm_ir.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/llvm_ir.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/llvm_ir.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/llvm_ir.dir/flags.make

CMakeFiles/llvm_ir.dir/main.cpp.o: CMakeFiles/llvm_ir.dir/flags.make
CMakeFiles/llvm_ir.dir/main.cpp.o: ../main.cpp
CMakeFiles/llvm_ir.dir/main.cpp.o: CMakeFiles/llvm_ir.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/llvm_ir.dir/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/llvm_ir.dir/main.cpp.o -MF CMakeFiles/llvm_ir.dir/main.cpp.o.d -o CMakeFiles/llvm_ir.dir/main.cpp.o -c /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp

CMakeFiles/llvm_ir.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/llvm_ir.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp > CMakeFiles/llvm_ir.dir/main.cpp.i

CMakeFiles/llvm_ir.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/llvm_ir.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/main.cpp -o CMakeFiles/llvm_ir.dir/main.cpp.s

# Object files for target llvm_ir
llvm_ir_OBJECTS = \
"CMakeFiles/llvm_ir.dir/main.cpp.o"

# External object files for target llvm_ir
llvm_ir_EXTERNAL_OBJECTS =

llvm_ir: CMakeFiles/llvm_ir.dir/main.cpp.o
llvm_ir: CMakeFiles/llvm_ir.dir/build.make
llvm_ir: CMakeFiles/llvm_ir.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable llvm_ir"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/llvm_ir.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/llvm_ir.dir/build: llvm_ir
.PHONY : CMakeFiles/llvm_ir.dir/build

CMakeFiles/llvm_ir.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/llvm_ir.dir/cmake_clean.cmake
.PHONY : CMakeFiles/llvm_ir.dir/clean

CMakeFiles/llvm_ir.dir/depend:
	cd /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build /mnt/d/downloads/bmstu/7st_sem/cw/main_cw/llvm_ir/build/CMakeFiles/llvm_ir.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/llvm_ir.dir/depend

