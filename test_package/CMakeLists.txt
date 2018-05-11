project(PackageTest CXX)
cmake_minimum_required(VERSION 3.4)

set(CMAKE_CXX_STANDARD "14")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_custom_target(force_dir_change 
	COMMAND echo "Changing to ${CMAKE_CURRENT_BINARY_DIR}"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
)

find_package(FlatBuffers REQUIRED)
build_flatbuffers("fbs/test.fbs" "" "fb" "" "${CMAKE_CURRENT_BINARY_DIR}" "" "")

add_executable(test_fb test_fb.cpp)
target_include_directories(test_fb PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(test_fb ${CONAN_LIBS})
add_dependencies(test_fb fb)

