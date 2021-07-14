import os, sys, pathlib
import click,yaml
import d3b_cli_igor.common

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

config_file="d3b_cli_igor/utils/config/shortcuts.yaml"

def browser(name, browser_type="", list_shortcuts=False):
    path = os.getcwd()
    stream = open(path+"/"+config_file, 'r')
    dictionary = yaml.load(stream, Loader=yaml.FullLoader)
    if (list_shortcuts):
        for k, v in dictionary.items():
            logger.info(k + " : " + v)
    else:
        try:
            if(browser_type == ""): 
                os.system("open " + dictionary[name])
            else:
                os.system("open \"" + browser_type + "\" " + dictionary[name])
        except Exception as e:
            logger.error("Could not find file: " + str(e))
