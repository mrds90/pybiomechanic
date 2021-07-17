# pybiomechanic
This repository resolve a simply biomechanical model of the lower limb. There is an example that use the pyc3dserver aplication (only for windows) to load information from a c3d files. But it's not necesary to load a c3d file to use the library.

## Run the example (only Windows)

### Install python

There are many ways to install python on windows, I recommend to install the last version in the Microsoft Store. Also you can download in the official website of [python](https://www.python.org/downloads/).

I recommend to use a virtual enviroment in all you python projects, but is optional. Virtualenv is available in PyPi, you can use it to create the enviroments.

### Install git

If you don't have git yet, you should install. The commands below are bash commands and the git terminal is a bash terminal. You can download in the official website of [git](https://git-scm.com/).

### Install dependences
in a bash terminal, as git terminal, execute:

```
pip3 install numpy
```
```
pip3 install pyc3dserver
```
```
pip3 install scipy
```
```
pip3 install matplotlib
```

### Install C3D Software Development Kit (c3dServer)
c3d.org give us the access to this diferents tool to manage c3d files [c3dAplications](https://www.c3d.org/c3dapps.html). c3dServer is A Software Development Kit (SDK) for C3D.  Updated for 32/64-bit Windows systems, this provides easy-to-use C3D file access from Visual Basic, MATLAB, C++, Excel, Java, and Word etc. The SDK includes documentation, sample Visual Basic and C++ code, and a C3D file editing application (including Visual Basic source code and documentation).
This tool is neccesary to load the c3d file from the python script.
You can downloand in the link: [C3dServer_setup](https://www.c3d.org/apps/C3Dserver_setup.exe).

### run the script
after install al the necesary tools run the python script. Open a terminal in the pybiomechanic folder and run:
```
python example.py
```