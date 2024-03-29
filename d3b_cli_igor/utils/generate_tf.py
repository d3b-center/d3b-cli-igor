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
    filelist = []
    for root, dirs, files in os.walk(path):
        for folder in dirs:
            print(os.path.join(root,folder))
            os.makedirs(folder, exist_ok=True)
        for file in files:
            print(file)
            filelist.append(os.path.join(root,file))
    filelist_modified=[]
    for file in filelist:
        index = file.find("template")
        filelist_modified.append(file[index:len(file)])
    return filelist

#Generate TF scaffold using different templates
def generate(project, region, account, environment, template_name):
    templateEnv = jinja2.Environment(
        loader=FileSystemLoader(str(pathlib.Path(__file__).parent.absolute()))
    )
    path = os.getcwd()
    logger.info("Checking for " + config_file)

    for file in get_files(str(pathlib.Path(__file__).parent.absolute())+"/templates/"+template_name+"/"):
        #Generate template
        print(file)
        template_path = file[file.find("templates"):len(file)]
        #Create folder structure
        #template_path_structure=template_path[len("templates/"+template_name+"/"):]
        #if(not os.path.exists(os.path.dirname(template_path_structure))):
        #    print(os.path.dirname(template_path_structure))
            #os.makedirs(os.path.dirname(template_path_structure))
        template = templateEnv.get_template(template_path)
        output = template.render(project=project, region=region, account=account, environment=environment, state_files_bucket=d3b_cli_igor.common.get_account_info()[account]["state_files_bucket"], account_id=d3b_cli_igor.common.get_account_info()[account]["account_id"],azs=d3b_cli_igor.common.get_account_info()[account]["azs"])
        with(open(template_path[len("templates/"+template_name+"/"):len(template_path)], "w")) as f:
            f.write(output)
