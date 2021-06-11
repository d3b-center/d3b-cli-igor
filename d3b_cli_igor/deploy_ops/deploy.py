import os, sys, pathlib
import click
import stat
import d3b_cli_igor.common, d3b_cli_igor.deploy_ops.generate_config

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

def deploy_jenkinsfile(account_name, organization, region, environment):
    d3b_cli_igor.deploy_ops.generate_config.generate(account_name, organization, region, environment) 
    logger.info("Generating deployment script")
    os.system('./tmp_deploy_application')
    logger.info("Cleaning Up")
    os.remove('./tmp_deploy_application')

