import os, sys, pathlib
from os.path import exists
import click
import stat, shutil
import fnmatch
from pathlib import Path
import d3b_cli_igor.common, d3b_cli_igor.deploy_ops.generate_config

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

def execute_deploy(account_name, organization, region, environment, config_file, mode, debug=False):
    d3b_cli_igor.deploy_ops.generate_config.generate(
        account_name, organization, region, environment, config_file, mode
    )
    logger.info("Executing deployment script")
    exit_status = os.system("./tmp_" + mode + "_application")
    if exit_status != 0:
        exit_status = 1
    if not debug:  
        logger.info("Cleaning Up")
        os.remove("./tmp_" + mode + "_application")
        dirpath = Path("./tmp")
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
    logger.info("Exit status is : " + str(exit_status))
    sys.exit(exit_status)

def deploy(account_name, organization, region, environment, config_file, mode, debug=False):
    if (not exists(config_file) and "*.deploy" not in config_file):
        logger.error("File "+ config_file +" does not exist")
        sys.exit(1)
    if("*.deploy" in config_file or "*.destroy" in config_file):
        files = fnmatch.filter(os.listdir("./"), "*.deploy")
        for item in files:
            execute_deploy(account_name, organization, region, environment, item, mode, debug=False)
    else:
        execute_deploy(account_name, organization, region, environment, config_file, mode, debug=False)
