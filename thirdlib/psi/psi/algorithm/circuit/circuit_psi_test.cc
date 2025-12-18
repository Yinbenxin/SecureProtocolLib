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

#include "psi/algorithm/circuit/circuit_psi.h"

#include <future>
#include <iostream>

#include "gtest/gtest.h"
#include "spdlog/spdlog.h"
#include "yacl/base/exception.h"
#include "yacl/link/test_util.h"

#include "psi/utils/test_utils.h"

struct TestParams {
  std::vector<std::string> items_a;
  std::vector<std::string> items_b;
  psi::CurveType curve_type = psi::CurveType::CURVE_25519;
};

namespace psi::circuit {

class CircuitPsiTest : public testing::TestWithParam<TestParams> {};

TEST_P(CircuitPsiTest, Works) {
  auto params = GetParam();
  auto ctxs = yacl::link::test::SetupWorld(2);
  auto proc =
      [&](const std::shared_ptr<yacl::link::Context>& ctx,
          const std::vector<std::string>& id,
          const std::vector<std::vector<int64_t>>& data) -> std::vector<std::vector<int64_t>> {
    return RunCircuitPsi(ctx, id, data, params.curve_type);
  };
  SPDLOG_INFO("items_a:{}", params.items_a[0]);  
  // 创建测试数据：每个item对应一个包含多个int64_t的向量
  std::vector<std::vector<int64_t>> data_a(params.items_a.size(), std::vector<int64_t>(10, 1));
  std::vector<std::vector<int64_t>> data_b(params.items_b.size(), std::vector<int64_t>(10, 10));
  std::future<std::vector<std::vector<int64_t>>> fa =
      std::async(proc, ctxs[0], params.items_a, data_a);
  std::future<std::vector<std::vector<int64_t>>> fb =
      std::async(proc, ctxs[1], params.items_b, data_b);

  auto results_a = fa.get();
  auto results_b = fb.get();

  ASSERT_EQ(results_a.size(), results_b.size());
  ASSERT_GT(results_a.size(), 0u);

  auto feature_size_a = data_a[0].size();
  auto feature_size_b = data_b[0].size();

  for (size_t i = 0; i < results_a.size(); ++i) {
    ASSERT_EQ(results_a[i].size(), results_b[i].size());
    ASSERT_EQ(results_a[i].size(), feature_size_a + feature_size_b);

    for (size_t j = 0; j < feature_size_a; ++j) {
      EXPECT_EQ(results_a[i][j] + results_b[i][j], data_a[0][j]);
    }

    for (size_t j = 0; j < feature_size_b; ++j) {
      auto idx = feature_size_a + j;
      EXPECT_EQ(results_a[i][idx] + results_b[i][idx], data_b[0][j]);
    }
  }
}

INSTANTIATE_TEST_SUITE_P(
    Works_Instances, CircuitPsiTest,
    testing::Values(
        // // more than one batch
        TestParams{test::CreateRangeItems(0, 1000),
                   test::CreateRangeItems(1, 1000),
                   CurveType::CURVE_FOURQ}  //
        ));

}  // namespace psi::circuit
