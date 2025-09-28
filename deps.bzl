load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
def deps():
    _psi()

def _psi():
    maybe(
        http_archive,
        name = "psi",
        urls = [
            "https://github.com/Yinbenxin/psi/archive/refs/tags/gaia_0.1.1.tar.gz",
        ],
        strip_prefix = "psi-gaia_0.1.1",
    )