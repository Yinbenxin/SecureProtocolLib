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

#include "ecdh_psi.h"

namespace {

// 生成随机的测试数据
std::vector<std::string> GenerateTestData(size_t size) {
  // 生成随机的 uint64 数据
  // 确保生成的数字在合理范围内
  std::vector<std::string> data;
  std::mt19937_64 rng(0);  // 使用固定种子 0，与 Python 版本一致
  
  for (size_t i = 0; i < size; ++i) {
    data.push_back(std::to_string(rng() % (1ULL << 63)));
  }
  
  return data;
}

// 准备测试数据
struct TestData {
  std::vector<std::string> input_data;
  std::string taskid;
  std::string party;
  std::string redis;
  size_t sysectbits;
  size_t psi_type;
  size_t curve_type;
  std::string log_dir;
  size_t log_level;
  bool log_with_console;
  bool net_log_switch;
  bool server_output;
  bool use_redis;
  std::string chl_type;
  size_t connect_wait_time;
  std::map<std::string, std::string> meta;
};

// 准备测试环境和数据
TestData PrepareTestData(size_t role, size_t data_size) {
  TestData data;
  data.taskid = "taskid";
  data.party = "localhost:50051";
  data.redis = "localhost:6379";
  data.sysectbits = 112;
  data.psi_type = 1;
  data.curve_type = 1;
  data.log_dir = ".";
  data.log_level = 2;
  data.log_with_console = true;
  data.net_log_switch = false;
  data.server_output = true;
  data.use_redis = true;
  data.chl_type = "mem";
  data.connect_wait_time = 60000;
  data.meta = std::map<std::string, std::string>();
  data.input_data = GenerateTestData(data_size);
  SPDLOG_INFO("Role {} prepared data size: {}", role, data.input_data.size());
  return data;
}

// 运行 ECDHPsi
void RunECDHPsi(size_t role, const TestData& test_data) {
  // 创建 ECDHPsi 实例
  // 注意：这里使用1作为curve_type参数，对应于psi::CurveType::CURVE_25519
  psi::ECDHPsi ecdh_psi(role, test_data.taskid, test_data.party, test_data.redis,
                       test_data.psi_type, test_data.curve_type, test_data.sysectbits,  test_data.log_dir,
                       test_data.log_level, test_data.log_with_console, test_data.net_log_switch,
                       test_data.server_output, test_data.use_redis, test_data.chl_type,
                       test_data.connect_wait_time, test_data.meta);
  
  SPDLOG_INFO("Role {} starting PSI computation...", role);
  
  // 开始计时
  auto start_time = std::chrono::high_resolution_clock::now();
  
  // 调用 Run 方法并获取结果
  auto result = ecdh_psi.Run(role, test_data.input_data, true, false, true);
  
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
  auto prep_start_time = std::chrono::high_resolution_clock::now();
  
  // 先准备好双方的数据
  TestData data0 = PrepareTestData(0,100000);
  TestData data1 = PrepareTestData(1,100000);
  
  // 结束数据准备计时
  auto prep_end_time = std::chrono::high_resolution_clock::now();
  auto prep_duration = std::chrono::duration_cast<std::chrono::milliseconds>(prep_end_time - prep_start_time);
  
  SPDLOG_INFO("Data preparation completed in {} ms, starting PSI computation...", prep_duration.count());
  
  // 开始总体计时
  auto total_start_time = std::chrono::high_resolution_clock::now();
  
  // 创建两个线程，分别运行角色 0 和角色 1 的PSI计算
  std::thread t0(RunECDHPsi, 0, std::ref(data0));
  std::thread t1(RunECDHPsi, 1, std::ref(data1));
  
  // 等待线程结束
  t0.join();
  t1.join();
  
  // 结束总体计时
  auto total_end_time = std::chrono::high_resolution_clock::now();
  auto total_duration = std::chrono::duration_cast<std::chrono::milliseconds>(total_end_time - total_start_time);
  
  SPDLOG_INFO("PSI computation completed.");
  SPDLOG_INFO("Total PSI execution time (including both parties): {} ms", total_duration.count());
  
  return 0;
}