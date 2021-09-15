# location of the Python header files
PYTHON_VERSION = 3.9
PYTHON_INCLUDE = /usr/local/include/python$(PYTHON_VERSION)
# location of the Boost Python include files and library
BOOST_INC = /usr/local/include
BOOST_LIB = /usr/local/lib
# compile mesh classes
TARGET = fast_ai
$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic $(TARGET).o -L$(BOOST_LIB) -fPIC -lboost_python39 -L/usr/local/lib -lpython$(PYTHON_VERSION) -o $(TARGET).so
$(TARGET).o: $(TARGET).cpp
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp
clean:
	rm -f *.o *.so