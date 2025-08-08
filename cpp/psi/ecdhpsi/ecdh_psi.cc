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



#include "ecdh_psi.h"
#include <algorithm>
#include "fmt/format.h"

namespace psi {

std::vector<std::string> ecdh_execute(const std::shared_ptr<yacl::link::Context>& lctx,
                                      const std::string& config_json,
                                      const std::vector<std::string>& input) {
    // json解析config_json
    nlohmann::json config = nlohmann::json::parse(config_json);
    // 从config中提取psi_type
    int curve_type = config.value("curve_type", 0);
    SPDLOG_INFO("[ECDHPSI]  config_json: {}", config_json);
    SPDLOG_INFO("[ECDHPSI]  START curve_type: {}", curve_type);
    SPDLOG_INFO("[ECDHPSI]  input size: {}, input[0]: {}", input.size(), input[0]);
    std::vector<std::string> output = ecdh::RunEcdhPsi(lctx, input, yacl::link::kAllRank, static_cast<psi::CurveType>(curve_type));
    SPDLOG_INFO("[ECDHPSI]  END output size: {}", output.size());
    return output;

};

}
