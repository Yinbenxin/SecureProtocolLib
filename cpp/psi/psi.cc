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
#include "fmt/format.h"

namespace psi {

std::vector<std::string> Psi::Run(const std::vector<std::string>& input){
    SPDLOG_INFO("[Psi] start");
    SPDLOG_INFO("[Psi] input size: {}", input.size());
    if (!input.empty()) {
      SPDLOG_INFO("[Psi] input[0]: {}", input[0]);
    }
    switch (psi_type_) {
      case 0: {
        // ECDH PSI
        ECDHPsi ecdh_psi(role_, taskid_, party_, redis_, psi_type_, curve_type_, sysectbits_,  log_dir_, 
                        log_level_, log_with_console_, net_log_switch_, server_output_, 
                        use_redis_, chl_type_,connect_wait_time_, meta_);
        return ecdh_psi.Run(role_, input, fast_mode_, malicious_, broadcast_result_);
      }
      case 1: {
        // VOLE PSI
        VolePsi vole_psi(role_, taskid_, party_, redis_, psi_type_, sysectbits_,  log_dir_, 
                        log_level_, log_with_console_, net_log_switch_, server_output_, 
                        use_redis_, chl_type_,connect_wait_time_, meta_);
        return vole_psi.Run(role_, input, fast_mode_, malicious_, broadcast_result_);
      }
      default: {
        throw std::runtime_error("PSI type not supported: " + std::to_string(psi_type_));
      }
    }
}

}  // namespace psi

