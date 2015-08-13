#!/bin/bash

cd ./glfw
cmake -D BUILD_SHARED_LIBS:BOOL=ON .
make
sudo make install
