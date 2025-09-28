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
std::shared_ptr<yacl::link::Context> Createlinks(
    size_t role,
    const std::string& taskid,
    const std::string& chl_type = "mem",
    const std::string& party = "localhost:50051",
    const std::string& redis = "localhost:6379",
    size_t connect_wait_time = 60000,
    bool use_redis = false,
    bool net_log_switch = false,
    const std::map<std::string, std::string>& meta = {}
);

}  // namespace utils
}  // namespace psi