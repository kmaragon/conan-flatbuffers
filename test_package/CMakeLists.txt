project(PackageTest CXX)
cmake_minimum_required(VERSION 3.4)

set(CMAKE_CXX_STANDARD "14")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

list(GET CONAN_BINDIRS_FLATBUFFER 0 flatc_bindir)
find_program(flatc_command "flatc" HINTS "${flatc_bindir}")

add_custom_command(
    COMMAND "${flatc_command}" --cpp -o "${CMAKE_CURRENT_BINARY_DIR}" "test.fbs"
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/test.fbs"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/test_generated.h"
)

add_executable(test_fb test_fb.cpp "${CMAKE_CURRENT_BINARY_DIR}/test_generated.h")
target_include_directories(test_fb PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(test_fb ${CONAN_LIBS})

