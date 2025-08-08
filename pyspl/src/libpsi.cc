#include "pybind11/functional.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "cpp/psi/psi.h"
#include "cpp/psi/utils/network_utils.h"
#include "yacl/base/buffer.h"
#include <cstddef>
#include <string>
#include <map>
#include <memory>

namespace py = pybind11;

#define NO_GIL py::call_guard<py::gil_scoped_release>()
#define PY_CALL_TAG "python_call"

PYBIND11_MODULE(libpsi, m) {


  m.def("psi_execute", &psi::PsiExecute, "psi execute", py::arg("config"),
        py::arg("lctx"), py::arg("input"), NO_GIL);

  // 绑定Context类
  py::class_<yacl::link::Context, std::shared_ptr<yacl::link::Context>>(m, "Context", "the link handle")
      .def(
          "send",
          [](const std::shared_ptr<yacl::link::Context>& self, const std::string& in) -> bool {
            py::gil_scoped_release release;
            // 假设发送方rank=0发送给接收方rank=1
            size_t dst_rank = (self->Rank() == 0) ? 1 : 0;
            self->Send(dst_rank, in, PY_CALL_TAG);
            return true;
          },
          py::arg("data"), "Sends data to the other party")
      .def(
          "recv",
          [](const std::shared_ptr<yacl::link::Context>& self) -> py::bytes {
            py::gil_scoped_release release;
            // 假设接收方从对方rank接收数据
            size_t src_rank = (self->Rank() == 0) ? 1 : 0;
            yacl::Buffer buf = self->Recv(src_rank, PY_CALL_TAG);
            py::gil_scoped_acquire acquire;
            return py::bytes{buf.data<char>(), static_cast<size_t>(buf.size())};
          },
          "Receives data from the other party");
  // 绑定Createlinks函数
  m.def("CreateChannel", 
        [](size_t role,
           const std::string& taskid,
           const std::string& chl_type,
           const std::string& party,
           const std::string& redis,
           const std::map<std::string, std::string>& meta,
           size_t connect_wait_time,
           bool use_redis,
           bool net_log_switch)
            -> std::shared_ptr<yacl::link::Context> {
          py::gil_scoped_release release;
          
          auto ctx = psi::utils::Createlinks(role, taskid, chl_type, party, redis, 
                                               connect_wait_time, use_redis, net_log_switch, meta);
          return ctx;
        },
        py::arg("role"),
        py::arg("taskid"),
        py::arg("chl_type"),
        py::arg("party")="localhost:50051",
        py::arg("redis")="localhost:6379",
        py::arg("meta") = std::map<std::string, std::string>(),
        py::arg("connect_wait_time") = 60000,
        py::arg("use_redis") = true,
        py::arg("net_log_switch") = false,
        "Setup GRPC links for PSI communication");
      
}

