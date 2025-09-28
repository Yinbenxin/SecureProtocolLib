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

#include <iostream>
#include <random>
#include <string>
#include <thread>
#include <vector>
#include <functional>
#include <map>
#include <chrono>
#include "spdlog/spdlog.h"
#include "fmt/format.h"
#include "nlohmann/json.hpp"
#include "yacl/link/test_util.h"
#include "yacl/link/context.h"

#include "cpp/key_exchange/ecdhke/ecdh_ke.h"
#include "cpp/psi/utils/network_utils.h"
namespace {

// 运行 ECDHKE
void RunECDHKE(size_t role, size_t key_exchange_size) {
  // 创建配置JSON
  nlohmann::json config;
  config["role"] = role;
  config["psi_protocol"] = 0;  // ECDH PSI
  config["curve_type"] = 1;   // CURVE_25519
  
  std::string config_json = config.dump();
  
  // 创建链接
  auto ctx = psi::utils::Createlinks(role, "ECDH-KE-test", "mem");
  SPDLOG_INFO("Role {} starting ECDHKE computation...", role);
  
  // 开始计时
  auto start_time = std::chrono::high_resolution_clock::now();
  
  // 调用 ecdh_execute 方法并获取结果
  auto result = ke::ecdhke_execute(ctx, config_json, key_exchange_size);
  
  // 结束计时
  auto end_time = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
  
  // 打印耗时
  SPDLOG_INFO("Role {} PSI computation time: {} ms", role, duration.count());
  
  // 打印结果
  SPDLOG_INFO("Role {} PSI result count: {}", role, result.size());
  SPDLOG_INFO("Role {} PSI first 5 results: ", role);
  
  size_t count = std::min(result.size(), size_t(5));
  std::string results_str;
  for (size_t i = 0; i < count; ++i) {
    results_str += result[i];
    if (i < count - 1) {
      results_str += ", ";
    }
  }
  SPDLOG_INFO("Results: {}", results_str);
}

}  // namespace

int main() {

  SPDLOG_INFO("Preparing test data...");
  
  // 开始数据准备计时
  
  // 创建两个线程，分别运行角色 0 和角色 1 的PSI计算
  std::thread t0(RunECDHKE, 0, 10000);
  std::thread t1(RunECDHKE, 1, 10000);
  
  // 等待线程结束
  t0.join();
  t1.join();
  
  SPDLOG_INFO("PSI computation completed.");
  
  return 0;
}