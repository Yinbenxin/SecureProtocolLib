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
#include "cpp/psi/volepsi/vole_psi.h"
#include <algorithm>
#include <stdexcept>
#include "fmt/format.h"

namespace psi {



std::vector<std::string> Psi::Run(size_t role, const std::vector<std::string>& input, bool fast_mode, bool malicious, bool broadcast_result){
    SPDLOG_INFO("[Psi] start");
    SPDLOG_INFO("[Psi] role: {}", role);
    SPDLOG_INFO("[Psi] input size: {}", input.size());
    SPDLOG_INFO("[Psi] fast mode: {}", fast_mode);
    SPDLOG_INFO("[Psi] malicious: {}", malicious);
    SPDLOG_INFO("[Psi] broadcast result: {}", broadcast_result);
    switch (psi_type_) {
      case 0: {
        // ECDH PSI
        throw std::runtime_error("ECDH PSI (type 0) is not yet implemented in this version");
      }
      case 1: {
        // VOLE PSI
        VolePsi vole_psi(role_, taskid_, party_, redis_, psi_type_, sysectbits_,  log_dir_, 
                        log_level_, log_with_console_, net_log_switch_, server_output_, 
                        use_redis_, chl_type_,connect_wait_time_, meta_);
        return vole_psi.Run(role, input, fast_mode, malicious, broadcast_result);
      }
      default: {
        throw std::runtime_error("PSI type not supported: " + std::to_string(psi_type_));
      }
    }
}

}  // namespace psi

