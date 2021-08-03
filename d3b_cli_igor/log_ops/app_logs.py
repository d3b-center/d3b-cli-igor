import d3b_cli_igor.common
import boto3,yaml,numpy,sys,time

logger = d3b_cli_igor.common.get_logger(__name__, testing_mode=False, log_format="detailed")

def get_app_logs(app, environment, query, hours):
    client = d3b_cli_igor.common.setup("logs")
    start_time=int(time.time())-hours*(3600)
    start_time, i = divmod(start_time,1)
    start_time = int(start_time)
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
    count=0
    while (result == ""):
        results = client.get_query_results(queryId=response['queryId'])
        if(results['status'] == "Complete"):
            count=0
            result = results['results']
            d3b_cli_igor.common.logger.info("Printing Results:")
        else:
            count +=1
            d3b_cli_igor.common.progress_bar(count, "Query in progress... ", " second(s)")
            time.sleep(1)
    for item in results["results"]:
        for result in item:
            message+=" "+result["value"]
        message+="\n"
        print(message)
