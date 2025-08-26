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

#include <string>
#include <filesystem>
#include "spdlog/spdlog.h"
#include "spdlog/sinks/rotating_file_sink.h"
#include "spdlog/sinks/stdout_color_sinks.h"

namespace spl {
namespace logging {

/**
 * 日志配置结构体
 */
struct LogConfig {
    std::string log_file_path = "spllogs/log";  // 日志文件路径
    size_t max_file_size = 1024 * 1024 * 5;     // 最大文件大小 (5MB)
    size_t max_files = 3;                       // 最大文件数量
    spdlog::level::level_enum log_level = spdlog::level::debug;  // 日志级别
    std::string pattern = "[%Y-%m-%d %H:%M:%S.%e] [%l] [%s:%#] %v";  // 日志格式，包含文件位置
    bool enable_console = true;                // 是否启用控制台输出
};

/**
 * 设置旋转文件日志记录器
 * @param config 日志配置
 */
void setup_rotating_file_logger(const LogConfig& config = LogConfig{});

/**
 * 使用文件路径设置日志记录器（向后兼容）
 * @param log_file_path 日志文件路径
 */
void setup_rotating_file_logger(const std::string& log_file_path);

}  // namespace logging
}  // namespace spl