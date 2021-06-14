import os, sys, pathlib
import click
import stat
import d3b_cli_igor.common
import jinja2
from jinja2 import ChoiceLoader, FileSystemLoader

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)


def generate(account_name, organization, region, environment, config_file, mode):
    templateEnv = jinja2.Environment(
        loader=FileSystemLoader(pathlib.Path(__file__).parent.absolute())
    )
    path = os.getcwd()
    logger.info("Checking for Jenkinsfile")
    jenkinsfile = open(path + "/" + config_file, "r")
    logger.info("Found Jenkinsfile")
    lines = jenkinsfile.readlines()
    f = open("tmp_" + mode + "_application", "w")

    logger.info("Generating file")
    f.write("set -e")
    f.write("\n")
    f.write('export account_name="' + account_name + '"')
    f.write("\n")
    f.write('export region="' + region + '"')
    f.write("\n")
    f.write('export vpc_prefix="apps"')
    f.write("\n")
    f.write('export TF_VAR_environment="' + environment + '"')
    f.write("\n")
    f.write('export TF_VAR_organization="' + organization + '"')
    f.write("\n")
    f.write("export branch=master")
    f.write("\n")
    f.write("export mode=" + mode)
    f.write("\n")
    for line in lines:
        if "=" in line and "shared-libraries" not in line:
            name, var = line.partition("=")[::2]
            f.write("export TF_VAR_" + name.strip() + "=" + var.strip() + "")
            f.write("\n")
        if "ecs_service_type_1" in line:
            f.write('export architecture_type="aws-ecs-service-type-1"')
            f.write("\n")
            f.write('export cloud_platform="aws"')
            f.write("\n")
            f.write("export TF_VAR_organization=" + organization)
            f.write("\n")
        if "aws_infra_ec2_module" in line:
            f.write('export architecture_type="aws-infra-ec2"')
            f.write("\n")
    template = templateEnv.get_template("templates/"+mode+".tmpl")
    st = os.stat("./tmp_" + mode + "_application")
    os.chmod("./tmp_" + mode + "_application", st.st_mode | stat.S_IEXEC)
    output = template.render()
    f.write(output)
    f.close()
