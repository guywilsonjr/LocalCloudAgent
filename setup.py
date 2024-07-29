from mypyc.build import mypycify
from setuptools import setup, find_packages


files = find_packages(where='src/local_cloud_agent')
common_flags = [
    "--strict",
    "--disallow-any-decorated",
    "--disallow-subclassing-any",
    "--disallow-untyped-decorators",
    "--warn-unreachable",
    "--show-error-context",
    "--show-error-code-links",
    "--warn-incomplete-stub",
    "--pretty",
    "--no-namespace-packages"
]
tokens = [token for file in files for token in ['-p', file]]
all_command_args = [*common_flags, *tokens]
print(' '.join(all_command_args))
print(files)
setup(packages=files, ext_modules=mypycify(files))

# RESERVED FOR TRACKING
allow_any_expr_explicit_files = [
    "common.systemd",
    "agent.agent_info",
    "agent.util",
    "agent.post_config",
    "cli.main",
    "agent.operations.util",
    "agent.operations.send"
]
allow_any_unimported_files = ["common.systemd"]
allow_any_explicit_files = ["agent.models"]
