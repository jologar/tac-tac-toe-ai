# TIC TAC TOE AI

This project implements a simple Tic Tac Toe game that allows the user to play against the AI.

The purpose of this project is to refresh basic AI algorithms knowledge and learning C++ and how to embed it as library inside a Python project using [Boost Python](https://www.boost.org/doc/libs/1_77_0/libs/python/doc/html/index.html).

Also, as the AI algorithm is implemented in both Python and C++, a simple evaluation script has been created in order to compare the algorithm performance in each case.

## Requirements

In order to be able to install and run this game, you should fulfill the following requirements.

<b>[Python 3](https://www.python.org/downloads/)</b>

You should check that your python distribution is compiled with the `-fPIC` flag. If not, the Python interpreper is not going to be able to use libboostpython to find and call the Python Boost symbols in the C++ library.

Is highly recommended to create a custom python environment in which install all the following dependencies.

<b>[Python Boost](https://www.boost.org/doc/libs/1_77_0/libs/python/doc/html/index.html)</b>

Download the latest version of Python Boost (for this project, version 1.77.0 is used). Follow the installation instructions [here](https://www.boost.org/doc/libs/1_77_0/more/getting_started/unix-variants.html#prepare-to-use-a-boost-library-binary), BUT be sure that in the `b2 install` step, you pass the `-fPIC` flag in order for Boost to be compiled with this option, also. i.e:
```
./b2 cflags=-fPIC cxxflags=-fPIC ... install
```

<b>[Tkinter](https://docs.python.org/3/library/tkinter.html)</b>

This project uses Tkinter to build a simple desktop GUI. You should also install [Pillow](https://pypi.org/project/Pillow/).

<b>[GCC](https://gcc.gnu.org/)</b>

Or your favourite C compiler :)

<b>[Matplotlib](https://matplotlib.org/)</b> (optional)

Only needed if you want to use the [evaluation](https://github.com/jologar/tac-tac-toe-ai/blob/master/evaluation.py) script.



## Installation

1. Clone the repo in your local machine.
2. Be sure you fulfill the requirements
3. Compile the C++ library in your system: navigate to `fastai` folder and execute:
```
make clean && make
```
4. In base folder, run:
```
python3 main.py
```
4. Try to beat the AI. Luck!
