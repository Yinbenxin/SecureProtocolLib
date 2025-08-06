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
class Psi {
 public:
  // JSON配置构造函数
  Psi(const std::string& config_json) {
    SPDLOG_INFO("config_json: {}", config_json);
    InitializeFromJson(config_json);
  }

private:
  void InitializeFromParams(size_t role, std::string taskid, std::string party, std::string redis, 
         size_t psi_type, size_t curve_type, size_t sysectbits, std::string log_dir, 
         size_t log_level, bool log_with_console, bool net_log_switch, 
         bool server_output, bool use_redis, std::string chl_type, size_t connect_wait_time,
         const std::map<std::string, std::string> &meta) {
    // 移除 meta 参数，因为 fmt 无法格式化 std::map
    SPDLOG_INFO("role: {}, taskid: {}, party: {}, redis: {}, sysectbits: {}, psi_type: {}, log_dir: {}, log_level: {}, log_with_console: {}, net_log_switch: {}, server_output: {}, use_redis: {}, chl_type: {}",
                role, taskid, party, redis, sysectbits, psi_type, log_dir, log_level, log_with_console, net_log_switch, server_output, use_redis, chl_type);
    role_ = role;
    taskid_ = taskid;
    party_ = party;
    redis_ = redis;
    psi_type_ = psi_type;
    curve_type_ = curve_type;
    sysectbits_ = sysectbits;
    log_dir_ = log_dir;
    log_level_ = log_level;
    log_with_console_ = log_with_console;
    net_log_switch_ = net_log_switch;
    server_output_ = server_output;
    use_redis_ = use_redis;
    chl_type_ = chl_type;
    meta_ = meta;
    connect_wait_time_ = connect_wait_time;
  }

  void InitializeFromJson(const std::string& config_json) {
    try {
      auto config = nlohmann::json::parse(config_json);
      
      // 解析JSON配置
      role_ = config.value("role", 0);
      taskid_ = config.value("taskid", "");
      party_ = config.value("party", "localhost:50051");
      redis_ = config.value("redis", "localhost:6379");
      psi_type_ = config.value("psi_type", 1);
      curve_type_ = config.value("curve_type", 1);
      sysectbits_ = config.value("sysectbits", 112);
      log_dir_ = config.value("log_dir", ".");
      log_level_ = config.value("log_level", 2);
      log_with_console_ = config.value("log_with_console", true);
      net_log_switch_ = config.value("net_log_switch", false);
      server_output_ = config.value("server_output", true);
      use_redis_ = config.value("use_redis", true);
      chl_type_ = config.value("chl_type", "mem");
      connect_wait_time_ = config.value("connect_wait_time", 60000);
      fast_mode_ = config.value("fast_mode", true);
      malicious_ = config.value("malicious", false);
      broadcast_result_ = config.value("broadcast_result", true);
      // 解析meta字段
      if (config.contains("meta") && config["meta"].is_object()) {
        for (auto& [key, value] : config["meta"].items()) {
          if (value.is_string()) {
            meta_[key] = value.get<std::string>();
          }
        }
      }
      
      SPDLOG_INFO("Initialized from JSON - role: {}, taskid: {}, party: {}, redis: {}, psi_type: {}, curve_type: {}", 
                  role_, taskid_, party_, redis_, psi_type_, curve_type_);
    } catch (const std::exception& e) {
      SPDLOG_ERROR("Failed to parse JSON config: {}", e.what());
      throw std::runtime_error("Invalid JSON configuration: " + std::string(e.what()));
    }
  }

public:
  
  ~Psi() = default;
  std::vector<std::string> Run(const std::vector<std::string>& input);

    
private:
  size_t role_;
  std::string taskid_;
  std::string party_;
  std::string redis_;
  size_t sysectbits_ = 112;
  size_t psi_type_ = 1;
  size_t curve_type_ = 1;
  std::string log_dir_ = ".";
  size_t log_level_ = 2;
  size_t connect_wait_time_ =20000;
  bool log_with_console_ = true;
  bool net_log_switch_ = false;
  bool server_output_ = true;
  bool use_redis_ = true;
  std::string chl_type_ = "mem";
  std::map<std::string, std::string> meta_;
  bool fast_mode_ = true;
  bool malicious_ = false;
  bool broadcast_result_ = true;
};



}  // namespace psi


