import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="d3b-cli-igor",
    version="0.1",
    scripts=["igor","d3b_cli_igor/utils/scripts/awslogin","d3b_cli_igor/utils/scripts/check_build"],
    author="Alex Lubneuski",
    author_email="alex@d3b.center",
    description="D3b DevOps-y Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d3b-center/d3b-cli-igor",
    packages=['d3b_cli_igor','d3b_cli_igor.app_ops','d3b_cli_igor.deploy_ops','d3b_cli_igor.log_ops','d3b_cli_igor.utils','d3b_cli_igor.utils.scripts.check_build'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
