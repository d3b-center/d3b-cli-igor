import d3b_cli_igor.common
import boto3
import boto3, yaml, numpy, sys, time
from termcolor import colored

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

def pretty_print(output):
    for item in output:
        print(colored('Application Name: ','red'),colored(item['app'],'green'))
        for k in item:
            print(colored(k,'red'),":",colored(str(item[k]),'green'))


def get_secrets(app, environment, account, region):
    client = boto3.client('s3')
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    bucket = account+"-"+account_id+"-"+region+"-"+environment+"-secrets"
    prefix = app + "/"

    result = client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/")
    for obj in result["Contents"]:
        print(obj["Key"])
        print("=============================")
        s3 = boto3.resource('s3')
        object_body = s3.Object(bucket,obj["Key"])
        print(object_body.get()['Body'].read().decode('utf-8'))
