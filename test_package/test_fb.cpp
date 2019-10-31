#include <iostream>
#include "test_generated.h"

int main() {
    ::flatbuffers::FlatBufferBuilder builder;
    auto msgb = ::test::conan::flatbufferspkg::Createtest_flatbuffer_messageDirect(builder, "Hello", 5, "World");
	builder.Finish(msgb);

    size_t size = builder.GetSize();
    uint8_t* data = builder.GetBufferPointer();

    std::cout << "Serialized data: ";
    std::cout.flush();
    for (size_t i = 0; i < size; i++)
        printf("%.2X", data[i]);
    std::cout << std::endl;
}
