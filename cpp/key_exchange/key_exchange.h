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
#include <cstdint>
#include <future>
#include <mutex>
#include <random>
#include <tuple>
#include <map>
#include "nlohmann/json.hpp"

#include "spdlog/spdlog.h"
#include "fmt/format.h"
#include "yacl/crypto/rand/rand.h"
#include "yacl/crypto/tools/prg.h"
#include "yacl/link/test_util.h"
#include "yacl/link/context.h"
#include "cpp/tools/logs/log_config.h"
// 定义 PSI 类型
// enum KEType {
//   ECDHPSI = 0,
// };
// enum CurveType {
// CURVE_25519 = 1,
// CURVE_FOURQ = 2,
// CURVE_SM2 = 3,
// CURVE_SECP256K1 = 4,
// };

namespace ke {

std::vector<std::string> KEExecute(const std::shared_ptr<yacl::link::Context>& lctx,
                                    const std::string& config_json,
                                    size_t key_exchange_size);
// 使用新的日志配置模块
using spl::logging::setup_rotating_file_logger;
using spl::logging::LogConfig;
                                    
}  // namespace ke


