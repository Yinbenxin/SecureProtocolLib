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
#include "yacl/link/context.h"

// 前向声明
// 依赖 yacl::link::Context 及其回调类型

namespace psi {
namespace utils {

// 获取可用端口的辅助函数
int GetAvailablePort();

// 设置链接并注入发送/接收回调
std::shared_ptr<yacl::link::Context> Createlinks(
    size_t role,
    std::function<int(const std::string &, std::string &)> send_cb,
    std::function<std::string(const std::string&)> recv_cb);

}  // namespace utils
}  // namespace psi
