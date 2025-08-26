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

#include "cpp/tools/logs/log_config.h"
#include <filesystem>

namespace spl {
namespace logging {

void setup_rotating_file_logger(const LogConfig& config) {
    // 检查rotating_logger是否已经被初始化过
    if (spdlog::get("spl_logger") != nullptr) {
        SPDLOG_INFO("Logger 'spl_logger' already exists, skipping initialization");
        return;
    }
    
    // 从文件路径中提取目录路径
    std::filesystem::path file_path(config.log_file_path);
    std::filesystem::path dir_path = file_path.parent_path();
    SPDLOG_INFO("log_file_path: {}", config.log_file_path);
    // 确保日志目录存在
    if (!dir_path.empty()) {
        std::filesystem::create_directories(dir_path);
    }
    
    // 创建旋转文件日志记录器
    auto rotating_logger = spdlog::rotating_logger_mt(
        "spl_logger", 
        config.log_file_path,
        config.max_file_size,
        config.max_files
    );
    
    // 如果启用控制台输出，创建多重输出日志记录器
    if (config.enable_console) {
        auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
        auto file_sink = std::make_shared<spdlog::sinks::rotating_file_sink_mt>(
            config.log_file_path, config.max_file_size, config.max_files);
        
        auto multi_logger = std::make_shared<spdlog::logger>("spl_logger", 
            spdlog::sinks_init_list{console_sink, file_sink});
        spdlog::set_default_logger(multi_logger);
        
        // 设置日志级别和格式
        multi_logger->set_level(config.log_level);
        multi_logger->set_pattern(config.pattern);
        multi_logger->flush_on(config.log_level);
    } else {
        spdlog::set_default_logger(rotating_logger);
        
        // 设置日志级别和格式
        rotating_logger->set_level(config.log_level);
        rotating_logger->set_pattern(config.pattern);
        rotating_logger->flush_on(config.log_level);
    }
    
    // 设置全局日志级别
    spdlog::set_level(config.log_level);
}

void setup_rotating_file_logger(const std::string& log_file_path) {
    LogConfig config;
    config.log_file_path = log_file_path;
    setup_rotating_file_logger(config);
}

}  // namespace logging
}  // namespace spl