# Almost all CMake files should start with cmake version info
cmake_minimum_required(VERSION 3.22)

# A compatible C++ compiler that supports at least C++14
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Project name required
project(BlackJack 
    VERSION 1.0.0 # major, minor, patch
    LANGUAGES C CXX)

add_subdirectory(src)
add_subdirectory(app)
add_subdirectory(inc)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
  DOWNLOAD_EXTRACT_TIMESTAMP ON
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_subdirectory(tests)