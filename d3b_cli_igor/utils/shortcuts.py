import os, sys, pathlib, boto3
import botocore.exceptions
import click, yaml
import d3b_cli_igor.common

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

config_file = "config/shortcuts.yaml"
check_build_script = "check_build"
onboarding_script = "onboarding"
awslogin_script = "awslogin"
dev_env_tunnel_script = "dev-env-tunnel"
path = os.path.dirname(__file__)


def browser(name, browser_type="", list_shortcuts=False):
    stream = open(path + "/" + config_file, "r")
    dictionary = yaml.load(stream, Loader=yaml.FullLoader)
    if list_shortcuts:
        for k, v in dictionary.items():
            print(k + " : " + v["description"])
    else:
        try:
            if browser_type == "":
                os.system("open " + dictionary[name]["name"])
            else:
                os.system('open "' + browser_type + '" ' + dictionary[name]["name"])
        except Exception as e:
            logger.error("Could not find file: " + str(e))


def check_build(account):
    os.system(check_build_script + " " + account)

def onboarding(role,install_os="mac"):
    os.system(onboarding_script + "_" + role + "_" + install_os)

def dev_env_tunnel(environment,cidr_block):
    sts = boto3.client('sts')
    try:
        sts.get_caller_identity()
        print("Credentials are valid.")
        os.system(dev_env_tunnel_script + " " + environment + " " + cidr_block)
    except botocore.exceptions.ClientError:
        print("Credentials are NOT valid. You might want to execute : igor awslogin and export AWS_PROFILE=<profile_name> in order to set credentials.")

def awslogin():
    os.system(awslogin_script)
