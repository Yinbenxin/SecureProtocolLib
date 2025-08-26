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



#include "cpp/key_exchange/ecdhke/ecdh_ke.h"
#include <algorithm>
#include "fmt/format.h"

namespace ke {
std::vector<std::string> ecdhke_execute(const std::shared_ptr<yacl::link::Context>& lctx,
                                      const std::string& config_json,
                                      size_t key_exchange_size) {
    // json解析config_json
    nlohmann::json config = nlohmann::json::parse(config_json);
    // 从config中提取psi_type
    size_t curve_type = config.value("curve_type", 0);
    size_t batch_size = config.value("batch_size", 4096);
    SPDLOG_INFO("[ECDHKE]  config_json: {}", config_json);
    SPDLOG_INFO("[ECDHKE]  START curve_type: {}", curve_type);
    SPDLOG_INFO("[ECDHKE]  batch_size: {}", batch_size);
    SPDLOG_INFO("[ECDHKE]  key_exchange_size: {}", key_exchange_size);

    std::vector<std::string> raw_output = psi::ecdhke::RunEcdhKe(lctx, key_exchange_size, yacl::link::kAllRank, static_cast<psi::CurveType>(curve_type), batch_size);
    
    SPDLOG_INFO("[ECDHKE]  END output size: {}", raw_output.size());
    return raw_output;

}  
}// namespace ke
