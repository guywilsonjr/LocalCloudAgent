from mypyc.build import mypycify
from setuptools import find_namespace_packages, setup, find_packages



files = find_packages(where='src')
print('Found files: ', files)
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
all_command_args = [*(tokens[1:])]
comstr = ' '.join(all_command_args)
print(comstr)
print(files)
setup(ext_modules=mypycify(paths=['src/local_cloud_agent/__init__.py'], verbose=True, strip_asserts=True))

# RESERVED FOR TRACKING
allow_any_expr_explicit_files = [
   "agent.agent_info",
    "agent.util",
    "agent.post_config",
    "cli.main",
    "agent.operations.util",
    "agent.operations.send"
]
allow_any_explicit_files = ["agent.models"]
