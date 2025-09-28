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



#include <algorithm>
#include <stdexcept>
#include <string>
#include <vector>
#include <filesystem>
#include "fmt/format.h"
#include "nlohmann/json.hpp"
#include "cpp/key_exchange/key_exchange.h"
#include "cpp/key_exchange/ecdhke/ecdh_ke.h"
#include "cpp/tools/logs/log_config.h"
namespace ke {

// 日志设置函数已移动到 cpp/tools/logs/log_config.cc

std::vector<std::string> KEExecute(const std::shared_ptr<yacl::link::Context>& lctx,
                                    const std::string& config_json,
                                    size_t key_exchange_size) {
    // json解析config_json
    nlohmann::json config = nlohmann::json::parse(config_json);
    // 从config中提取psi_type
    auto log_dir = config.value("log_dir", "spllog");
    spl::logging::setup_rotating_file_logger(log_dir);
    int protocol = config.value("protocol", 0);
    SPDLOG_INFO("[KEExecute] protocol: {}", protocol);
    if (protocol == 0) {  // ECDH PSI
        return ecdhke_execute(lctx, config_json, key_exchange_size);
    } else {
        throw std::runtime_error("PSI type not supported: " + std::to_string(protocol));
    }
}
}  // namespace ke



