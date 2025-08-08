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



#include "cpp/psi/psi.h"
#include "cpp/psi/ecdhpsi/ecdh_psi.h"
#include "cpp/psi/volepsi/vole_psi.h"
#include <algorithm>
#include <stdexcept>
#include <string>
#include <vector>
#include "fmt/format.h"
#include "nlohmann/json.hpp"

namespace psi {

std::vector<std::string> PsiExecute(const std::shared_ptr<yacl::link::Context>& lctx,
                                    const std::string& config_json,
                                    const std::vector<std::string>& input) {
    // json解析config_json
    nlohmann::json config = nlohmann::json::parse(config_json);
    // 从config中提取psi_type
    int psi_protocol = config.value("psi_protocol", 0);
    SPDLOG_INFO("[PsiExecute] psi_protocol: {}", psi_protocol);
    if (psi_protocol == 0) {  // ECDH PSI
        return ecdh_execute(lctx, config_json, input);
    } else if (psi_protocol == 1) {  // VOLE PSI
        return vole_execute(lctx, config_json, input); 
    } else {
        throw std::runtime_error("PSI type not supported: " + std::to_string(psi_protocol));
    }
}


}  // namespace psi

