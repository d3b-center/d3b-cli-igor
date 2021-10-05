import d3b_cli_igor.common
import boto3, yaml, numpy, sys, time

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

def health_check(app, environment, account):
    alb_client = boto3.client('elbv2', region_name="us-east-1")
    albs = alb_client.describe_load_balancers()
    app_resources = [{}]
    app_resource = {}
    app_resources = [] 
    alb_arns = [] 
    alb_sg = []
    for item in albs["LoadBalancers"]:
        tags=alb_client.describe_tags(ResourceArns=[item["LoadBalancerArn"]])
        for tag_desc in tags["TagDescriptions"]:
            for tag in  tag_desc["Tags"]:
                if tag["Key"] == "Name":
                    application = tag["Value"]
                if tag["Key"] == "Environment":
                    env = tag["Value"]
            if application == app and environment == env:
                #Describe Listeners
                app_resource={ "alb": str(item["LoadBalancerArn"]), "alb_sgs": str(item["SecurityGroups"]), "alb_listeners": str(alb_client.describe_listeners(LoadBalancerArn=item["LoadBalancerArn"])['Listeners'])}
                app_resources.append(app_resource)
    logger.info(app_resource)

