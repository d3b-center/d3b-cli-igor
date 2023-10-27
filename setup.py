import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="d3b-cli-igor",
    version="0.2",
    scripts=[
        "igor",
        "d3b_cli_igor/utils/scripts/awslogin",
        "d3b_cli_igor/utils/scripts/check_build",
        "d3b_cli_igor/utils/scripts/github_open",
        "d3b_cli_igor/utils/scripts/dev-env-tunnel",
        "d3b_cli_igor/utils/scripts/onboarding_devops_mac",
        "d3b_cli_igor/utils/scripts/onboarding_devops_ubuntu",
        "d3b_cli_igor/utils/scripts/onboarding_dev_mac",
        "d3b_cli_igor/utils/scripts/onboarding_dev_ubuntu",
    ],
    author="Alex Lubneuski",
    author_email="alex@d3b.center",
    description="D3b Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d3b-center/d3b-cli-igor",
    packages=[
        "d3b_cli_igor",
        "d3b_cli_igor.app_ops",
        "d3b_cli_igor.deploy_ops",
        "d3b_cli_igor.log_ops",
        "d3b_cli_igor.utils",
    ],
    package_data={
        'd3b_cli_igor.deploy_ops': ['templates/*.tmpl'],
        'd3b_cli_igor.deploy_ops': ['config/*.json'],
        'd3b_cli_igor.utils': ['templates/*/**'],
        'd3b_cli_igor': ['config/*.json'],
    },
    include_package_data=True,
    install_requires=[
        'numpy',
        'jinja2',
        'boto3',
        'colorlog',
        'click',
        'pyyaml',
        'datetime',
        'aws-ssm-tools',
        'auth0-login',
        'botocore',
        'colored',
        'termcolor'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
