# Copyright 2021 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

workspace(name = "secure_protocol_lib")
load("//bazel:deps.bzl", "deps")
deps()
load("@psi//bazel:repositories.bzl", "psi_deps")
psi_deps()
#
# yacl
# Warning: psi relies on yacl to bring in common 3p libraries.
#          Please make sure yacl_deps are called right after psi_deps.
#
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@yacl//bazel:repositories.bzl", "yacl_deps")
yacl_deps()

load("@gaia_net//bazel:gaia_net_deps.bzl", "gaia_net_deps")

gaia_net_deps()

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@pybind11_bazel//:python_configure.bzl", "python_configure")

python_configure(
    name = "local_config_python",
    python_version = "3",
)

load(
    "@rules_foreign_cc//foreign_cc:repositories.bzl",
    "rules_foreign_cc_dependencies",
)

rules_foreign_cc_dependencies(
    register_built_tools = False,
    register_default_tools = False,
    register_preinstalled_tools = True,
)
load("@bazel_features//:deps.bzl", "bazel_features_deps")

bazel_features_deps()
load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")

grpc_deps()

# Not mentioned in official docs... mentioned here https://github.com/grpc/grpc/issues/20511
load("@com_github_grpc_grpc//bazel:grpc_extra_deps.bzl", "grpc_extra_deps")

grpc_extra_deps()

#
# boost
#
load("@com_github_nelhage_rules_boost//:boost/boost.bzl", "boost_deps")

boost_deps()
