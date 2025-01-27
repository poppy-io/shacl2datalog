#!/usr/bin/env bash
# lifted from https://souffle-lang.github.io/functors
g++ functors.cpp -c -fPIC -o functors.o
g++ -shared -o libfunctors.so functors.o
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}`pwd`
