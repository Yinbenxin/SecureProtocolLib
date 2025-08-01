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

std::vector<std::string> ECDHPsi::Run(size_t role, const std::vector<std::string>& input, bool fast_mode, bool malicious, bool broadcast_result){
    SPDLOG_INFO("[ECDHPsi] start");
    SPDLOG_INFO("[ECDHPsi] role: {}", role);
    SPDLOG_INFO("[ECDHPsi] input size: {}", input.size());
    SPDLOG_INFO("[ECDHPsi] fast mode: {}", fast_mode);
    SPDLOG_INFO("[ECDHPsi] malicious: {}", malicious);
    SPDLOG_INFO("[ECDHPsi] broadcast result: {}", broadcast_result);
    
  std::shared_ptr<yacl::link::Context> lctxs = utils::SetupGrpclinks(role_, taskid_, chl_type_, party_, redis_, 
                               connect_wait_time_, use_redis_, net_log_switch_, meta_);
  // 使用类成员变量curve_type_，它在构造函数中被初始化为传入的curve_type参数
  // 通过static_cast将size_t类型的curve_type_转换为psi::CurveType枚举类型
  psi::CurveType curve_type = static_cast<psi::CurveType>(curve_type_);
  // 使用yacl::link::kAllRank作为target_rank，表示结果广播给所有参与方
  std::vector<std::string> output = ecdh::RunEcdhPsi(lctxs, input, yacl::link::kAllRank, curve_type);
  SPDLOG_INFO("[ECDHPsi] output size: {}", output.size());
  return output;
    
};

};

