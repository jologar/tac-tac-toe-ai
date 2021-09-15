#include <iostream>
#include "fast_ai.h"
#include <boost/python.hpp>
#include <boost/python/call.hpp>

namespace {

    struct AiConfig {
        char player1;
        char player2;
        char emptyValue;
        PyObject* callback;
    };
    
    class MinMaxAi {
        public:
            MinMaxAi(AiConfig config) {
                aiconfig = config;
            };
            char test() {
                return boost::python::call<char>(aiconfig.callback);
            };
            int getPlayerMove() {
                return 23;
            };
        private:
            AiConfig aiconfig;
            int minmax() {
                return 0;
            };
    };
}

BOOST_PYTHON_MODULE(fast_ai)
{
    using namespace boost::python;
    
    class_<AiConfig>("AiConfig")
        .def_readwrite("player1", &AiConfig::player1)
        .def_readwrite("player2", &AiConfig::player2)
        .def_readwrite("emptyValue", &AiConfig::emptyValue)
        .def_readwrite("callback", &AiConfig::callback);

    class_<MinMaxAi>("MinMaxAi", init<AiConfig&>())
        .def("getPlayerMove", &MinMaxAi::getPlayerMove)
        .def("test", &MinMaxAi::test);
}
