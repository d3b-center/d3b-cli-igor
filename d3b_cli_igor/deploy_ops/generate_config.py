import os, sys, pathlib
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

def generate(account_name, organization, region, environment, config_file, mode):
    templateEnv = jinja2.Environment(
        loader=FileSystemLoader(str(pathlib.Path(__file__).parent.absolute()))
    )
    path = os.getcwd()
    logger.info("Checking for " + config_file)
    deployment_file = open(path + "/" + config_file, "r")
    logger.info("Found " + config_file)
    lines = deployment_file.readlines()
    f = open("tmp_" + mode + "_application", "w")

    logger.info("Generating file")
    f.write("#!/bin/bash")
    f.write("\n")
    f.write("set -e")
    f.write("\n")
    f.write('export account_name="' + account_name + '"')
    f.write("\n")
    f.write('export region="' + region + '"')
    f.write("\n")
    f.write('export TF_VAR_vpc_prefix="apps"')
    f.write("\n")
    f.write('export TF_VAR_environment="' + environment + '"')
    f.write("\n")
    f.write('export TF_VAR_branch="master"')
    f.write("\n")
    f.write('export TF_VAR_organization="' + organization + '"')
    f.write("\n")
    f.write('export TF_VAR_owner="' + organization + '"')
    f.write("\n")
    f.write("export mode=" + mode)
    f.write("\n")
    client = boto3.client("sts")
    f.write("export TF_VAR_account_id=" + client.get_caller_identity()["Account"])
    f.write("\n")
    for line in lines:
        if "project_name" in line or "projectName" in line:
            name, var = line.partition("=")[::2]
            f.write("\n")
            f.write("export TF_VAR_" + name.strip() + "=" + var.strip() + "")
            f.write("\n")
        if (environment+"_cidr") in line:
            name, var = line.partition("=")[::2]
            f.write("\n")
            f.write("export TF_VAR_chop_cidr=\"[" + var.strip().replace("\"", "\\\"") + "]\"")
            f.write("\n")
    f.write(
        """
    S3_SECRETS_BUCKET_PREFIX="${TF_VAR_organization}-${TF_VAR_account_id}-${region}-${TF_VAR_environment}-secrets/${TF_VAR_projectName}"
    export S3_SECRETS_BUCKET_PREFIX
    if [ ! -z TF_VAR_setup_deploy_secrets ] && [ TF_VAR_setup_deploy_secrets = "true" ]; then
      echo "Secrets Bucket: $S3_SECRETS_BUCKET_PREFIX"
      echo "Entrypoint Command: $ENTRYPOINT_COMMAND"
      aws s3 sync s3://"$S3_SECRETS_BUCKET_PREFIX"/ secrets/
       if ls secrets/*.env 1> /dev/null 2>&1; then
          echo "Setting environmental variables..."
          export $(cat secrets/*.env | xargs) > /dev/null 2>&1;
       else
          echo "INFO: Could not find *.env files"
       fi
       if ls secrets/*.secrets 1> /dev/null 2>&1; then
        echo "Setting environmental variables..."
        export $(cat secrets/*.secrets | xargs) > /dev/null 2>&1;
       else
        echo "INFO: Could not find *.secrets files"
      fi
    rm -rf secrets
    fi
    
    """
    )
    f.write("\n")
    for line in lines:
        if "=" in line and "shared-libraries" not in line:
            name, var = line.partition("=")[::2]
            f.write("export TF_VAR_" + name.strip() + "=" + var.strip() + "")
            f.write("\n")
        if "ecs_service_type_1" in line:
            f.write('export architecture_type="aws-ecs-service-type-1"')
            f.write("\n")
        if "ecs_service_existing_alb" in line:
            f.write('export architecture_type="aws-ecs-service-existing-alb"')
            f.write("\n")
        if "aws_infra_ec2_module" in line:
            f.write('export architecture_type="aws-infra-ec2"')
            f.write("\n")
        if "aws_infra_lambda_module" in line:
            f.write('export architecture_type="aws-infra-lambda"')
            f.write("\n")
        if "aws-alb" in line:
            f.write('export architecture_type="aws-alb"')
            f.write("\n")
    template = templateEnv.get_template("templates/deploy.tmpl")
    st = os.stat("./tmp_" + mode + "_application")
    os.chmod("./tmp_" + mode + "_application", st.st_mode | stat.S_IEXEC)
    output = template.render(mode=mode)
    f.write(output)
    f.close()


def generate_tf_module_files(project, region, account_name, environment, module):
    account_information = {}
    state_files_bucket = ""

    with open(path + "/" + config_file ) as json_file:
        account_information = json.load(json_file)
    backend_file = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=FileSystemLoader("templates/"))

    TEMPLATE_FILES = os.listdir("./templates")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for templ in TEMPLATE_FILES:
        template = templateEnv.get_template(templ)
        if not os.path.exists(module + "/infra-scripts/" + account_name + "/" + region):
            os.makedirs(module + "/infra-scripts/" + account_name + "/" + region)
        for item in environment.split(","):
            file_mapping_path = {
                templ: "./"
                + module
                + "/infra-scripts/"
                + account_name
                + "/"
                + region
                + "/"
                + item
                + "/",
            }
            if not os.path.exists(
                module + "/infra-scripts/" + account_name + "/" + region + "/" + item
            ):
                os.mkdir(
                    module
                    + "/infra-scripts/"
                    + account_name
                    + "/"
                    + region
                    + "/"
                    + item
                )

            outputText = template.render(
                organization=account_information[account_name]["organization"],
                azs=account_information[account_name]["azs"],
                vpc_prefix=account_information[account_name]["vpc_prefix"],
                cidr_addr=account_information[account_name][item + "_cidr"],
                project=project,
                account_name=account_name,
                region=region,
                environment=item,
                state_files_bucket=account_information[account_name][
                    "state_files_bucket"
                ],
            )

            with open(file_mapping_path[templ] + templ, "w") as fh:
                fh.write(outputText)
