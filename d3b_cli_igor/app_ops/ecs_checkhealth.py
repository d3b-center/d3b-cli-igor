import d3b_cli_igor.common
import boto3, yaml, numpy, sys, time

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)


def check_health(app, environment, account):
    client = d3b_cli_igor.common.setup("ecs")
    app_cluster = ""
    if environment == "service":
        app_cluster = account + "-" + environment + "-us-east-1-ecs"
    else:
        app_cluster = account + "-apps-" + environment + "-us-east-1-ecs"
    response = client.update_service(
        cluster=(app_cluster),
        service=app + "-" + environment,
        forceNewDeployment=True,
    )
    logger.info("Executed new deployment")
