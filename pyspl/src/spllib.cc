#include "pybind11/functional.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "cpp/psi/psi.h"
// #include "cpp/key_exchange/key_exchange.h"
#include "cpp/tools/network/network_utils.h"
#include "yacl/base/buffer.h"
#include <cstddef>
#include <string>
#include <map>
#include <memory>

namespace py = pybind11;

#define NO_GIL py::call_guard<py::gil_scoped_release>()
#define PY_CALL_TAG "python_call"

PYBIND11_MODULE(spllib, m) {
  m.doc() = "Secure Protocol Library";

  m.def("psi_execute", &psi::PsiExecute, "psi execute", py::arg("config"),
        py::arg("lctx"), py::arg("input"), NO_GIL);

  // m.def("label_psi_execute", &psi::LabelPsiExecute, "label psi execute", py::arg("config"),
  //       py::arg("lctx"), py::arg("id"), py::arg("label"), NO_GIL);
  
  // m.def("ke_execute", &ke::KEExecute, "key exchange execute", py::arg("config"),
  //       py::arg("lctx"), py::arg("key_exchange_size"), NO_GIL);

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
  // 绑定 Createlinks：基于 network_utils.cc，将 Python 回调适配为 C++ 回调
  m.def("CreateChannel", 
        [](size_t role,
           py::function sendCb, py::function recvCb)
            -> std::shared_ptr<yacl::link::Context> {
          // 持有 Python 回调的指针，并在析构时获取 GIL 以避免 GIL 断言
          auto send_fn = std::shared_ptr<py::function>(
              new py::function(sendCb),
              [](py::function* f) {
                py::gil_scoped_acquire acquire;
                delete f;
              });
          auto recv_fn = std::shared_ptr<py::function>(
              new py::function(recvCb),
              [](py::function* f) {
                py::gil_scoped_acquire acquire;
                delete f;
              });

          // 将 Python 回调包装为 C++ 回调，调用时获取 GIL
          std::function<int(const std::string&, std::string&)> send_wrapper =
              [send_fn](const std::string& tag, std::string& payload) -> int {
                py::gil_scoped_acquire acquire;
                py::bytes py_payload(payload);
                py::object ret = (*send_fn)(tag, py_payload);
                return ret.cast<int>();
              };
          std::function<std::string(const std::string&)> recv_wrapper =
              [recv_fn](const std::string& tag) -> std::string {
                py::gil_scoped_acquire acquire;
                py::object ret = (*recv_fn)(tag);
                return ret.cast<std::string>();
              };

          py::gil_scoped_release release;
          auto ctx = psi::utils::Createlinks(role, std::move(send_wrapper), std::move(recv_wrapper));
          return ctx;
        },
        py::arg("role"),
        py::arg("send_cb"),
        py::arg("recv_cb"),
        "Create Context and inject memory send/recv callbacks");
      
}
