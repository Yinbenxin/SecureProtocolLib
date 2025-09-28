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



#include "circuit_psi.h"
#include <algorithm>
#include "fmt/format.h"

namespace psi {

std::vector<std::vector<int64_t>> circuit_execute(const std::shared_ptr<yacl::link::Context>& lctx,
                                      const std::string& config_json,
                                      const std::vector<std::string>& id,
                                    const std::vector<std::vector<int64_t>>& data) {
    // json解析config_json
    nlohmann::json config = nlohmann::json::parse(config_json);
    // 从config中提取psi_type
    int curve_type = config.value("curve_type", 0);
    SPDLOG_INFO("[CircuitPSI]  START curve_type: {}", curve_type);
    SPDLOG_INFO("[CircuitPSI]  id size: {}, id[0]: {}", id.size(), id[0]);
    SPDLOG_INFO("[CircuitPSI]  config_json: {}", config_json);
    SPDLOG_INFO("[CircuitPSI]  data size: {}, data[0]: {}", data.size(), data[0][0]);
    auto output = circuit::RunCircuitPsi(lctx, id, data, static_cast<psi::CurveType>(curve_type));
    SPDLOG_INFO("[CircuitPSI]  END output size: {}", output.size());
    return output;

};


}