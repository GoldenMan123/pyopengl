# Python OpenGL game

## Requirements

1. OpenGL >4.3
2. Python 2.7

## Installing glfw

To compile GLFW for X11, you need to have the X11 and OpenGL header packages installed, as well as the basic development tools like GCC and make. For example, on Ubuntu and other distributions based on Debian GNU/Linux, you need to install the `cmake`, `xorg-dev` and `libglu1-mesa-dev` packages. The former pulls in all X.org header packages and the latter pulls in the Mesa OpenGL and GLU packages. GLFW itself doesn't need or use GLU, but some of the examples do. Note that using header files and libraries from Mesa during compilation will not tie your binaries to the Mesa implementation of OpenGL.

1. Run `install_glfw.sh`

## Installing game

To install game you need to have `virtualenv` and `pip` packages installed.

1. Run `install.sh`

## Testing

1. For test image rendering activate vitrualenv with `. ./bin/activate` command and run `python2.7 ./tests/sceneX.py` where X &mdash; scene number (1, 2 or 3).

## Running game

1. Run `run.sh`

