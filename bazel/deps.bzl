load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
def deps():
    _psi()

def _psi():
    maybe(
        http_archive,
        name = "psi",
        urls = [
            "https://github.com/Yinbenxin/psi/archive/refs/tags/gaia2.1.tar.gz",
        ],
        strip_prefix = "psi-gaia2.1",
        sha256 = "6fc7f30b410a23b5c79e3d59a8091952a5f3dd06f1068bc017ff2eb284983a78",
    )