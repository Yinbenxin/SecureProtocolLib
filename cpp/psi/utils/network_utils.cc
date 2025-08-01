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

#include "network_utils.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include "fmt/format.h"
#include "spdlog/spdlog.h"
#include "yacl/link/context.h"
#include "yacl/link/test_util.h"
#include "yacl/base/buffer.h"
namespace psi {
namespace utils {

// 获取可用端口的辅助函数
int GetAvailablePort() {
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    return -1;
  }
  
  struct sockaddr_in addr;
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = INADDR_ANY;
  addr.sin_port = 0; // 让系统自动分配端口
  
  if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
    close(sockfd);
    return -1;
  }
  
  socklen_t len = sizeof(addr);
  if (getsockname(sockfd, (struct sockaddr*)&addr, &len) < 0) {
    close(sockfd);
    return -1;
  }
  
  int port = ntohs(addr.sin_port);
  close(sockfd);
  return port;
}

// 设置GRPC链接的函数
std::shared_ptr<yacl::link::Context> SetupGrpclinks(
    size_t role,
    const std::string& taskid,
    const std::string& chl_type,
    const std::string& party,
    const std::string& redis,
    size_t connect_wait_time,
    bool use_redis,
    bool net_log_switch,
    const std::map<std::string, std::string>& meta
) {
  size_t world_size = 2;
  yacl::link::ContextDesc ctx_desc;
  
  // 获取两个可用端口
  std::vector<size_t> available_ports;
  for (size_t i = 0; i < world_size; i++) { 
    int port = GetAvailablePort();
    if (port > 0) {
      available_ports.push_back(port);
    } else {
      // 如果获取失败，使用默认端口作为备选
      available_ports.push_back(10086 + i * 10);
    }
  }
  
  SPDLOG_INFO("available ports: {}", available_ports[0]);
  for (size_t rank = 0; rank < world_size; rank++) {
    const auto id = fmt::format("id-{}", rank);
    const auto host = fmt::format("127.0.0.1:{}", available_ports[rank]);
    ctx_desc.parties.emplace_back(id, host);
  }
  auto lctx = yacl::link::FactoryBrpc().CreateContext(ctx_desc, role);
  lctx->add_gaia_net(taskid, chl_type, party, redis, connect_wait_time, use_redis, net_log_switch, meta);
  return lctx;
}


channel::channel(size_t role, std::string taskid, std::string chl_type, std::string party, std::string redis, size_t connect_wait_time, bool use_redis, bool net_log_switch, std::map<std::string, std::string> meta) 
    : role_(role), taskid_(taskid), party_(party), redis_(redis) {
  ctx_ = SetupGrpclinks(role, taskid, chl_type, party, redis, connect_wait_time, use_redis, net_log_switch, meta);
}

channel::~channel() {
  // 析构函数实现
}

bool channel::send(std::string input) {
  yacl::Buffer buffer(input.c_str(), input.length());
  ctx_->Send((role_ + 1) % 2, buffer, "tag");
  return true;
}

std::string channel::recv() {
  auto value = ctx_->Recv((role_ + 1) % 2, "tag");
  std::string ret(static_cast<const char*>(value.data()), value.size());
  return ret;
}



}  // namespace utils
}  // namespace psi