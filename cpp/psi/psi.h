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
#include "psi/rr22/rr22_psi.h"
#include "psi/rr22/rr22_utils.h"
#include "psi/utils/hash_bucket_cache.h"

// 定义 PSI 类型
// enum PsiType {
//   ECDHPSI = 0,
//   RR22 = 1,
// };
// enum CurveType {
// CURVE_25519 = 1,
// CURVE_FOURQ = 2,
// CURVE_SM2 = 3,
// CURVE_SECP256K1 = 4,
// };

namespace psi {

std::vector<std::string> PsiExecute(const std::shared_ptr<yacl::link::Context>& lctx,
                                    const std::string& config_json,
                                    const std::vector<std::string>& input);

}  // namespace psi


