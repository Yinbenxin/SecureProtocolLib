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



#include "vole_psi.h"
#include <algorithm>



namespace psi {

std::vector<std::string> vole_execute(const std::shared_ptr<yacl::link::Context>& lctx,
                                      const std::string& config_json,
                                      const std::vector<std::string>& input) {
    // json解析config_json
    nlohmann::json config = nlohmann::json::parse(config_json);
    // 从config中提取参数
    bool fast_mode = config.value("fast_mode", true);
    bool malicious = config.value("malicious", false);
    bool broadcast_result = config.value("broadcast_result", true);
    size_t sysectbits = config.value("sysectbits", 112);
    size_t role = config.value("role", 0);
    
    SPDLOG_INFO("[VOLEPSI] START fast_mode: {}, malicious: {}, broadcast_result: {}, sysectbits: {}", 
                fast_mode, malicious, broadcast_result, sysectbits);
    SPDLOG_INFO("[VOLEPSI] input size: {}, input[0]: {}", input.size(), input[0]);
    
    rr22::Rr22PsiOptions psi_options(sysectbits, 0, true);
    if (fast_mode) {
        psi_options.mode = rr22::Rr22PsiMode::FastMode;
    } else {
        psi_options.mode = rr22::Rr22PsiMode::LowCommMode;
    }
    
    psi_options.malicious = malicious;
    std::vector<uint32_t> indices_psi;
    
    rr22::PreProcessFunc pre_f = [&](size_t) {
        std::vector<HashBucketCache::BucketItem> bucket_items(input.size());
        for (size_t i = 0; i < input.size(); ++i) {
            bucket_items[i] = {.index = i, .base64_data = fmt::format("{}", input[i])};
        }
        return bucket_items;
    };
    
    size_t bucket_num = 1;
    std::mutex mtx;
    
    rr22::PostProcessFunc post_f = [&](size_t, const std::vector<HashBucketCache::BucketItem>& bucket_items,
                                       const std::vector<uint32_t>& indices,
                                       const std::vector<uint32_t>& peer_dup_cnt) {
        std::unique_lock lock(mtx);
        for (size_t i = 0; i < indices.size(); ++i) {
            indices_psi.push_back(bucket_items[indices[i]].index);
            for (size_t j = 0; j < peer_dup_cnt[i]; ++j) {
                indices_psi.push_back(bucket_items[indices[i]].index);
            }
        }
    };
    
    auto psi_proc = std::async([&] {
        rr22::Rr22Runner runner(lctx, psi_options, bucket_num, broadcast_result, pre_f, post_f);
        if (role == 0) {
            runner.AsyncRun(0, true);
        } else {
            runner.AsyncRun(0, false);
        }
    });
    psi_proc.get();
    
    std::sort(indices_psi.begin(), indices_psi.end());
    std::vector<std::string> result;
    for (size_t i = 0; i < indices_psi.size(); ++i) {
        result.push_back(input[indices_psi[i]]);
    }
    
    SPDLOG_INFO("[VOLEPSI] END output size: {}", result.size());
    return result;
};

};

