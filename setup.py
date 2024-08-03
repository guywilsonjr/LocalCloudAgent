import os


from mypyc.build import mypycify
from setuptools import setup, find_packages



all_files = find_packages(where='src')
print('Found files: ', all_files)
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
tokens = [token for file in all_files for token in ['-p', file]]
all_command_args = [*(tokens[1:])]
comstr = ' '.join(all_command_args)


all_files = [fp for fp in [os.path.join(dirpath, f) for (dirpath, dirnames, paths) in os.walk('src/local_cloud_agent') for f in paths] if fp.endswith('.py')]

print('Found files: ', all_files)
test_files = [
    'local_cloud_agent',
]

setup(
    ext_modules=mypycify(
        paths=[
            'src/local_cloud_agent'
        ],
        verbose=True,
        strip_asserts=True
    )
)

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
