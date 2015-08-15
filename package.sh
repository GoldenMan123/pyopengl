#!/bin/bash

mkdir -p ./PyOpenGL_game
cp *.py ./PyOpenGL_game
cp *.vert ./PyOpenGL_game
cp *.frag ./PyOpenGL_game
cp ./glfw/src/libglfw.so ./PyOpenGL_game
cp event.list ./PyOpenGL_game
touch ./PyOpenGL_game/__init__.py
mkdir -p ./PyOpenGL_game/data
mkdir -p ./PyOpenGL_game/localization
cp ./data/* ./PyOpenGL_game/data
cp ./localization/*.po* ./PyOpenGL_game/localization
mkdir -p ./PyOpenGL_game/localization/ru/LC_MESSAGES
cp ./localization/ru/LC_MESSAGES/* ./PyOpenGL_game/localization/ru/LC_MESSAGES
python2.7 setup.py bdist_wheel register upload
rm -rf ./PyOpenGL_game ./PyOpenGL_game.egg-info ./build
