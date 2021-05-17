import d3b_cli_igor.common
import boto3,yaml,numpy,sys,time

logger = d3b_cli_igor.common.get_logger(__name__, testing_mode=False, log_format="detailed")

def get_app_logs(app, environment, query, hours):
    client = d3b_cli_igor.common.setup("logs")
    start_time=int(time.time())-hours*(3600)
    end_time=int(time.time())
    log_group="apps-"+ environment +'/'+app
    result = ""
    message = ""
    response = client.start_query(
        logGroupNames=[
        log_group    
        ],
        startTime=start_time,
        endTime=end_time,
        queryString=query,
        limit=200
    )
    while (result == ""):
        results = client.get_query_results(queryId=response['queryId'])
        if(results['status'] == "Complete"):
            result = results['results']
            d3b_cli_igor.common.logger.info("Printing Results:")
        else:
            d3b_cli_igor.common.logger.info("Query in progress")
            time.sleep(1)
    for item in results["results"]:
        for result in item:
            message+=" "+result["value"]
        message+="\n"
        print(message)
