import sys, pathlib
import os as os
import click
import stat
import d3b_cli_igor.common
import jinja2, json, boto3
from jinja2 import ChoiceLoader, FileSystemLoader

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

path = os.path.dirname(__file__)
config_file = "config/account_info.json"

#Get files in the folder
def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

#Generate TF scaffold using different templates
def generate(project, region, account, environment, template_name):
    templateEnv = jinja2.Environment(
        loader=FileSystemLoader(str(pathlib.Path(__file__).parent.absolute()))
    )
    path = os.getcwd()
    logger.info("Checking for " + config_file)
    
    for file in get_files(str(pathlib.Path(__file__).parent.absolute())+"/templates/"+template_name+"/"):
        template = templateEnv.get_template("templates/"+template_name+"/"+file)
        output = template.render(project=project, region=region, account=account, environment=environment, state_files_bucket=d3b_cli_igor.common.get_account_info()[account]["state_files_bucket"])
        with(open(file, "w")) as f:
            f.write(output)
