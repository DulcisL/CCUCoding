# Boilerplate CMake Code ##############################
cmake_minimum_required(VERSION 3.14)
project(ChantsAdventure VERSION 0.0.0)

# C++ Standard 14 at the least is required for gtest
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# add any subdirectories, the order is important. Library must be created first before the exe
add_subdirectory(src) # .cpp
add_subdirectory(app) # location of main
add_subdirectory(inc) # .h and .hpp
# End Biolerplate ####################################

############ START GTEST ##############################
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

add_subdirectory(tests) # gtests