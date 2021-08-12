import os, sys, pathlib
import click, yaml
import d3b_cli_igor.common

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

config_file = "config/shortcuts.yaml"
check_build_script = "check_build"
awslogin_script = "awslogin"
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


def awslogin():
    os.system(awslogin_script)
