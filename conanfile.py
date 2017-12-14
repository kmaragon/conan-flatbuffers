from conans import ConanFile, CMake, tools
import os

class FlatbuffersConan(ConanFile):
    name = "flatbuffers"
    version = "1.7.1"
    license = "Apache 2.0"
    url = "https://github.com/kmaragon/conan-flatbuffers"
    description = "Conan Package for google flatbuffers"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "enable_flatc": [True, False], "enable_flathash": [True, False]}
    default_options = "shared=False", "enable_flatc=True", "enable_flathash=True"
    generators = "cmake"

    def source(self):
        tools.download("https://github.com/google/flatbuffers/archive/v%s.tar.gz" % self.version, "flatbuffers.tar.gz")
        tools.unzip("flatbuffers.tar.gz")
        os.unlink("flatbuffers.tar.gz")

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("flatbuffers-%s/CMakeLists.txt" % self.version, "project(FlatBuffers)", '''project(FlatBuffers)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["FLATBUFFERS_CODE_COVERAGE"] = "OFF"
        cmake.definitions["FLATBUFFERS_INSTALL"] = "ON"
        cmake.definitions["FLATBUFFERS_BUILD_TESTS"] = "OFF" 
        cmake.definitions["FLATBUFFERS_GRPCTEST"] = "OFF"
 
        cmake.definitions["FLATBUFFERS_BUILD_FLATLIB"] = "ON" if not self.options.shared else "OFF"
        cmake.definitions["FLATBUFFERS_BUILD_FLATC"] = "ON" if self.options.enable_flatc else "OFF"
        cmake.definitions["FLATBUFFERS_BUILD_FLATHASH"] = "ON" if self.options.enable_flathash else "OFF"
        cmake.definitions["FLATBUFFERS_BUILD_SHAREDLIB"] = "ON" if self.options.shared else "OFF"
        cmake.configure(source_dir="%s/flatbuffers-%s" % (self.source_folder, self.version))
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        self.copy("*.cmake", dst=".", src="flatbuffers-%s/CMake/" % self.version)

    def package_info(self):
        self.cpp_info.libs = ["flatbuffers"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.includedirs = ["include"]
