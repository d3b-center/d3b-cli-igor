import d3b_cli_igor.common
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


def health_check(app, environment, account, region):
    app_cluster = ""
    if environment == "service":
        app_cluster = account + "-" + environment + "-"+region+"-ecs"
    else:
        app_cluster = account + "-apps-" + environment + "-"+region+"-ecs"
    alb_client = boto3.client('elbv2', region_name=region)
    ecs_client = boto3.client('ecs', region_name=region)
    rds_client = boto3.client('rds', region_name=region)
    albs = alb_client.describe_load_balancers()
    app_resource = {}
    app_resources = [] 
    alb_arns = [] 
    alb_sg = []
    rds_info={}
    try:
        if environment != "prd":
            rds_info=rds_client.describe_db_instances(DBInstanceIdentifier=app+"-postgres-service-rds")
        else:
            rds_info=rds_client.describe_db_instances(DBInstanceIdentifier=app+"-postgres-"+environment+"-rds")
        rds_info={ "instance_name": str(rds_info["DBInstances"][0]["DBInstanceIdentifier"]), "allocated_storage": str(rds_info["DBInstances"][0]["AllocatedSt   orage"]) }
    except Exception as e:
        logger.info(e)
    for item in albs["LoadBalancers"]:
        tags=alb_client.describe_tags(ResourceArns=[item["LoadBalancerArn"]])
        for tag_desc in tags["TagDescriptions"]:
            for tag in  tag_desc["Tags"]:
                if tag["Key"] == "Name":
                    application = tag["Value"]
                if tag["Key"] == "Environment":
                    env = tag["Value"]
            if application == app and environment == env:
                service=ecs_client.describe_services(cluster=app_cluster,services=[app+"-"+environment])['services'][0]
                app_resource={ "app": app, "alb": str(item["LoadBalancerArn"]), "alb_sgs": str(item["SecurityGroups"]), "alb_listeners": str(alb_client.describe_listeners(LoadBalancerArn=item["LoadBalancerArn"])['Listeners']),"service_info":{"status":service['status'],"desired_count": service['desiredCount'], 'running_count': service['runningCount'], 'pending_count': service['pendingCount'], 'deployments': service['deployments']},"rds_info": rds_info }
                app_resources.append(app_resource)
    pretty_print(app_resources)

