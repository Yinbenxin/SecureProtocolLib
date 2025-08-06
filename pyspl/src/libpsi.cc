#include "pybind11/functional.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "cpp/psi/psi.h"
#include "cpp/psi/utils/network_utils.h"

namespace py = pybind11;
namespace psi {

PYBIND11_MODULE(libpsi, m) {
  py::class_<Psi>(m, "Psi")
      // JSON配置构造函数
      .def(py::init<const std::string&>(),
           py::arg("config_json"))
      .def("Run", &Psi::Run,
           py::arg("input"));


  py::class_<psi::utils::channel>(m, "Channel")
      .def(py::init<size_t, std::string, std::string, std::string, std::string, size_t, bool, bool, std::map<std::string, std::string>>(),
           py::arg("role"),
           py::arg("taskid"),
           py::arg("chl_type") = "mem",
           py::arg("party"),
           py::arg("redis"),
           py::arg("connect_wait_time") = 60000,
           py::arg("use_redis") = true,
           py::arg("net_log_switch") = false,
           py::arg("meta") = std::map<std::string, std::string>())
      .def("send", &psi::utils::channel::send,
           py::arg("input"))
      .def("recv", &psi::utils::channel::recv);
}

}  // namespace psi
