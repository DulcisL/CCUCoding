# Almost all CMake files should start with this
# You should always specify a range with the newest
# and oldest tested versions of CMake. This will ensure
# you pick up the best policies.
cmake_minimum_required(VERSION 3.15)

# Make std 11 required
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Project name required
project(MyFunctions)

# Adding something we can run - Output name matches target name
add_executable(Functions main.cpp)

# To implement cmake:
# change directory to the build dir.
# cmake ..
# cmake --build .
