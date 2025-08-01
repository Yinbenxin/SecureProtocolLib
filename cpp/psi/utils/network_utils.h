// Copyright 2022 Ant Group Co., Ltd.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include <memory>
#include <string>
#include <vector>
#include <map>

// 前向声明
namespace yacl {
namespace link {
class Context;
}  // namespace link
}  // namespace yacl

namespace psi {
namespace utils {

// 获取可用端口的辅助函数
int GetAvailablePort();

// 设置GRPC链接的函数
std::shared_ptr<yacl::link::Context> SetupGrpclinks(
    size_t role,
    const std::string& taskid,
    const std::string& chl_type,
    const std::string& party,
    const std::string& redis,
    size_t connect_wait_time,
    bool use_redis,
    bool net_log_switch,
    const std::map<std::string, std::string>& meta
);

class channel {
 public:
  channel(size_t role, std::string taskid, std::string chl_type, std::string party, std::string redis, size_t connect_wait_time, bool use_redis, bool net_log_switch, std::map<std::string, std::string> meta);
  ~channel();
  bool send(std::string input);
  std::string recv();
 private:
  size_t role_;
  std::string taskid_;
  std::string party_;
  std::string redis_;
  std::shared_ptr<yacl::link::Context> ctx_;
};


}  // namespace utils
}  // namespace psi