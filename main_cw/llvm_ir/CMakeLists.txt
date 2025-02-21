cmake_minimum_required(VERSION 3.17)
set(CMAKE_CXX_STANDARD 17)
project(llvm_ir)

add_library(runtimelib STATIC main.cpp)

# Tạo mã LLVM IR nếu cần
set(CXX_SOURCES_NAMES "main")
foreach (name ${CXX_SOURCES_NAMES})
    add_custom_command(
        OUTPUT
            "${CMAKE_CURRENT_BINARY_DIR}/${name}.ll"
        COMMENT
            "Generating LLVM IR for ${CMAKE_CURRENT_SOURCE_DIR}/${name}.cpp"
        COMMAND
            clang -S -emit-llvm "${CMAKE_CURRENT_SOURCE_DIR}/${name}.cpp" -o "${CMAKE_CURRENT_BINARY_DIR}/${name}.ll"
        DEPENDS
            "${CMAKE_CURRENT_SOURCE_DIR}/${name}.cpp"
    )
    list(APPEND LLVM_RESULTS "${CMAKE_CURRENT_BINARY_DIR}/${name}.ll")
endforeach ()
add_custom_target(std-library-llvm ALL DEPENDS ${LLVM_RESULTS})