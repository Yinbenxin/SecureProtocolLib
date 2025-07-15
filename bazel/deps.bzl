load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
def deps():
    _psi()

def _psi():
    maybe(
        http_archive,
        name = "psi",
        urls = [
            "https://github.com/Yinbenxin/psi/archive/refs/tags/2.0.tar.gz",
        ],
        strip_prefix = "psi-2.0",
        sha256 = "82ac4978b5c01438c365be6c2e7aa437a937c3af7df40027d6576b043619b8e3",
    )